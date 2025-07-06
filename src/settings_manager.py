# src/settings_manager.py - Gerenciador de configurações avançadas

import pygame
import json
import os
from config import *

class SettingsManager:
    """Gerenciador de configurações do jogo"""
    
    def __init__(self):
        self.settings_file = os.path.join(DATA_PATH, 'settings.json')
        self.current_resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.current_screen = None
        self.fullscreen = False
        self.vsync = True
        self.sound_volume = 100
        self.music_volume = 80
        self.ui_scale = 1.0
        self.auto_login = True
        self.steam_username = "Jogador"
        
        # Resoluções suportadas
        self.resolutions = [
            (1280, 720),   # HD
            (1366, 768),   # HD+
            (1600, 900),   # HD+
            (1920, 1080),  # Full HD
            (2560, 1440),  # QHD
            (3840, 2160)   # 4K
        ]
        
        self.load_settings()
        
    def load_settings(self):
        """Carrega configurações do arquivo"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.current_resolution = tuple(data.get('resolution', (WINDOW_WIDTH, WINDOW_HEIGHT)))
                self.fullscreen = data.get('fullscreen', False)
                self.vsync = data.get('vsync', True)
                self.sound_volume = data.get('sound_volume', 100)
                self.music_volume = data.get('music_volume', 80)
                self.ui_scale = data.get('ui_scale', 1.0)
                self.auto_login = data.get('auto_login', True)
                self.steam_username = data.get('steam_username', "Jogador")
                
                print(f"✓ Configurações carregadas: {self.current_resolution}")
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            self.save_settings()
    
    def save_settings(self):
        """Salva configurações no arquivo"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            data = {
                'resolution': self.current_resolution,
                'fullscreen': self.fullscreen,
                'vsync': self.vsync,
                'sound_volume': self.sound_volume,
                'music_volume': self.music_volume,
                'ui_scale': self.ui_scale,
                'auto_login': self.auto_login,
                'steam_username': self.steam_username
            }
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            print("✓ Configurações salvas")
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
    
    def apply_resolution(self):
        """Aplica a resolução atual"""
        flags = pygame.DOUBLEBUF
        if self.vsync:
            flags |= pygame.HWSURFACE
        
        if self.fullscreen:
            flags |= pygame.FULLSCREEN
            # Use resolução nativa em tela cheia
            info = pygame.display.Info()
            resolution = (info.current_w, info.current_h)
        else:
            resolution = self.current_resolution
        
        try:
            new_screen = pygame.display.set_mode(resolution, flags)
            self.current_screen = new_screen
            print(f"✓ Resolução aplicada: {resolution}, Tela cheia: {self.fullscreen}")
            return new_screen
        except Exception as e:
            print(f"Erro ao aplicar resolução: {e}")
            # Fallback para resolução segura
            safe_resolution = (1280, 720)
            self.current_resolution = safe_resolution
            self.fullscreen = False
            new_screen = pygame.display.set_mode(safe_resolution)
            self.current_screen = new_screen
            return new_screen
    
    def toggle_fullscreen(self):
        """Alterna entre tela cheia e janela"""
        self.fullscreen = not self.fullscreen
        screen = self.apply_resolution()
        self.save_settings()
        return screen
    
    def set_resolution(self, width, height):
        """Define nova resolução"""
        self.current_resolution = (width, height)
        if not self.fullscreen:
            screen = self.apply_resolution()
        self.save_settings()
        return self.current_screen
    
    def get_ui_scale_factor(self):
        """Retorna fator de escala para UI responsiva"""
        base_width = 1600  # Resolução base do design
        current_width = self.current_resolution[0] if not self.fullscreen else pygame.display.Info().current_w
        auto_scale = current_width / base_width
        return auto_scale * self.ui_scale
    
    def scale_size(self, size):
        """Escala um tamanho baseado na resolução atual"""
        factor = self.get_ui_scale_factor()
        if isinstance(size, tuple):
            return (int(size[0] * factor), int(size[1] * factor))
        return int(size * factor)
    
    def scale_pos(self, pos):
        """Escala uma posição baseada na resolução atual"""
        factor = self.get_ui_scale_factor()
        return (int(pos[0] * factor), int(pos[1] * factor))
    
    def get_scaled_font_size(self, base_size):
        """Retorna tamanho de fonte escalado"""
        return max(12, int(base_size * self.get_ui_scale_factor()))

# Instância global
settings_manager = SettingsManager()
