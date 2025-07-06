# src/board.py - Tabuleiro responsivo (CORRIGIDO)

import pygame
import math
from config import *
from src.tile_manager import TileManager
from src.layout_manager import layout_manager

class Board:
    """Tabuleiro do jogo com layout responsivo"""
    
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        
        # Sistema de destaque
        self.highlight_cells = []
        self.wave_offset = 0
        
        # Gerenciador de tiles
        self.tile_manager = TileManager()
        
        print(f"Tabuleiro criado: {size}x{size} (responsivo)")
    
    def update(self, dt):
        """Atualiza animações do tabuleiro"""
        self.wave_offset += dt * 100
    
    def update_screen_size(self, width, height):
        """Atualiza tamanho da tela"""
        layout_manager.update_screen_size(width, height)
    
    def is_valid_position(self, x, y):
        """Verifica se a posição é válida"""
        return 0 <= x < self.size and 0 <= y < self.size
    
    def is_occupied(self, x, y):
        """Verifica se a posição está ocupada"""
        if not self.is_valid_position(x, y):
            return True
        return self.grid[y][x] is not None
    
    def place_object(self, x, y, obj):
        """Coloca um objeto no tabuleiro"""
        if self.is_valid_position(x, y):
            self.grid[y][x] = obj
            return True
        return False
    
    def remove_object(self, x, y):
        """Remove um objeto do tabuleiro"""
        if self.is_valid_position(x, y):
            obj = self.grid[y][x]
            self.grid[y][x] = None
            return obj
        return None
    
    def get_object(self, x, y):
        """Retorna o objeto em uma posição"""
        if self.is_valid_position(x, y):
            return self.grid[y][x]
        return None
    
    def move_object(self, from_x, from_y, to_x, to_y):
        """Move um objeto de uma posição para outra"""
        if self.is_valid_position(from_x, from_y) and self.is_valid_position(to_x, to_y):
            obj = self.grid[from_y][from_x]
            self.grid[from_y][from_x] = None
            self.grid[to_y][to_x] = obj
            return True
        return False
    
    def get_valid_moves(self, x, y, max_distance):
        """Retorna movimentos válidos a partir de uma posição"""
        valid_moves = []
        
        for dx in range(-max_distance, max_distance + 1):
            for dy in range(-max_distance, max_distance + 1):
                if dx == 0 and dy == 0:
                    continue
                    
                new_x, new_y = x + dx, y + dy
                
                if abs(dx) + abs(dy) <= max_distance:
                    if self.is_valid_position(new_x, new_y) and not self.is_occupied(new_x, new_y):
                        valid_moves.append((new_x, new_y))
        
        return valid_moves
    
    def highlight_moves(self, moves):
        """Destaca células válidas para movimento"""
        self.highlight_cells = moves
        
    def clear_highlights(self):
        """Limpa células destacadas"""
        self.highlight_cells = []
    
    def screen_to_board(self, screen_x, screen_y):
        """Converte coordenadas da tela para coordenadas do tabuleiro"""
        return layout_manager.get_screen_to_board_coordinates(screen_x, screen_y)
    
    def board_to_screen(self, board_x, board_y):
        """Converte coordenadas do tabuleiro para coordenadas da tela"""
        return layout_manager.get_scaled_board_coordinates(board_x, board_y)
    
    def draw(self, surface):
        """Desenha o tabuleiro responsivo"""
        # Atualiza tamanho da tela
        screen_width, screen_height = surface.get_size()
        layout_manager.update_screen_size(screen_width, screen_height)
        
        # Desenha tiles de água como fundo
        self.draw_water_tiles(surface)
        
        # Desenha grade responsiva
        layout_manager.draw_board_grid(surface)
        
        # Desenha highlights
        self.draw_highlights(surface)
        
        # Desenha coordenadas responsivas
        layout_manager.draw_coordinates(surface)
    
    def draw_water_tiles(self, surface):
        """Desenha tiles de água responsivos"""
        water_tile = self.tile_manager.get_water_tile()
        board_area = layout_manager.get_board_area()
        
        if not water_tile:
            # Fallback para cor sólida
            board_rect = pygame.Rect(board_area['x'], board_area['y'], 
                                   board_area['width'], board_area['height'])
            pygame.draw.rect(surface, COLORS['BOARD'], board_rect)
            return
        
        # Escala o tile para o tamanho da célula
        cell_size = board_area['cell_size']
        if water_tile.get_size() != (cell_size, cell_size):
            water_tile = pygame.transform.scale(water_tile, (cell_size, cell_size))
        
        # Desenha tiles de água
        for row in range(self.size):
            for col in range(self.size):
                x = board_area['x'] + col * cell_size
                y = board_area['y'] + row * cell_size
                surface.blit(water_tile, (x, y))
    
    def draw_highlights(self, surface):
        """Desenha células destacadas responsivas"""
        board_area = layout_manager.get_board_area()
        cell_size = board_area['cell_size']
        
        for cell_x, cell_y in self.highlight_cells:
            x = board_area['x'] + cell_x * cell_size
            y = board_area['y'] + cell_y * cell_size
            
            rect = pygame.Rect(x, y, cell_size, cell_size)
            
            # Efeito de onda
            alpha = 100 + int(50 * math.sin(self.wave_offset * 0.01))
            highlight_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            highlight_surface.set_alpha(alpha)
            highlight_surface.fill(COLORS['GREEN'])
            surface.blit(highlight_surface, rect)
            
            # Borda
            pygame.draw.rect(surface, COLORS['GREEN'], rect, 2)
    
    def get_all_occupied_positions(self):
        """Retorna todas as posições ocupadas"""
        occupied = []
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] is not None:
                    occupied.append((x, y))
        return occupied
