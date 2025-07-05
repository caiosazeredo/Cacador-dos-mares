# src/board.py - Classe do tabuleiro

import pygame
import math
from config import *
from src.utils import board_to_screen, draw_text

class Board:
    def __init__(self):
        self.size = BOARD_SIZE
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        
        # Visual
        self.cell_size = CELL_SIZE
        self.offset_x = BOARD_OFFSET_X
        self.offset_y = BOARD_OFFSET_Y
        
        # Animações
        self.wave_offset = 0
        self.highlight_cells = []  # Células destacadas para movimento
        
    def update(self, dt):
        """Atualiza animações do tabuleiro"""
        self.wave_offset += dt * 100
        
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
            
    def remove_object(self, x, y):
        """Remove um objeto do tabuleiro"""
        if self.is_valid_position(x, y):
            self.grid[y][x] = None
            
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
                
                # Verifica se está dentro do limite de movimento (Manhattan)
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
    
    def draw(self, screen):
        """Desenha o tabuleiro"""
        # Fundo do mar
        board_rect = pygame.Rect(self.offset_x, self.offset_y, 
                               self.size * self.cell_size, 
                               self.size * self.cell_size)
        pygame.draw.rect(screen, COLORS['BOARD'], board_rect)
        
        # Grade
        for i in range(self.size + 1):
            # Linhas horizontais
            y = self.offset_y + i * self.cell_size
            pygame.draw.line(screen, COLORS['GRID'], 
                           (self.offset_x, y), 
                           (self.offset_x + self.size * self.cell_size, y), 1)
            
            # Linhas verticais
            x = self.offset_x + i * self.cell_size
            pygame.draw.line(screen, COLORS['GRID'], 
                           (x, self.offset_y), 
                           (x, self.offset_y + self.size * self.cell_size), 1)
        
        # Destaca células válidas para movimento
        for cell_x, cell_y in self.highlight_cells:
            rect = pygame.Rect(
                self.offset_x + cell_x * self.cell_size,
                self.offset_y + cell_y * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            
            # Efeito de onda
            alpha = 100 + int(50 * math.sin(self.wave_offset * 0.01))
            highlight_surface = pygame.Surface((self.cell_size, self.cell_size))
            highlight_surface.set_alpha(alpha)
            highlight_surface.fill(COLORS['GREEN'])
            screen.blit(highlight_surface, rect)
            
            # Borda
            pygame.draw.rect(screen, COLORS['GREEN'], rect, 2)
        
        # Coordenadas
        font_size = 14
        
        # Números nas laterais (linhas)
        for i in range(self.size):
            # Esquerda
            draw_text(screen, str(i + 1), 
                     self.offset_x - 25, 
                     self.offset_y + i * self.cell_size + self.cell_size // 2 - 7,
                     size=font_size, color=COLORS['WHITE'])
            
            # Direita
            draw_text(screen, str(i + 1), 
                     self.offset_x + self.size * self.cell_size + 10,
                     self.offset_y + i * self.cell_size + self.cell_size // 2 - 7,
                     size=font_size, color=COLORS['WHITE'])
        
        # Letras em cima e embaixo (colunas)
        for i in range(self.size):
            letter = chr(ord('A') + i)
            
            # Cima
            draw_text(screen, letter,
                     self.offset_x + i * self.cell_size + self.cell_size // 2 - 5,
                     self.offset_y - 25,
                     size=font_size, color=COLORS['WHITE'])
            
            # Baixo
            draw_text(screen, letter,
                     self.offset_x + i * self.cell_size + self.cell_size // 2 - 5,
                     self.offset_y + self.size * self.cell_size + 10,
                     size=font_size, color=COLORS['WHITE'])
    
    def get_all_occupied_positions(self):
        """Retorna todas as posições ocupadas"""
        occupied = []
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] is not None:
                    occupied.append((x, y))
        return occupied