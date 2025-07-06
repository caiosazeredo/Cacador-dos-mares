# src/responsive_window.py - Sistema de janela responsiva

import pygame
from config import *

class ResponsiveWindow:
    """Sistema de janela responsiva com redimensionamento por arrastar"""
    
    def __init__(self):
        self.min_width = 1000
        self.min_height = 700
        self.max_width = 3840
        self.max_height = 2160
        self.current_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.is_resizing = False
        self.resize_edge = None
        self.resize_threshold = 10
        self.last_mouse_pos = (0, 0)
        
        # Bordas para redimensionamento
        self.resize_edges = {
            'right': False,
            'bottom': False,
            'bottom_right': False
        }
        
    def handle_event(self, event, screen):
        """Processa eventos de redimensionamento"""
        if event.type == pygame.VIDEORESIZE:
            return self.handle_resize(event.w, event.h)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo
                return self.start_resize(event.pos, screen)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                return self.stop_resize()
        
        elif event.type == pygame.MOUSEMOTION:
            if self.is_resizing:
                return self.update_resize(event.pos, screen)
            else:
                self.update_cursor(event.pos, screen)
        
        return None
    
    def handle_resize(self, new_width, new_height):
        """Processa redimensionamento da janela"""
        # Aplica limites
        new_width = max(self.min_width, min(self.max_width, new_width))
        new_height = max(self.min_height, min(self.max_height, new_height))
        
        # Atualiza tamanho atual
        self.current_size = (new_width, new_height)
        
        # Cria nova superfície
        flags = pygame.RESIZABLE | pygame.DOUBLEBUF
        new_screen = pygame.display.set_mode((new_width, new_height), flags)
        
        # Atualiza configurações globais
        from src.settings_manager import settings_manager
        settings_manager.current_resolution = (new_width, new_height)
        settings_manager.save_settings()
        
        return new_screen
    
    def start_resize(self, mouse_pos, screen):
        """Inicia redimensionamento se mouse estiver na borda"""
        screen_width, screen_height = screen.get_size()
        mouse_x, mouse_y = mouse_pos
        
        # Verifica se está nas bordas
        at_right = abs(mouse_x - screen_width) <= self.resize_threshold
        at_bottom = abs(mouse_y - screen_height) <= self.resize_threshold
        
        if at_right and at_bottom:
            self.resize_edge = 'bottom_right'
            self.is_resizing = True
        elif at_right:
            self.resize_edge = 'right'
            self.is_resizing = True
        elif at_bottom:
            self.resize_edge = 'bottom'
            self.is_resizing = True
        
        if self.is_resizing:
            self.last_mouse_pos = mouse_pos
            return True
        
        return False
    
    def stop_resize(self):
        """Para o redimensionamento"""
        if self.is_resizing:
            self.is_resizing = False
            self.resize_edge = None
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            return True
        return False
    
    def update_resize(self, mouse_pos, screen):
        """Atualiza redimensionamento durante o arraste"""
        if not self.is_resizing:
            return None
        
        mouse_x, mouse_y = mouse_pos
        last_x, last_y = self.last_mouse_pos
        
        # Calcula mudança
        delta_x = mouse_x - last_x
        delta_y = mouse_y - last_y
        
        current_width, current_height = screen.get_size()
        new_width = current_width
        new_height = current_height
        
        # Aplica mudança baseada na borda
        if self.resize_edge in ['right', 'bottom_right']:
            new_width = current_width + delta_x
        
        if self.resize_edge in ['bottom', 'bottom_right']:
            new_height = current_height + delta_y
        
        # Aplica limites
        new_width = max(self.min_width, min(self.max_width, new_width))
        new_height = max(self.min_height, min(self.max_height, new_height))
        
        # Atualiza apenas se mudou
        if (new_width, new_height) != (current_width, current_height):
            self.last_mouse_pos = mouse_pos
            return self.handle_resize(new_width, new_height)
        
        return None
    
    def update_cursor(self, mouse_pos, screen):
        """Atualiza cursor baseado na posição do mouse"""
        screen_width, screen_height = screen.get_size()
        mouse_x, mouse_y = mouse_pos
        
        # Verifica proximidade das bordas
        at_right = abs(mouse_x - screen_width) <= self.resize_threshold
        at_bottom = abs(mouse_y - screen_height) <= self.resize_threshold
        
        # Define cursor apropriado
        if at_right and at_bottom:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
        elif at_right:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
        elif at_bottom:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def draw_resize_indicators(self, surface):
        """Desenha indicadores visuais de redimensionamento"""
        if not self.is_resizing:
            return
        
        width, height = surface.get_size()
        
        # Desenha cantos de redimensionamento
        corner_size = 20
        corner_color = (100, 100, 100, 128)
        
        # Canto inferior direito
        corner_rect = pygame.Rect(
            width - corner_size, height - corner_size,
            corner_size, corner_size
        )
        
        corner_surface = pygame.Surface((corner_size, corner_size), pygame.SRCALPHA)
        corner_surface.set_alpha(128)
        corner_surface.fill(corner_color)
        surface.blit(corner_surface, corner_rect)
        
        # Linhas de redimensionamento
        for i in range(3):
            offset = i * 6 + 4
            start_pos = (width - corner_size + offset, height - 4)
            end_pos = (width - 4, height - corner_size + offset)
            pygame.draw.line(surface, (200, 200, 200), start_pos, end_pos, 2)
    
    def get_current_size(self):
        """Retorna tamanho atual da janela"""
        return self.current_size
    
    def set_minimum_size(self, width, height):
        """Define tamanho mínimo da janela"""
        self.min_width = width
        self.min_height = height

# Instância global
responsive_window = ResponsiveWindow()
