# src/layout_manager.py - Sistema de layout responsivo

import pygame
from config import *

class LayoutManager:
    """Gerenciador de layout responsivo para o Caçador dos Mares"""
    
    def __init__(self):
        self.screen_width = WINDOW_WIDTH
        self.screen_height = WINDOW_HEIGHT
        self.margin_ratio = 0.05  # 5% de margem
        self.board_ratio = 0.7    # 70% da tela para o tabuleiro
        self.ui_ratio = 0.25      # 25% para UI lateral
        
        # Cache de layouts calculados
        self.layout_cache = {}
        self.last_screen_size = (0, 0)
        
    def update_screen_size(self, width, height):
        """Atualiza tamanho da tela e recalcula layout"""
        if (width, height) != self.last_screen_size:
            self.screen_width = width
            self.screen_height = height
            self.last_screen_size = (width, height)
            self.layout_cache.clear()  # Limpa cache quando tela muda
    
    def get_margins(self):
        """Retorna margens baseadas no tamanho da tela"""
        margin_x = int(self.screen_width * self.margin_ratio)
        margin_y = int(self.screen_height * self.margin_ratio)
        
        # Margens mínimas e máximas
        margin_x = max(20, min(80, margin_x))
        margin_y = max(20, min(60, margin_y))
        
        return margin_x, margin_y
    
    def get_board_area(self):
        """Retorna área disponível para o tabuleiro"""
        margin_x, margin_y = self.get_margins()
        
        # Área disponível após margens
        available_width = self.screen_width - (margin_x * 2)
        available_height = self.screen_height - (margin_y * 2)
        
        # Reserva espaço para UI lateral
        board_width = int(available_width * self.board_ratio)
        board_height = available_height
        
        # Mantém proporção quadrada se possível
        board_size = min(board_width, board_height)
        
        # Posição central do tabuleiro
        board_x = margin_x + (board_width - board_size) // 2
        board_y = margin_y + (board_height - board_size) // 2
        
        return {
            'x': board_x,
            'y': board_y,
            'width': board_size,
            'height': board_size,
            'cell_size': board_size // BOARD_SIZE
        }
    
    def get_ui_area(self):
        """Retorna área para interface do usuário"""
        margin_x, margin_y = self.get_margins()
        board_area = self.get_board_area()
        
        ui_x = board_area['x'] + board_area['width'] + margin_x
        ui_y = margin_y
        ui_width = self.screen_width - ui_x - margin_x
        ui_height = self.screen_height - (margin_y * 2)
        
        return {
            'x': ui_x,
            'y': ui_y,
            'width': ui_width,
            'height': ui_height
        }
    
    def get_scaled_board_coordinates(self, board_x, board_y):
        """Converte coordenadas do tabuleiro para coordenadas da tela"""
        cache_key = f"board_coord_{board_x}_{board_y}"
        if cache_key in self.layout_cache:
            return self.layout_cache[cache_key]
        
        board_area = self.get_board_area()
        
        screen_x = board_area['x'] + (board_x * board_area['cell_size']) + (board_area['cell_size'] // 2)
        screen_y = board_area['y'] + (board_y * board_area['cell_size']) + (board_area['cell_size'] // 2)
        
        result = (screen_x, screen_y)
        self.layout_cache[cache_key] = result
        return result
    
    def get_screen_to_board_coordinates(self, screen_x, screen_y):
        """Converte coordenadas da tela para coordenadas do tabuleiro"""
        board_area = self.get_board_area()
        
        # Verifica se está dentro da área do tabuleiro
        if (screen_x < board_area['x'] or screen_x > board_area['x'] + board_area['width'] or
            screen_y < board_area['y'] or screen_y > board_area['y'] + board_area['height']):
            return None
        
        board_x = (screen_x - board_area['x']) // board_area['cell_size']
        board_y = (screen_y - board_area['y']) // board_area['cell_size']
        
        # Verifica limites
        if 0 <= board_x < BOARD_SIZE and 0 <= board_y < BOARD_SIZE:
            return (board_x, board_y)
        
        return None
    
    def get_element_scale_factor(self):
        """Retorna fator de escala para elementos baseado no tamanho da tela"""
        # Escala baseada na área do tabuleiro
        board_area = self.get_board_area()
        base_size = 1280  # Tamanho base de referência
        current_size = min(self.screen_width, self.screen_height)
        
        scale = current_size / base_size
        return max(0.5, min(2.0, scale))  # Limita entre 50% e 200%
    
    def get_font_size(self, base_size):
        """Retorna tamanho de fonte escalado"""
        scale = self.get_element_scale_factor()
        return max(12, int(base_size * scale))
    
    def get_sprite_size(self, base_size):
        """Retorna tamanho de sprite escalado"""
        board_area = self.get_board_area()
        sprite_size = int(board_area['cell_size'] * 0.8)  # 80% do tamanho da célula
        return max(16, min(128, sprite_size))
    
    def draw_board_grid(self, surface):
        """Desenha grade do tabuleiro responsiva"""
        board_area = self.get_board_area()
        
        # Cor da grade baseada no contraste
        grid_color = (45, 125, 184)
        
        # Linhas verticais
        for i in range(BOARD_SIZE + 1):
            x = board_area['x'] + (i * board_area['cell_size'])
            start_pos = (x, board_area['y'])
            end_pos = (x, board_area['y'] + board_area['height'])
            pygame.draw.line(surface, grid_color, start_pos, end_pos, 1)
        
        # Linhas horizontais
        for i in range(BOARD_SIZE + 1):
            y = board_area['y'] + (i * board_area['cell_size'])
            start_pos = (board_area['x'], y)
            end_pos = (board_area['x'] + board_area['width'], y)
            pygame.draw.line(surface, grid_color, start_pos, end_pos, 1)
    
    def draw_coordinates(self, surface):
        """Desenha coordenadas do tabuleiro"""
        board_area = self.get_board_area()
        font_size = self.get_font_size(16)
        font = pygame.font.Font(None, font_size)
        
        # Números nas laterais (linhas)
        for i in range(BOARD_SIZE):
            text = str(i + 1)
            text_surface = font.render(text, True, COLORS['WHITE'])
            text_rect = text_surface.get_rect()
            
            # Esquerda
            text_rect.centery = board_area['y'] + (i * board_area['cell_size']) + (board_area['cell_size'] // 2)
            text_rect.right = board_area['x'] - 10
            surface.blit(text_surface, text_rect)
            
            # Direita
            text_rect.left = board_area['x'] + board_area['width'] + 10
            surface.blit(text_surface, text_rect)
        
        # Letras em cima e embaixo (colunas)
        for i in range(BOARD_SIZE):
            letter = chr(ord('A') + i)
            text_surface = font.render(letter, True, COLORS['WHITE'])
            text_rect = text_surface.get_rect()
            
            text_rect.centerx = board_area['x'] + (i * board_area['cell_size']) + (board_area['cell_size'] // 2)
            
            # Cima
            text_rect.bottom = board_area['y'] - 10
            surface.blit(text_surface, text_rect)
            
            # Baixo
            text_rect.top = board_area['y'] + board_area['height'] + 10
            surface.blit(text_surface, text_rect)
    
    def get_debug_info(self):
        """Retorna informações de debug do layout"""
        board_area = self.get_board_area()
        ui_area = self.get_ui_area()
        margins = self.get_margins()
        
        return {
            'screen_size': (self.screen_width, self.screen_height),
            'margins': margins,
            'board_area': board_area,
            'ui_area': ui_area,
            'scale_factor': self.get_element_scale_factor(),
            'cache_size': len(self.layout_cache)
        }

# Instância global
layout_manager = LayoutManager()
