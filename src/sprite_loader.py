# src/sprite_loader.py - Sistema de carregamento de sprites

import pygame
import xml.etree.ElementTree as ET
import os
from config import *

class SpriteSheet:
    """Classe para carregar e gerenciar spritesheets"""
    
    def __init__(self, image_path, xml_path):
        self.image = None
        self.sprites = {}
        
        # Carrega a imagem
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
        else:
            print(f"Aviso: Imagem não encontrada: {image_path}")
            return
            
        # Carrega o XML
        if os.path.exists(xml_path):
            self.load_xml(xml_path)
        else:
            print(f"Aviso: XML não encontrado: {xml_path}")
    
    def load_xml(self, xml_path):
        """Carrega as coordenadas dos sprites do XML"""
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            for subtexture in root.findall('SubTexture'):
                name = subtexture.get('name')
                x = int(subtexture.get('x'))
                y = int(subtexture.get('y'))
                width = int(subtexture.get('width'))
                height = int(subtexture.get('height'))
                
                # Extrai o sprite da imagem
                sprite_rect = pygame.Rect(x, y, width, height)
                sprite_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                sprite_surface.blit(self.image, (0, 0), sprite_rect)
                
                self.sprites[name] = sprite_surface
                
        except Exception as e:
            print(f"Erro ao carregar XML {xml_path}: {e}")
    
    def get_sprite(self, name):
        """Retorna um sprite pelo nome"""
        return self.sprites.get(name)
    
    def has_sprite(self, name):
        """Verifica se o sprite existe"""
        return name in self.sprites

class SpriteManager:
    """Gerenciador global de sprites"""
    
    def __init__(self):
        self.sheets = {}
        self.load_all_sprites()
    
    def load_all_sprites(self):
        """Carrega todos os spritesheets"""
        # Carrega spritesheet principal
        main_sheet_path = os.path.join(IMAGES_PATH, 'spritesheet.png')
        main_xml_path = os.path.join(IMAGES_PATH, 'spritesheet.xml')
        
        if os.path.exists(main_sheet_path) and os.path.exists(main_xml_path):
            self.sheets['main'] = SpriteSheet(main_sheet_path, main_xml_path)
        else:
            # Tenta localizar os arquivos na raiz
            main_sheet_path = 'spritesheet.png'
            main_xml_path = 'spritesheet.xml'
            if os.path.exists(main_sheet_path) and os.path.exists(main_xml_path):
                self.sheets['main'] = SpriteSheet(main_sheet_path, main_xml_path)
        
        # Carrega spritesheet duplo se existir
        double_sheet_path = os.path.join(IMAGES_PATH, 'spritesheet-double.png')
        double_xml_path = os.path.join(IMAGES_PATH, 'spritesheet-double.xml')
        
        if os.path.exists(double_sheet_path) and os.path.exists(double_xml_path):
            self.sheets['double'] = SpriteSheet(double_sheet_path, double_xml_path)
        else:
            # Tenta localizar os arquivos na raiz
            double_sheet_path = 'spritesheet-double.png'
            double_xml_path = 'spritesheet-double.xml'
            if os.path.exists(double_sheet_path) and os.path.exists(double_xml_path):
                self.sheets['double'] = SpriteSheet(double_sheet_path, double_xml_path)
        
        # Carrega sprites de navios se existir
        ships_sheet_path = os.path.join(IMAGES_PATH, 'shipsMiscellaneous_sheet.png')
        ships_xml_path = os.path.join(IMAGES_PATH, 'shipsMiscellaneous_sheet.xml')
        
        if os.path.exists(ships_sheet_path) and os.path.exists(ships_xml_path):
            self.sheets['ships'] = SpriteSheet(ships_sheet_path, ships_xml_path)
        
        print("Sprites carregados:")
        for sheet_name, sheet in self.sheets.items():
            if sheet.image:
                print(f"  {sheet_name}: {len(sheet.sprites)} sprites")
    
    def get_sprite(self, sprite_name, sheet_name='main'):
        """Retorna um sprite específico"""
        if sheet_name in self.sheets:
            return self.sheets[sheet_name].get_sprite(sprite_name)
        return None
    
    def get_fish_sprite(self, fish_color):
        """Retorna um sprite de peixe baseado na cor"""
        color_map = {
            (255, 165, 0): 'fish_orange',      # Laranja
            (255, 192, 203): 'fish_pink',      # Rosa
            (147, 112, 219): 'fish_blue',      # Roxo -> Azul
            (135, 206, 250): 'fish_blue',      # Azul claro
            (152, 251, 152): 'fish_green',     # Verde claro
            (255, 255, 0): 'fish_brown',       # Amarelo -> Marrom
        }
        
        # Encontra a cor mais próxima
        closest_color = min(color_map.keys(), 
                          key=lambda c: sum((a-b)**2 for a, b in zip(c, fish_color)))
        
        sprite_name = color_map[closest_color]
        return self.get_sprite(sprite_name)
    
    def get_ship_sprite(self, player_id):
        """Retorna um sprite de navio baseado no ID do jogador"""
        ship_sprites = [
            'ship (1).png',
            'ship (2).png', 
            'ship (3).png',
            'ship (4).png'
        ]
        
        ship_name = ship_sprites[player_id % len(ship_sprites)]
        sprite = self.get_sprite(ship_name, 'ships')
        
        if sprite:
            return sprite
        
        # Fallback para sprites principais se não encontrar nos navios
        return self.get_sprite('hullSmall (1).png')

# Instância global do gerenciador de sprites
sprite_manager = None

def get_sprite_manager():
    """Retorna a instância global do gerenciador de sprites"""
    global sprite_manager
    if sprite_manager is None:
        sprite_manager = SpriteManager()
    return sprite_manager

def init_sprites():
    """Inicializa o sistema de sprites"""
    global sprite_manager
    sprite_manager = SpriteManager()
    return sprite_manager