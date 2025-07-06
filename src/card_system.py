# src/card_system.py - Sistema de cartas baseado no PDF

import pygame
import math
from config import *
from src.layout_manager import layout_manager

class VisualCard:
    """Carta visual baseada no design do PDF fornecido"""
    
    def __init__(self, vector, card_id=None):
        self.vector = vector
        self.card_id = card_id or f"card_{vector[0]}_{vector[1]}"
        
        # Dimensões responsivas
        self.base_width = 100
        self.base_height = 140
        
        # Estados visuais
        self.is_selected = False
        self.is_hovered = False
        self.is_face_down = False
        self.animation_time = 0
        self.hover_offset = 0
        self.selection_glow = 0
        
        # Cache de superfície
        self.surface_cache = {}
        self.last_scale = 0
    
    def get_dimensions(self):
        """Retorna dimensões responsivas da carta"""
        scale = layout_manager.get_element_scale_factor()
        width = int(self.base_width * scale)
        height = int(self.base_height * scale)
        return width, height
    
    def update(self, dt, is_selected=False, is_hovered=False):
        """Atualiza estado da carta"""
        self.is_selected = is_selected
        self.is_hovered = is_hovered
        self.animation_time += dt
        
        # Animação de hover
        target_hover = 20 if is_hovered and not is_selected else 0
        self.hover_offset += (target_hover - self.hover_offset) * dt * 8
        
        # Animação de seleção
        target_glow = 1.0 if is_selected else 0.0
        self.selection_glow += (target_glow - self.selection_glow) * dt * 6
    
    def get_surface(self):
        """Retorna superfície da carta com cache"""
        scale = layout_manager.get_element_scale_factor()
        
        # Verifica cache
        cache_key = f"{scale}_{self.is_selected}_{self.is_hovered}_{self.is_face_down}_{int(self.animation_time * 10)}"
        if cache_key in self.surface_cache and scale == self.last_scale:
            return self.surface_cache[cache_key]
        
        # Limpa cache se escala mudou
        if scale != self.last_scale:
            self.surface_cache.clear()
            self.last_scale = scale
        
        # Cria nova superfície
        width, height = self.get_dimensions()
        surface = self.create_card_surface(width, height)
        
        # Atualiza cache (máximo 10 entradas)
        if len(self.surface_cache) >= 10:
            self.surface_cache.clear()
        self.surface_cache[cache_key] = surface
        
        return surface
    
    def create_card_surface(self, width, height):
        """Cria superfície da carta baseada no PDF"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        if self.is_face_down:
            self.draw_card_back(surface, width, height)
        else:
            self.draw_card_front(surface, width, height)
        
        return surface
    
    def draw_card_front(self, surface, width, height):
        """Desenha frente da carta (baseado no PDF)"""
        # Fundo com gradiente roxo-azul (como no PDF)
        self.draw_gradient_background(surface, width, height)
        
        # Borda da carta
        self.draw_card_border(surface, width, height)
        
        # Efeito de seleção
        if self.is_selected:
            self.draw_selection_effect(surface, width, height)
        
        # Desenha o vetor no centro
        self.draw_vector_visualization(surface, width, height)
        
        # Coordenadas na parte inferior
        self.draw_coordinates_text(surface, width, height)
    
    def draw_gradient_background(self, surface, width, height):
        """Desenha fundo com gradiente como no PDF"""
        # Cores baseadas no PDF: roxo escuro -> azul
        start_color = (64, 32, 128)   # Roxo escuro
        end_color = (32, 64, 255)     # Azul
        
        # Desenha gradiente vertical
        for y in range(height):
            ratio = y / height
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    
    def draw_card_border(self, surface, width, height):
        """Desenha borda da carta"""
        border_color = (255, 255, 255)  # Branco como no PDF
        border_width = max(2, int(3 * layout_manager.get_element_scale_factor()))
        
        # Borda externa
        pygame.draw.rect(surface, border_color, (0, 0, width, height), border_width)
        
        # Se hover, adiciona borda interna
        if self.is_hovered and not self.is_selected:
            inner_border = max(1, border_width - 1)
            inner_rect = pygame.Rect(border_width, border_width, 
                                   width - border_width * 2, height - border_width * 2)
            pygame.draw.rect(surface, (200, 200, 255), inner_rect, inner_border)
    
    def draw_selection_effect(self, surface, width, height):
        """Desenha efeito de seleção (brilho dourado)"""
        # Brilho pulsante dourado
        glow_alpha = int(100 + 50 * math.sin(self.animation_time * 8) * self.selection_glow)
        glow_color = (255, 255, 0, glow_alpha)  # Dourado
        
        # Cria superfície de brilho
        glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        glow_surface.set_alpha(glow_alpha)
        glow_surface.fill((255, 255, 0))
        
        # Aplica brilho
        surface.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_ADD)
        
        # Borda dourada
        pygame.draw.rect(surface, (255, 255, 0), (0, 0, width, height), 
                        max(3, int(4 * layout_manager.get_element_scale_factor())))
    
    def draw_vector_visualization(self, surface, width, height):
        """Desenha visualização do vetor como no PDF"""
        center_x = width // 2
        center_y = height // 2 - height // 8  # Ligeiramente acima do centro
        
        # Escala do vetor baseada no tamanho da carta
        scale = min(width, height) // 6
        
        # Calcula ponto final do vetor
        end_x = center_x + self.vector[0] * scale
        end_y = center_y - self.vector[1] * scale  # Y invertido
        
        # Cor do vetor (branco como no PDF)
        vector_color = (255, 255, 255)
        line_width = max(2, int(3 * layout_manager.get_element_scale_factor()))
        
        if self.vector == (0, 0):
            # Para vetor zero, desenha círculo (como no PDF)
            radius = max(6, int(8 * layout_manager.get_element_scale_factor()))
            pygame.draw.circle(surface, vector_color, (center_x, center_y), radius, line_width)
            
            # Ponto central
            pygame.draw.circle(surface, vector_color, (center_x, center_y), radius // 2)
        else:
            # Desenha linha do vetor
            pygame.draw.line(surface, vector_color, (center_x, center_y), (end_x, end_y), line_width)
            
            # Desenha seta na ponta
            self.draw_arrow_head(surface, center_x, center_y, end_x, end_y, vector_color)
    
    def draw_arrow_head(self, surface, start_x, start_y, end_x, end_y, color):
        """Desenha ponta da seta"""
        # Calcula ângulo da linha
        angle = math.atan2(end_y - start_y, end_x - start_x)
        
        # Tamanho da seta baseado na escala
        arrow_size = max(8, int(12 * layout_manager.get_element_scale_factor()))
        arrow_angle = math.pi / 6  # 30 graus
        
        # Pontos da seta
        point1_x = end_x - arrow_size * math.cos(angle - arrow_angle)
        point1_y = end_y - arrow_size * math.sin(angle - arrow_angle)
        point2_x = end_x - arrow_size * math.cos(angle + arrow_angle)
        point2_y = end_y - arrow_size * math.sin(angle + arrow_angle)
        
        # Desenha triângulo da seta
        arrow_points = [(end_x, end_y), (point1_x, point1_y), (point2_x, point2_y)]
        pygame.draw.polygon(surface, color, arrow_points)
    
    def draw_coordinates_text(self, surface, width, height):
        """Desenha texto das coordenadas como no PDF"""
        font_size = layout_manager.get_font_size(18)
        font = pygame.font.Font(None, font_size)
        
        # Texto das coordenadas
        coord_text = f"({self.vector[0]}, {self.vector[1]})"
        text_surface = font.render(coord_text, True, (255, 255, 255))
        
        # Posição na parte inferior
        text_rect = text_surface.get_rect()
        text_rect.centerx = width // 2
        text_rect.bottom = height - max(8, int(10 * layout_manager.get_element_scale_factor()))
        
        # Fundo semi-transparente para legibilidade
        bg_padding = max(4, int(6 * layout_manager.get_element_scale_factor()))
        bg_rect = text_rect.inflate(bg_padding * 2, bg_padding)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.set_alpha(128)
        bg_surface.fill((0, 0, 0))
        
        surface.blit(bg_surface, bg_rect)
        surface.blit(text_surface, text_rect)
    
    def draw_card_back(self, surface, width, height):
        """Desenha verso da carta"""
        # Fundo com gradiente diferente
        for y in range(height):
            ratio = y / height
            r = int(32 + ratio * 32)
            g = int(64 + ratio * 32)
            b = int(128 + ratio * 64)
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
        
        # Borda
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, width, height), 
                        max(2, int(3 * layout_manager.get_element_scale_factor())))
        
        # Logo "Caçador dos Mares" (texto simples)
        font_size = layout_manager.get_font_size(12)
        font = pygame.font.Font(None, font_size)
        
        text_lines = ["Caçador", "dos", "Mares"]
        line_height = font_size + 2
        total_height = len(text_lines) * line_height
        start_y = (height - total_height) // 2
        
        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.centerx = width // 2
            text_rect.y = start_y + i * line_height
            surface.blit(text_surface, text_rect)
    
    def get_rect(self, x, y):
        """Retorna rect da carta na posição especificada"""
        width, height = self.get_dimensions()
        return pygame.Rect(x, y - int(self.hover_offset), width, height)
    
    def draw(self, surface, x, y):
        """Desenha a carta na posição especificada"""
        card_surface = self.get_surface()
        draw_y = y - int(self.hover_offset)
        
        # Efeito de elevação para carta selecionada
        if self.is_selected:
            draw_y -= max(10, int(15 * layout_manager.get_element_scale_factor()))
        
        surface.blit(card_surface, (x, draw_y))

class CardHand:
    """Mão de cartas do jogador"""
    
    def __init__(self):
        self.cards = []
        self.selected_index = -1
        self.card_spacing_ratio = 1.1  # 10% de espaçamento
    
    def add_card(self, vector):
        """Adiciona carta à mão"""
        card = VisualCard(vector)
        self.cards.append(card)
    
    def remove_card(self, index):
        """Remove carta da mão"""
        if 0 <= index < len(self.cards):
            removed = self.cards.pop(index)
            if self.selected_index >= index:
                self.selected_index = max(-1, self.selected_index - 1)
            return removed
        return None
    
    def select_card(self, index):
        """Seleciona carta"""
        if 0 <= index < len(self.cards):
            self.selected_index = index
        else:
            self.selected_index = -1
    
    def get_selected_card(self):
        """Retorna carta selecionada"""
        if 0 <= self.selected_index < len(self.cards):
            return self.cards[self.selected_index]
        return None
    
    def update(self, dt, mouse_pos):
        """Atualiza todas as cartas da mão"""
        for i, card in enumerate(self.cards):
            is_selected = (i == self.selected_index)
            is_hovered = False
            
            # Verifica hover se não selecionada
            if not is_selected and mouse_pos:
                card_rect = self.get_card_rect(i)
                is_hovered = card_rect.collidepoint(mouse_pos) if card_rect else False
            
            card.update(dt, is_selected, is_hovered)
    
    def get_card_rect(self, index):
        """Retorna rect de uma carta específica"""
        if not (0 <= index < len(self.cards)):
            return None
        
        layout = self.get_layout()
        if index < len(layout['positions']):
            x, y = layout['positions'][index]
            return self.cards[index].get_rect(x, y)
        return None
    
    def get_layout(self):
        """Calcula layout das cartas"""
        if not self.cards:
            return {'positions': [], 'total_width': 0, 'total_height': 0}
        
        # Dimensões das cartas
        card_width, card_height = self.cards[0].get_dimensions()
        
        # Espaçamento entre cartas
        spacing = int(card_width * self.card_spacing_ratio - card_width)
        
        # Largura total
        total_width = len(self.cards) * card_width + (len(self.cards) - 1) * spacing
        
        # Posições das cartas
        positions = []
        for i in range(len(self.cards)):
            x = i * (card_width + spacing)
            y = 0
            positions.append((x, y))
        
        return {
            'positions': positions,
            'total_width': total_width,
            'total_height': card_height,
            'card_width': card_width,
            'card_height': card_height
        }
    
    def handle_click(self, mouse_pos):
        """Processa clique do mouse nas cartas"""
        for i in range(len(self.cards)):
            card_rect = self.get_card_rect(i)
            if card_rect and card_rect.collidepoint(mouse_pos):
                if self.selected_index == i:
                    # Deseleciona se já estava selecionada
                    self.selected_index = -1
                else:
                    # Seleciona carta
                    self.selected_index = i
                return i
        return -1
    
    def draw(self, surface, base_x, base_y):
        """Desenha todas as cartas da mão"""
        layout = self.get_layout()
        
        # Centraliza as cartas
        start_x = base_x - layout['total_width'] // 2
        
        for i, (offset_x, offset_y) in enumerate(layout['positions']):
            x = start_x + offset_x
            y = base_y + offset_y
            self.cards[i].draw(surface, x, y)

# Instância global para teste
test_hand = CardHand()
