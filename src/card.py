# src/card.py - Sistema de cartas de movimento

import pygame
import random
import math
from config import *
from src.utils import draw_text

class Card:
    """Classe que representa uma carta de movimento"""
    
    def __init__(self, vector):
        self.vector = vector  # (dx, dy)
        self.selected = False
        self.hover = False
        
        # Visual
        self.width = 80
        self.height = 120
        self.color = (50, 50, 100)
        self.border_color = COLORS['WHITE']
        self.selected_color = COLORS['YELLOW']
        
        # Posição (será definida quando desenhada)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
    def get_vector(self):
        """Retorna o vetor de movimento"""
        return self.vector
    
    def set_position(self, x, y):
        """Define a posição da carta"""
        self.rect.x = x
        self.rect.y = y
        
    def handle_click(self, pos):
        """Verifica se a carta foi clicada"""
        if self.rect.collidepoint(pos):
            self.selected = not self.selected
            return True
        return False
    
    def update_hover(self, mouse_pos):
        """Atualiza o estado de hover"""
        self.hover = self.rect.collidepoint(mouse_pos)
        
    def draw(self, screen, face_up=True):
        """Desenha a carta"""
        # Fundo da carta
        if self.hover:
            color = tuple(min(255, c + 30) for c in self.color)
        else:
            color = self.color
            
        pygame.draw.rect(screen, color, self.rect)
        
        # Borda
        border_color = self.selected_color if self.selected else self.border_color
        pygame.draw.rect(screen, border_color, self.rect, 3)
        
        if face_up:
            # Desenha o vetor
            center_x = self.rect.centerx
            center_y = self.rect.centery - 10
            
            # Círculo central
            pygame.draw.circle(screen, COLORS['WHITE'], (center_x, center_y), 5)
            
            # Seta do vetor
            dx, dy = self.vector
            if dx != 0 or dy != 0:
                # Escala para visualização
                scale = 20
                end_x = center_x + dx * scale
                end_y = center_y + dy * scale
                
                # Linha principal
                pygame.draw.line(screen, COLORS['WHITE'], 
                               (center_x, center_y), (end_x, end_y), 3)
                
                # Ponta da seta
                arrow_size = 8
                angle = math.atan2(dy, dx)
                
                # Pontos da ponta da seta
                arrow_point1 = (
                    end_x - arrow_size * math.cos(angle - math.pi/6),
                    end_y - arrow_size * math.sin(angle - math.pi/6)
                )
                arrow_point2 = (
                    end_x - arrow_size * math.cos(angle + math.pi/6),
                    end_y - arrow_size * math.sin(angle + math.pi/6)
                )
                
                pygame.draw.polygon(screen, COLORS['WHITE'], 
                                  [(end_x, end_y), arrow_point1, arrow_point2])
            
            # Texto do vetor
            vector_text = f"({dx}, {dy})"
            draw_text(screen, vector_text, self.rect.centerx, 
                     self.rect.bottom - 20, size=16, color=COLORS['WHITE'], center=True)
        else:
            # Carta virada para baixo
            # Desenha o verso da carta
            pattern_color = (70, 70, 120)
            for i in range(4):
                for j in range(6):
                    if (i + j) % 2 == 0:
                        rect = pygame.Rect(
                            self.rect.x + 5 + i * 18,
                            self.rect.y + 5 + j * 18,
                            16, 16
                        )
                        pygame.draw.rect(screen, pattern_color, rect)
            
            # Texto "?"
            draw_text(screen, "?", self.rect.centerx, self.rect.centery,
                     size=48, color=COLORS['WHITE'], center=True)


class CardDeck:
    """Classe que gerencia o baralho de cartas"""
    
    def __init__(self):
        self.cards = []
        self.create_deck()
        self.shuffle()
        
    def create_deck(self):
        """Cria o baralho com todas as cartas"""
        # Cria múltiplas cópias de cada vetor
        for vector in MOVEMENT_CARDS:
            # Quantidade de cópias baseada na força do vetor
            magnitude = abs(vector[0]) + abs(vector[1])
            if magnitude == 0:
                copies = 4  # Cartas sem movimento
            elif magnitude == 1:
                copies = 6  # Movimentos básicos
            elif magnitude == 2:
                copies = 4  # Movimentos diagonais ou fortes
            else:
                copies = 2  # Movimentos muito fortes
            
            for _ in range(copies):
                self.cards.append(Card(vector))
    
    def shuffle(self):
        """Embaralha o baralho"""
        random.shuffle(self.cards)
        
    def draw_card(self):
        """Compra uma carta do baralho"""
        if len(self.cards) == 0:
            # Reembaralha se acabaram as cartas
            self.create_deck()
            self.shuffle()
        
        return self.cards.pop()
    
    def return_card(self, card):
        """Retorna uma carta ao baralho"""
        self.cards.append(card)
        

class PlayerHand:
    """Classe que gerencia a mão de um jogador"""
    
    def __init__(self, player_id):
        self.player_id = player_id
        self.cards = []
        self.max_cards = 3
        self.selected_card = None
        
    def add_card(self, card):
        """Adiciona uma carta à mão"""
        if len(self.cards) < self.max_cards:
            self.cards.append(card)
            return True
        return False
    
    def remove_card(self, card):
        """Remove uma carta da mão"""
        if card in self.cards:
            self.cards.remove(card)
            if self.selected_card == card:
                self.selected_card = None
            return True
        return False
    
    def select_card(self, index):
        """Seleciona uma carta pelo índice"""
        if 0 <= index < len(self.cards):
            # Deseleciona todas as outras
            for card in self.cards:
                card.selected = False
            
            # Seleciona a carta escolhida
            self.cards[index].selected = True
            self.selected_card = self.cards[index]
            return True
        return False
    
    def get_selected_card(self):
        """Retorna a carta selecionada"""
        return self.selected_card
    
    def handle_click(self, pos):
        """Processa clique nas cartas"""
        for i, card in enumerate(self.cards):
            if card.handle_click(pos):
                # Deseleciona outras cartas
                for j, other_card in enumerate(self.cards):
                    if i != j:
                        other_card.selected = False
                
                self.selected_card = card if card.selected else None
                return True
        return False
    
    def update(self, mouse_pos):
        """Atualiza as cartas"""
        for card in self.cards:
            card.update_hover(mouse_pos)
    
    def draw(self, screen, x, y, show_cards=True):
        """Desenha as cartas da mão"""
        card_spacing = 90
        
        for i, card in enumerate(self.cards):
            card_x = x + i * card_spacing
            card_y = y
            
            # Ajusta posição se hover
            if card.hover:
                card_y -= 10
            
            card.set_position(card_x, card_y)
            card.draw(screen, face_up=show_cards)
            
        # Indicador de jogador
        player_text = f"Jogador {self.player_id + 1}"
        draw_text(screen, player_text, x, y - 30, 
                 size=20, color=COLORS['PLAYER_COLORS'][self.player_id])