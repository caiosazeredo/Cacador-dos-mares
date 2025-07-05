# src/sprite_loader.py - Sistema PNG profissional corrigido

import pygame
import os
from config import *

# Inicializa pygame
pygame.init()
pygame.display.set_mode((1, 1), pygame.NOFRAME)

class SpriteManager:
    """Gerenciador de sprites PNG"""
    
    def __init__(self):
        self.sprites = {}
        self.load_png_sprites()
    
    def load_png_sprites(self):
        """Carrega sprites PNG individuais"""
        print("Carregando sprites PNG profissionais...")
        
        # Sprites necessários
        sprites_necessarios = [
            'fish_blue.png',
            'fish_brown.png',
            'fish_green.png',
            'fish_orange.png', 
            'fish_pink.png',
            'fish_grey.png',
            'ship (1).png',
            'ship (2).png',
            'ship (3).png',
            'ship (4).png'
        ]
        
        sprites_carregados = 0
        
        for sprite_name in sprites_necessarios:
            sprite_path = os.path.join(IMAGES_PATH, sprite_name)
            
            if os.path.exists(sprite_path):
                try:
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    
                    # Remove extensão para compatibilidade
                    nome_limpo = sprite_name.replace('.png', '')
                    self.sprites[nome_limpo] = sprite
                    self.sprites[sprite_name] = sprite
                    
                    print(f"Sprite carregado: {sprite_name} - {sprite.get_size()}")
                    sprites_carregados += 1
                    
                except Exception as e:
                    print(f"Erro ao carregar {sprite_name}: {e}")
            else:
                print(f"Nao encontrado: {sprite_path}")
        
        print(f"Sprites PNG carregados: {sprites_carregados}")
        self.criar_mapeamentos()
    
    def criar_mapeamentos(self):
        """Cria mapeamentos alternativos"""
        # Mapeia fish_gray para fish_grey
        if 'fish_grey' in self.sprites:
            self.sprites['fish_gray'] = self.sprites['fish_grey']
    
    def get_sprite(self, sprite_name, sheet_name=None):
        """Retorna sprite pelo nome"""
        nome_limpo = sprite_name.replace('.png', '')
        
        if sprite_name in self.sprites:
            return self.sprites[sprite_name]
        elif nome_limpo in self.sprites:
            return self.sprites[nome_limpo]
        
        return None
    
    def get_fish_sprite(self, fish_color):
        """Retorna peixe por cor"""
        color_map = {
            (255, 165, 0): 'fish_orange',
            (255, 192, 203): 'fish_pink',
            (135, 206, 250): 'fish_blue',
            (152, 251, 152): 'fish_green',
            (128, 128, 128): 'fish_grey',
            (139, 69, 19): 'fish_brown',
        }
        
        closest_color = min(color_map.keys(),
                          key=lambda c: sum((a-b)**2 for a, b in zip(c, fish_color)))
        
        sprite_name = color_map[closest_color]
        return self.get_sprite(sprite_name)
    
    def get_ship_sprite(self, player_id):
        """Retorna navio por ID do jogador"""
        ship_names = ['ship (1)', 'ship (2)', 'ship (3)', 'ship (4)']
        ship_name = ship_names[player_id % len(ship_names)]
        return self.get_sprite(ship_name)
    
    def debug_sprites(self):
        """Lista sprites carregados"""
        print(f"Sprites carregados: {len(self.sprites)}")
        for nome in sorted(self.sprites.keys()):
            sprite = self.sprites[nome]
            print(f"  {nome}: {sprite.get_size()}")

# Instância global
sprite_manager = None

def get_sprite_manager():
    global sprite_manager
    if sprite_manager is None:
        sprite_manager = SpriteManager()
    return sprite_manager

def init_sprites():
    global sprite_manager
    sprite_manager = SpriteManager()
    return sprite_manager

