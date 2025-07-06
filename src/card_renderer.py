# src/card_renderer.py - Renderizador de cartas baseado no PDF

import pygame
import math
from config import *
from src.utils import create_gradient_surface

class CardRenderer:
    """Renderizador de cartas visuais do Caçador dos Mares"""
    
    def __init__(self):
        self.card_width = 120
        self.card_height = 160
        self.card_cache = {}
        self.selected_card = None
        self.hover_card = None
        self.animation_time = 0
        
        # Cores baseadas no PDF
        self.colors = {
            'card_bg_start': (64, 32, 128),      # Roxo escuro
            'card_bg_end': (32, 64, 255),        # Azul
            'card_border': (255, 255, 255),      # Branco
            'vector_line': (255, 255, 255),      # Branco
            'vector_arrow': (255, 255, 0),       # Amarelo
            'coordinate_text': (255, 255, 255),  # Branco
            'selected_glow': (255, 255, 0),      # Amarelo
            'hover_highlight': (200, 200, 255)   # Azul claro
        }
        
    def create_card_surface(self, vector, selected=False, hover=False):
        """Cria superfície da carta com o vetor especificado"""
        # Verifica cache
        cache_key = f"{vector}_{selected}_{hover}_{int(self.animation_time)}"
        if cache_key in self.card_cache:
            return self.card_cache[cache_key]
        
        # Cria superfície da carta
        card_surface = pygame.Surface((self.card_width, self.card_height), pygame.SRCALPHA)
        
        # Fundo com gradiente (baseado no PDF)
        gradient = create_gradient_surface(
            self.card_width, self.card_height,
            self.colors['card_bg_start'],
            self.colors['card_bg_end'],
            vertical=True
        )
        card_surface.blit(gradient, (0, 0))
        
        # Borda da carta
        border_color = self.colors['selected_glow'] if selected else self.colors['card_border']
        border_width = 4 if selected else 2
        
        if hover and not selected:
            border_color = self.colors['hover_highlight']
            border_width = 3
        
        pygame.draw.rect(card_surface, border_color, 
                        (0, 0, self.card_width, self.card_height), border_width)
        
        # Efeito de brilho para carta selecionada
        if selected:
            glow_intensity = int(50 + 30 * math.sin(self.animation_time * 0.1))
            glow_surface = pygame.Surface((self.card_width, self.card_height), pygame.SRCALPHA)
            glow_surface.set_alpha(glow_intensity)
            glow_surface.fill(self.colors['selected_glow'])
            card_surface.blit(glow_surface, (0, 0))
        
        # Desenha vetor no centro da carta
        self.draw_vector_on_card(card_surface, vector)
        
        # Texto com coordenadas
        self.draw_coordinate_text(card_surface, vector)
        
        # Cache e retorna
        self.card_cache[cache_key] = card_surface
        return card_surface
    
    def draw_vector_on_card(self, surface, vector):
        """Desenha o vetor na carta"""
        center_x = self.card_width // 2
        center_y = self.card_height // 2 - 10
        
        # Escala do vetor para caber na carta
        scale = min(30, max(15, 25))
        
        # Calcula ponto final do vetor
        end_x = center_x + vector[0] * scale
        end_y = center_y - vector[1] * scale  # Y invertido no pygame
        
        # Desenha linha do vetor se não for (0,0)
        if vector != (0, 0):
            pygame.draw.line(surface, self.colors['vector_line'],
                           (center_x, center_y), (end_x, end_y), 3)
            
            # Desenha seta
            self.draw_arrow_head(surface, center_x, center_y, end_x, end_y)
        else:
            # Para vetor (0,0), desenha um círculo
            pygame.draw.circle(surface, self.colors['vector_line'],
                             (center_x, center_y), 8, 3)
            pygame.draw.circle(surface, self.colors['vector_arrow'],
                             (center_x, center_y), 4)
    
    def draw_arrow_head(self, surface, start_x, start_y, end_x, end_y):
        """Desenha a ponta da seta"""
        # Calcula ângulo da linha
        angle = math.atan2(end_y - start_y, end_x - start_x)
        
        # Tamanho da seta
        arrow_length = 12
        arrow_angle = math.pi / 6  # 30 graus
        
        # Pontos da seta
        arrow_point1_x = end_x - arrow_length * math.cos(angle - arrow_angle)
        arrow_point1_y = end_y - arrow_length * math.sin(angle - arrow_angle)
        arrow_point2_x = end_x - arrow_length * math.cos(angle + arrow_angle)
        arrow_point2_y = end_y - arrow_length * math.sin(angle + arrow_angle)
        
        # Desenha triângulo da seta
        points = [(end_x, end_y), (arrow_point1_x, arrow_point1_y), (arrow_point2_x, arrow_point2_y)]
        pygame.draw.polygon(surface, self.colors['vector_arrow'], points)
    
    def draw_coordinate_text(self, surface, vector):
        """Desenha o texto com as coordenadas"""
        font = pygame.font.Font(None, 24)
        coord_text = f"({vector[0]}, {vector[1]})"
        
        text_surface = font.render(coord_text, True, self.colors['coordinate_text'])
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.card_width // 2
        text_rect.bottom = self.card_height - 10
        
        # Fundo semi-transparente para o texto
        bg_rect = text_rect.copy()
        bg_rect.inflate(8, 4)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.set_alpha(128)
        bg_surface.fill((0, 0, 0))
        surface.blit(bg_surface, bg_rect)
        
        surface.blit(text_surface, text_rect)
    
    def update(self, dt):
        """Atualiza animações"""
        self.animation_time += dt
        
        # Limpa cache periodicamente
        if len(self.card_cache) > 50:
            self.card_cache.clear()
    
    def render_hand(self, surface, hand, x, y, selected_index=-1):
        """Renderiza a mão de cartas do jogador"""
        if not hand or len(hand) == 0:
            return []
        
        card_rects = []
        spacing = self.card_width + 10
        total_width = len(hand) * self.card_width + (len(hand) - 1) * 10
        start_x = x - total_width // 2
        
        for i, card in enumerate(hand):
            card_x = start_x + i * spacing
            card_y = y
            
            # Efeito de elevação para carta selecionada
            if i == selected_index:
                card_y -= 20
            
            # Verifica hover
            mouse_pos = pygame.mouse.get_pos()
            card_rect = pygame.Rect(card_x, card_y, self.card_width, self.card_height)
            is_hover = card_rect.collidepoint(mouse_pos)
            is_selected = (i == selected_index)
            
            # Renderiza carta
            card_surface = self.create_card_surface(card.get_vector(), is_selected, is_hover)
            surface.blit(card_surface, (card_x, card_y))
            
            card_rects.append(card_rect)
        
        return card_rects

# Instância global
card_renderer = CardRenderer()
