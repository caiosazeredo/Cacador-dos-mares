# src/fish.py - Peixes responsivos

import pygame
import random
import math
from config import *
from src.layout_manager import layout_manager

class Fish:
    """Peixe com posicionamento responsivo"""
    
    def __init__(self, x, y, fish_type='blue'):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.visual_x = float(x)
        self.visual_y = float(y)
        self.fish_type = fish_type
        
        # Animação
        self.is_moving = False
        self.move_progress = 0
        self.move_speed = 2.0
        self.bob_offset = random.uniform(0, math.pi * 2)
        self.bob_speed = 3.0
        
        # Sprite
        self.sprite = None
        self.load_sprite()
    
    def load_sprite(self):
        """Carrega sprite do peixe"""
        try:
            from src.sprite_loader import get_sprite_manager
            sprite_manager = get_sprite_manager()
            if sprite_manager:
                sprite_name = f"fish_{self.fish_type}"
                self.sprite = sprite_manager.get_sprite(sprite_name)
        except Exception as e:
            print(f"Erro ao carregar sprite do peixe: {e}")
            self.sprite = None
    
    def set_target_position(self, x, y):
        """Define posição alvo para movimento"""
        self.target_x = x
        self.target_y = y
        self.is_moving = True
        self.move_progress = 0
    
    def get_position(self):
        """Retorna posição atual do peixe"""
        return (self.x, self.y)
    
    def get_screen_position(self):
        """Retorna posição na tela com layout responsivo"""
        return layout_manager.get_scaled_board_coordinates(
            int(self.visual_x), int(self.visual_y)
        )
    
    def update(self, dt):
        """Atualiza animações do peixe"""
        # Animação de balanço
        self.bob_offset += self.bob_speed * dt
        
        # Movimento suave
        if self.is_moving:
            self.move_progress += self.move_speed * dt
            
            if self.move_progress >= 1.0:
                # Movimento completo
                self.x = self.target_x
                self.y = self.target_y
                self.visual_x = float(self.x)
                self.visual_y = float(self.y)
                self.is_moving = False
                self.move_progress = 1.0
            else:
                # Interpolação suave
                self.visual_x = self.x + (self.target_x - self.x) * self.move_progress
                self.visual_y = self.y + (self.target_y - self.y) * self.move_progress
    
    def draw(self, surface):
        """Desenha o peixe na tela com posicionamento responsivo"""
        screen_x, screen_y = self.get_screen_position()
        
        # Efeito de balanço
        wobble_x = math.sin(self.bob_offset) * 2
        wobble_y = math.cos(self.bob_offset * 1.3) * 1
        
        final_x = screen_x + wobble_x
        final_y = screen_y + wobble_y
        
        if self.sprite:
            # Escala sprite baseado no tamanho da célula
            sprite_size = layout_manager.get_sprite_size(64)
            
            if self.sprite.get_size() != (sprite_size, sprite_size):
                scaled_sprite = pygame.transform.scale(self.sprite, (sprite_size, sprite_size))
            else:
                scaled_sprite = self.sprite
            
            sprite_rect = scaled_sprite.get_rect()
            sprite_rect.center = (int(final_x), int(final_y))
            
            surface.blit(scaled_sprite, sprite_rect)
        else:
            # Fallback para desenho manual
            self.draw_manual(surface, final_x, final_y)
    
    def draw_manual(self, surface, x, y):
        """Desenha peixe manualmente como fallback"""
        size = layout_manager.get_sprite_size(32)
        
        # Cores dos peixes
        colors = {
            'blue': (0, 100, 255),
            'orange': (255, 165, 0),
            'green': (0, 255, 100),
            'pink': (255, 100, 150),
            'brown': (139, 69, 19),
            'grey': (128, 128, 128)
        }
        
        fish_color = colors.get(self.fish_type, (100, 100, 100))
        
        # Corpo do peixe
        body_rect = pygame.Rect(int(x - size//2), int(y - size//4), size, size//2)
        pygame.draw.ellipse(surface, fish_color, body_rect)
        pygame.draw.ellipse(surface, COLORS['BLACK'], body_rect, 2)
        
        # Cauda
        tail_points = [
            (int(x - size//2), int(y)),
            (int(x - size), int(y - size//4)),
            (int(x - size), int(y + size//4))
        ]
        pygame.draw.polygon(surface, fish_color, tail_points)
        pygame.draw.polygon(surface, COLORS['BLACK'], tail_points, 2)
        
        # Olho
        eye_x = int(x + size//4)
        eye_y = int(y - size//8)
        pygame.draw.circle(surface, COLORS['WHITE'], (eye_x, eye_y), size//8)
        pygame.draw.circle(surface, COLORS['BLACK'], (eye_x, eye_y), size//12)

class FishManager:
    """Gerenciador de peixes responsivo"""
    
    def __init__(self):
        self.fish_list = []
        self.fish_types = ['blue', 'orange', 'green', 'pink', 'brown', 'grey']
    
    def add_fish(self, x, y, fish_type=None):
        """Adiciona um peixe na posição especificada"""
        if fish_type is None:
            fish_type = random.choice(self.fish_types)
        
        fish = Fish(x, y, fish_type)
        self.fish_list.append(fish)
        return fish
    
    def remove_fish(self, fish):
        """Remove um peixe"""
        if fish in self.fish_list:
            self.fish_list.remove(fish)
    
    def get_fish_at(self, x, y):
        """Retorna peixe na posição especificada"""
        for fish in self.fish_list:
            fish_x, fish_y = fish.get_position()
            if fish_x == x and fish_y == y:
                return fish
        return None
    
    def move_all_fish(self, vector):
        """Move todos os peixes pelo vetor especificado"""
        for fish in self.fish_list[:]:  # Cópia da lista
            current_x, current_y = fish.get_position()
            new_x = current_x + vector[0]
            new_y = current_y + vector[1]
            
            # Remove peixes que saem do tabuleiro
            if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
                self.remove_fish(fish)
            else:
                fish.set_target_position(new_x, new_y)
    
    def update(self, dt):
        """Atualiza todos os peixes"""
        for fish in self.fish_list:
            fish.update(dt)
    
    def draw(self, surface):
        """Desenha todos os peixes"""
        for fish in self.fish_list:
            fish.draw(surface)
    
    def get_all_positions(self):
        """Retorna posições de todos os peixes"""
        return [fish.get_position() for fish in self.fish_list]

# Instância global
fish_manager = FishManager()
