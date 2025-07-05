# src/boat.py - Classe dos barcos

import pygame
import math
from config import *
from src.utils import board_to_screen, lerp

class Boat:
    """Classe que representa um barco no jogo"""
    
    def __init__(self, x, y, player_id, color):
        self.x = x
        self.y = y
        self.player_id = player_id
        self.color = color
        
        # Visual
        self.size = 25
        self.sail_color = (255, 255, 255)  # Vela branca
        
        # Movimento
        self.moves_remaining = MOVEMENT_LIMIT
        self.fish_collected = 0
        self.is_moving = False
        self.move_progress = 0
        self.move_speed = 3
        
        # Posição visual (para animação)
        self.visual_x = x
        self.visual_y = y
        self.target_x = x
        self.target_y = y
        
        # Animação
        self.rotation = 0
        self.bob_offset = 0
        self.bob_speed = 2
        
        # Rastro de movimento
        self.trail = []
        self.max_trail_length = 5
        
    def set_position(self, x, y):
        """Define uma nova posição (sem animação)"""
        self.x = x
        self.y = y
        self.visual_x = x
        self.visual_y = y
        self.target_x = x
        self.target_y = y
        
    def move_to(self, x, y):
        """Move o barco para uma nova posição (com animação)"""
        if self.can_move():
            # Adiciona posição atual ao rastro
            self.trail.append((self.x, self.y))
            if len(self.trail) > self.max_trail_length:
                self.trail.pop(0)
            
            # Define novo alvo
            self.target_x = x
            self.target_y = y
            self.is_moving = True
            self.move_progress = 0
            
            # Calcula rotação baseada na direção
            dx = x - self.x
            dy = y - self.y
            if dx != 0 or dy != 0:
                self.rotation = math.degrees(math.atan2(dy, dx)) - 90
            
            # Reduz movimentos restantes
            self.moves_remaining -= 1
            
            return True
        return False
    
    def can_move(self):
        """Verifica se o barco pode se mover"""
        return self.moves_remaining > 0
    
    def collect_fish(self):
        """Coleta um peixe"""
        self.fish_collected += 1
        self.moves_remaining = max(0, self.moves_remaining - 1)
        
    def reset_moves(self):
        """Reseta os movimentos para o próximo turno"""
        self.moves_remaining = MOVEMENT_LIMIT - self.fish_collected
        
    def update(self, dt):
        """Atualiza o barco"""
        # Animação de balanço
        self.bob_offset += self.bob_speed * dt
        
        # Movimento suave
        if self.is_moving:
            self.move_progress += self.move_speed * dt
            
            if self.move_progress >= 1.0:
                # Movimento completo
                self.x = self.target_x
                self.y = self.target_y
                self.visual_x = self.x
                self.visual_y = self.y
                self.is_moving = False
                self.move_progress = 1.0
            else:
                # Interpolação
                self.visual_x = lerp(self.x, self.target_x, self.move_progress)
                self.visual_y = lerp(self.y, self.target_y, self.move_progress)
    
    def draw(self, screen):
        """Desenha o barco"""
        # Desenha rastro
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(255 * (i + 1) / len(self.trail))
            trail_screen_x, trail_screen_y = board_to_screen(trail_x, trail_y)
            
            # Cria uma superfície com transparência
            trail_surface = pygame.Surface((10, 10))
            trail_surface.set_alpha(alpha // 2)
            trail_surface.fill((100, 150, 200))
            
            screen.blit(trail_surface, 
                       (trail_screen_x - 5, trail_screen_y - 5))
        
        # Posição na tela
        screen_x, screen_y = board_to_screen(self.visual_x, self.visual_y)
        
        # Efeito de balanço
        wobble = math.sin(self.bob_offset) * 2
        screen_y += wobble
        
        # Salva o estado atual
        original_surface = screen.copy()
        
        # Casco do barco
        hull_points = [
            (screen_x - self.size // 2, screen_y - self.size // 3),
            (screen_x + self.size // 2, screen_y - self.size // 3),
            (screen_x + self.size // 3, screen_y + self.size // 2),
            (screen_x - self.size // 3, screen_y + self.size // 2)
        ]
        
        # Rotaciona os pontos se estiver em movimento
        if self.is_moving:
            center = (screen_x, screen_y)
            hull_points = self._rotate_points(hull_points, center, self.rotation)
        
        pygame.draw.polygon(screen, self.color, hull_points)
        pygame.draw.polygon(screen, COLORS['BLACK'], hull_points, 2)
        
        # Vela
        sail_height = self.size
        sail_points = [
            (screen_x, screen_y - self.size // 3),
            (screen_x, screen_y - self.size // 3 - sail_height),
            (screen_x + self.size // 2, screen_y - self.size // 3 - sail_height // 2)
        ]
        
        if self.is_moving:
            sail_points = self._rotate_points(sail_points, (screen_x, screen_y), self.rotation)
        
        pygame.draw.polygon(screen, self.sail_color, sail_points)
        pygame.draw.polygon(screen, COLORS['BLACK'], sail_points, 1)
        
        # Mastro
        mast_start = (screen_x, screen_y - self.size // 3)
        mast_end = (screen_x, screen_y - self.size // 3 - sail_height - 5)
        
        if self.is_moving:
            mast_start = self._rotate_point(mast_start, (screen_x, screen_y), self.rotation)
            mast_end = self._rotate_point(mast_end, (screen_x, screen_y), self.rotation)
        
        pygame.draw.line(screen, (139, 69, 19), mast_start, mast_end, 3)
        
        # Número do jogador
        font = pygame.font.Font(None, 16)
        text = font.render(str(self.player_id + 1), True, COLORS['BLACK'])
        text_rect = text.get_rect(center=(screen_x, screen_y))
        screen.blit(text, text_rect)
        
        # Indicador de peixes coletados
        if self.fish_collected > 0:
            for i in range(self.fish_collected):
                fish_x = screen_x - 20 + i * 15
                fish_y = screen_y + self.size // 2 + 10
                pygame.draw.circle(screen, (255, 165, 0), (fish_x, fish_y), 5)
                pygame.draw.circle(screen, COLORS['BLACK'], (fish_x, fish_y), 5, 1)
    
    def _rotate_point(self, point, center, angle):
        """Rotaciona um ponto ao redor de um centro"""
        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        x = point[0] - center[0]
        y = point[1] - center[1]
        
        new_x = x * cos_a - y * sin_a + center[0]
        new_y = x * sin_a + y * cos_a + center[1]
        
        return (new_x, new_y)
    
    def _rotate_points(self, points, center, angle):
        """Rotaciona uma lista de pontos"""
        return [self._rotate_point(p, center, angle) for p in points]
    
    def get_position(self):
        """Retorna a posição do barco"""
        return (self.x, self.y)