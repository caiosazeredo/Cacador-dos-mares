# src/fish.py - Classe dos peixes com sprites

import pygame
import random
import math
from config import *
from src.utils import board_to_screen, lerp

class Fish:
    """Classe que representa um peixe no jogo"""
    
    # Cores dos diferentes tipos de peixes
    FISH_TYPES = [
        {'color': (255, 165, 0), 'name': 'Dourado', 'sprite': 'fish_orange'},     # Laranja
        {'color': (255, 192, 203), 'name': 'Rosa', 'sprite': 'fish_pink'},       # Rosa
        {'color': (135, 206, 250), 'name': 'Azul', 'sprite': 'fish_blue'},       # Azul claro
        {'color': (152, 251, 152), 'name': 'Verde', 'sprite': 'fish_green'},     # Verde claro
        {'color': (128, 128, 128), 'name': 'Cinza', 'sprite': 'fish_grey'},      # Cinza
        {'color': (139, 69, 19), 'name': 'Marrom', 'sprite': 'fish_brown'},      # Marrom
    ]
    
    def __init__(self, x, y, fish_type=None):
        self.x = x
        self.y = y
        
        # Tipo de peixe
        if fish_type is None:
            self.type = random.choice(self.FISH_TYPES)
        else:
            self.type = self.FISH_TYPES[fish_type % len(self.FISH_TYPES)]
        
        # Visual
        self.size = 30  # Tamanho base para sprites
        self.color = self.type['color']
        self.sprite_name = self.type['sprite']
        
        # Animação
        self.animation_offset = random.uniform(0, math.pi * 2)
        self.animation_speed = random.uniform(2, 4)
        self.scale = 1.0
        
        # Movimento
        self.target_x = x
        self.target_y = y
        self.moving = False
        self.move_progress = 0
        self.move_speed = 3  # Velocidade da animação de movimento
        
        # Posição visual (para animação suave)
        self.visual_x = x
        self.visual_y = y
        
        # Sprite
        self.sprite = None
        self.load_sprite()
        
    def load_sprite(self):
        """Carrega o sprite do peixe"""
        try:
            from src.sprite_loader import get_sprite_manager
            sprite_manager = get_sprite_manager()
            self.sprite = sprite_manager.get_sprite(self.sprite_name)
            
            # Tenta variações do nome se não encontrar
            if not self.sprite:
                # Tenta sem a extensão
                base_name = self.sprite_name.replace('.png', '')
                self.sprite = sprite_manager.get_sprite(base_name)
                
            # Se ainda não encontrou, usa fallback
            if not self.sprite:
                print(f"Sprite não encontrado: {self.sprite_name}, usando fallback")
                # Cria um sprite simples como fallback
                self.sprite = self.create_fallback_sprite()
                
        except Exception as e:
            print(f"Erro ao carregar sprite do peixe: {e}")
            self.sprite = self.create_fallback_sprite()
    
    def create_fallback_sprite(self):
        """Cria um sprite simples como fallback"""
        size = 32
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Corpo do peixe
        body_rect = pygame.Rect(4, 8, size-12, size//2)
        pygame.draw.ellipse(surface, self.color, body_rect)
        pygame.draw.ellipse(surface, (0, 0, 0), body_rect, 1)
        
        # Cauda
        tail_points = [
            (4, size//2),
            (0, size//3),
            (0, 2*size//3)
        ]
        pygame.draw.polygon(surface, self.color, tail_points)
        pygame.draw.polygon(surface, (0, 0, 0), tail_points, 1)
        
        # Olho
        eye_center = (size-8, size//2-2)
        pygame.draw.circle(surface, (255, 255, 255), eye_center, 3)
        pygame.draw.circle(surface, (0, 0, 0), eye_center, 2)
        
        return surface
        
    def set_target_position(self, x, y):
        """Define a posição alvo para movimento"""
        self.target_x = x
        self.target_y = y
        self.moving = True
        self.move_progress = 0
        
    def update(self, dt):
        """Atualiza o peixe"""
        # Animação de balanço
        self.animation_offset += self.animation_speed * dt
        
        # Movimento suave
        if self.moving:
            self.move_progress += self.move_speed * dt
            
            if self.move_progress >= 1.0:
                # Movimento completo
                self.x = self.target_x
                self.y = self.target_y
                self.visual_x = self.x
                self.visual_y = self.y
                self.moving = False
                self.move_progress = 1.0
            else:
                # Interpolação
                self.visual_x = lerp(self.x, self.target_x, self.move_progress)
                self.visual_y = lerp(self.y, self.target_y, self.move_progress)
    
    def get_position(self):
        """Retorna a posição lógica do peixe"""
        return (self.x, self.y)
    
    def draw(self, screen):
        """Desenha o peixe"""
        # Posição na tela
        screen_x, screen_y = board_to_screen(self.visual_x, self.visual_y)
        
        # Efeito de balanço
        wobble = math.sin(self.animation_offset) * 2
        screen_y += wobble
        
        # Escala com animação
        if self.moving:
            # Efeito de "pulo" durante movimento
            jump_scale = 1.0 + 0.2 * math.sin(self.move_progress * math.pi)
            current_scale = self.scale * jump_scale
        else:
            current_scale = self.scale
        
        if self.sprite:
            # Desenha usando sprite
            sprite_rect = self.sprite.get_rect()
            
            # Aplica escala se necessário
            if current_scale != 1.0:
                new_size = (int(sprite_rect.width * current_scale), 
                           int(sprite_rect.height * current_scale))
                scaled_sprite = pygame.transform.scale(self.sprite, new_size)
                sprite_rect = scaled_sprite.get_rect()
                sprite_rect.center = (screen_x, screen_y)
                screen.blit(scaled_sprite, sprite_rect)
            else:
                sprite_rect.center = (screen_x, screen_y)
                screen.blit(self.sprite, sprite_rect)
        else:
            # Fallback para desenho manual se não tiver sprite
            self.draw_manual(screen, screen_x, screen_y, current_scale)
    
    def draw_manual(self, screen, screen_x, screen_y, current_scale):
        """Desenha o peixe manualmente como fallback"""
        fish_size = int(self.size * current_scale)
        
        # Corpo principal (elipse)
        body_rect = pygame.Rect(0, 0, fish_size, int(fish_size * 0.6))
        body_rect.center = (screen_x, screen_y)
        pygame.draw.ellipse(screen, self.color, body_rect)
        pygame.draw.ellipse(screen, COLORS['BLACK'], body_rect, 1)
        
        # Cauda
        tail_size = int(fish_size * 0.4)
        tail_points = [
            (screen_x - fish_size // 2, screen_y),
            (screen_x - fish_size // 2 - tail_size, screen_y - tail_size // 2),
            (screen_x - fish_size // 2 - tail_size, screen_y + tail_size // 2)
        ]
        pygame.draw.polygon(screen, self.color, tail_points)
        pygame.draw.polygon(screen, COLORS['BLACK'], tail_points, 1)
        
        # Olho
        eye_x = screen_x + fish_size // 4
        eye_y = screen_y - 2
        pygame.draw.circle(screen, COLORS['WHITE'], (eye_x, eye_y), 3)
        pygame.draw.circle(screen, COLORS['BLACK'], (eye_x, eye_y), 2)
        
        # Barbatana
        fin_points = [
            (screen_x, screen_y - fish_size // 3),
            (screen_x - fish_size // 6, screen_y - fish_size // 2),
            (screen_x + fish_size // 6, screen_y - fish_size // 2)
        ]
        pygame.draw.polygon(screen, self.color, fin_points)
        pygame.draw.polygon(screen, COLORS['BLACK'], fin_points, 1)
    
    def __repr__(self):
        return f"Fish({self.x}, {self.y}, {self.type['name']})"