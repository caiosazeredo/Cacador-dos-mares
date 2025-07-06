# src/tile_manager.py - Gerenciador de Tiles

import pygame
import os
from config import *

class TileManager:
    """Gerenciador de tiles para o jogo"""
    
    def __init__(self):
        self.tiles = {}
        self.water_tile = None
        self.load_tiles()
    
    def load_tiles(self):
        """Carrega todos os tiles disponíveis"""
        print("Carregando tiles...")
        
        # Carrega o tile de água específico
        water_path = os.path.join(TILES_PATH, WATER_TILE)
        if os.path.exists(water_path):
            try:
                self.water_tile = pygame.image.load(water_path).convert_alpha()
                # Redimensiona para o tamanho correto se necessário
                if self.water_tile.get_size() != (TILE_SIZE, TILE_SIZE):
                    self.water_tile = pygame.transform.scale(self.water_tile, (TILE_SIZE, TILE_SIZE))
                print(f"✓ Tile de água carregado: {WATER_TILE}")
            except Exception as e:
                print(f"✗ Erro ao carregar tile de água: {e}")
                self.create_fallback_water_tile()
        else:
            print(f"✗ Tile de água não encontrado: {water_path}")
            self.create_fallback_water_tile()
        
        # Carrega outros tiles se necessário
        self.load_additional_tiles()
    
    def create_fallback_water_tile(self):
        """Cria um tile de água de emergência caso o arquivo não seja encontrado"""
        print("Criando tile de água alternativo...")
        self.water_tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        # Cria um padrão de água simples com variações de azul
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                # Cria um efeito de ondas usando seno
                import math
                wave = math.sin(x * 0.2) * math.cos(y * 0.2) * 20
                base_color = 100 + wave
                
                blue_value = max(150, min(255, int(base_color + 100)))
                green_value = max(100, min(200, int(base_color + 50)))
                
                color = (0, green_value, blue_value, 255)
                self.water_tile.set_at((x, y), color)
    
    def load_additional_tiles(self):
        """Carrega tiles adicionais se disponíveis"""
        if not os.path.exists(TILES_PATH):
            return
        
        for filename in os.listdir(TILES_PATH):
            if filename.endswith('.png') and filename != WATER_TILE:
                try:
                    tile_path = os.path.join(TILES_PATH, filename)
                    tile = pygame.image.load(tile_path).convert_alpha()
                    if tile.get_size() != (TILE_SIZE, TILE_SIZE):
                        tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
                    self.tiles[filename] = tile
                except Exception as e:
                    print(f"Erro ao carregar tile {filename}: {e}")
    
    def get_water_tile(self):
        """Retorna o tile de água"""
        return self.water_tile
    
    def get_tile(self, tile_name):
        """Retorna um tile específico pelo nome"""
        return self.tiles.get(tile_name)
