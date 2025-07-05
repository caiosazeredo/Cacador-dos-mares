# src/player.py - Classe do jogador

from src.boat import Boat
from src.card import PlayerHand
from config import *

class Player:
    """Classe que representa um jogador"""
    
    def __init__(self, player_id, name, color, is_ai=False, ai_difficulty='MEDIO'):
        self.id = player_id
        self.name = name
        self.color = color
        self.is_ai = is_ai
        self.ai_difficulty = ai_difficulty
        
        # Barco do jogador
        self.boat = None
        
        # Mão de cartas
        self.hand = PlayerHand(player_id)
        
        # Carta jogada no turno
        self.played_card = None
        
        # Estatísticas
        self.fish_collected = 0
        self.turns_played = 0
        self.total_distance_moved = 0
        
        # Estado
        self.is_active = True
        self.has_played_card = False
        self.has_moved = False
        
    def create_boat(self, x, y):
        """Cria o barco do jogador"""
        self.boat = Boat(x, y, self.id, self.color)
        
    def collect_fish(self):
        """Coleta um peixe"""
        self.fish_collected += 1
        if self.boat:
            self.boat.collect_fish()
            
    def play_card(self, card):
        """Joga uma carta"""
        if card in self.hand.cards:
            self.played_card = card
            self.hand.remove_card(card)
            self.has_played_card = True
            return True
        return False
    
    def move_boat(self, x, y):
        """Move o barco do jogador"""
        if self.boat and self.boat.can_move():
            old_x, old_y = self.boat.get_position()
            if self.boat.move_to(x, y):
                # Calcula distância movida
                distance = abs(x - old_x) + abs(y - old_y)
                self.total_distance_moved += distance
                self.has_moved = True
                return True
        return False
    
    def end_turn(self):
        """Finaliza o turno do jogador"""
        self.turns_played += 1
        self.has_played_card = False
        self.has_moved = False
        self.played_card = None
        
        if self.boat:
            self.boat.reset_moves()
    
    def get_stats(self):
        """Retorna as estatísticas do jogador"""
        return {
            'name': self.name,
            'fish_collected': self.fish_collected,
            'turns_played': self.turns_played,
            'total_distance': self.total_distance_moved,
            'average_distance': self.total_distance_moved / max(1, self.turns_played)
        }
    
    def is_winner(self):
        """Verifica se o jogador venceu"""
        return self.fish_collected >= WINNING_FISH_COUNT
    
    def update(self, dt):
        """Atualiza o jogador"""
        if self.boat:
            self.boat.update(dt)
    
    def draw_hand(self, screen, x, y, show_cards=True):
        """Desenha a mão do jogador"""
        if not self.is_ai or show_cards:
            self.hand.draw(screen, x, y, show_cards)
    
    def __repr__(self):
        return f"Player({self.id}, {self.name}, AI={self.is_ai})"