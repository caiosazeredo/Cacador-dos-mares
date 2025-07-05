# src/ai.py - Sistema de IA para jogadores computador

import random
import math
from config import *
from src.utils import manhattan_distance, euclidean_distance

class AIPlayer:
    """Classe que controla o comportamento da IA"""
    
    def __init__(self, player, difficulty='MEDIO'):
        self.player = player
        self.difficulty = AI_DIFFICULTIES[difficulty]
        self.think_timer = 0
        self.decision_made = False
        
    def update(self, dt, game_state):
        """Atualiza a IA"""
        if not self.decision_made:
            self.think_timer += dt
            
            if self.think_timer >= self.difficulty['think_time']:
                self.make_decision(game_state)
                self.decision_made = True
                self.think_timer = 0
    
    def reset_decision(self):
        """Reseta o estado de decisão"""
        self.decision_made = False
        self.think_timer = 0
    
    def make_decision(self, game_state):
        """Toma uma decisão baseada no estado do jogo"""
        pass  # Será implementado nas subclasses
    
    def evaluate_board_state(self, game_state):
        """Avalia o estado atual do tabuleiro"""
        boat_pos = self.player.boat.get_position()
        fish_positions = game_state['fish_positions']
        other_boats = game_state['other_boats']
        
        # Calcula distâncias para todos os peixes
        fish_distances = []
        for fish_pos in fish_positions:
            dist = manhattan_distance(boat_pos, fish_pos)
            fish_distances.append((dist, fish_pos))
        
        fish_distances.sort(key=lambda x: x[0])
        
        # Avalia posições dos outros barcos
        boat_distances = []
        for boat in other_boats:
            if boat != self.player.boat:
                dist = manhattan_distance(boat_pos, boat.get_position())
                boat_distances.append((dist, boat))
        
        return {
            'boat_pos': boat_pos,
            'fish_distances': fish_distances,
            'boat_distances': boat_distances,
            'closest_fish': fish_distances[0] if fish_distances else None
        }


class CardPlayAI(AIPlayer):
    """IA para escolher qual carta jogar"""
    
    def make_decision(self, game_state):
        """Escolhe uma carta para jogar"""
        evaluation = self.evaluate_board_state(game_state)
        
        # Fator de aleatoriedade baseado na dificuldade
        if random.random() < self.difficulty['random_factor']:
            # Escolha aleatória
            card = random.choice(self.player.hand.cards)
        else:
            # Escolha estratégica
            card = self.choose_best_card(evaluation, game_state)
        
        return card
    
    def choose_best_card(self, evaluation, game_state):
        """Escolhe a melhor carta baseada na estratégia"""
        boat_pos = evaluation['boat_pos']
        
        # Se não há peixes, joga qualquer carta
        if not evaluation['fish_distances']:
            return random.choice(self.player.hand.cards)
        
        # Analisa as cartas disponíveis
        card_scores = []
        
        for card in self.player.hand.cards:
            vector = card.get_vector()
            score = self.evaluate_card(vector, evaluation, game_state)
            card_scores.append((score, card))
        
        # Ordena por pontuação
        card_scores.sort(key=lambda x: x[0], reverse=True)
        
        # Retorna a melhor carta
        return card_scores[0][1]
    
    def evaluate_card(self, vector, evaluation, game_state):
        """Avalia uma carta específica"""
        score = 0
        
        # Considera o peixe mais próximo
        if evaluation['closest_fish']:
            closest_dist, closest_pos = evaluation['closest_fish']
            
            # Verifica se o vetor ajuda a mover peixes na direção do barco
            fish_new_pos = (
                closest_pos[0] + vector[0],
                closest_pos[1] + vector[1]
            )
            
            # Calcula nova distância
            new_dist = manhattan_distance(evaluation['boat_pos'], fish_new_pos)
            
            # Pontuação baseada na redução de distância
            if new_dist < closest_dist:
                score += (closest_dist - new_dist) * 10
            
            # Bonus se coloca o peixe dentro da distância de coleta
            if new_dist <= COLLECTION_DISTANCE:
                score += 50
            
            # Penalidade se joga o peixe para fora do tabuleiro
            if not (0 <= fish_new_pos[0] < BOARD_SIZE and 0 <= fish_new_pos[1] < BOARD_SIZE):
                score -= 30
        
        # Considera outros barcos (evita ajudá-los)
        for dist, other_boat in evaluation['boat_distances']:
            if dist < 5:  # Barco próximo
                other_pos = other_boat.get_position()
                
                # Verifica peixes próximos ao outro barco
                for fish_dist, fish_pos in evaluation['fish_distances']:
                    if manhattan_distance(other_pos, fish_pos) < 3:
                        # Penaliza se move peixe para perto do oponente
                        fish_new_pos = (
                            fish_pos[0] + vector[0],
                            fish_pos[1] + vector[1]
                        )
                        new_dist_to_opponent = manhattan_distance(other_pos, fish_new_pos)
                        if new_dist_to_opponent < manhattan_distance(other_pos, fish_pos):
                            score -= 20
        
        return score


class MovementAI(AIPlayer):
    """IA para decidir movimento do barco"""
    
    def make_decision(self, game_state):
        """Decide para onde mover o barco"""
        evaluation = self.evaluate_board_state(game_state)
        valid_moves = game_state['valid_moves']
        
        if not valid_moves:
            return None
        
        # Fator de aleatoriedade
        if random.random() < self.difficulty['random_factor']:
            # Movimento aleatório
            return random.choice(valid_moves)
        else:
            # Movimento estratégico
            return self.choose_best_move(evaluation, valid_moves, game_state)
    
    def choose_best_move(self, evaluation, valid_moves, game_state):
        """Escolhe o melhor movimento"""
        move_scores = []
        
        for move in valid_moves:
            score = self.evaluate_move(move, evaluation, game_state)
            move_scores.append((score, move))
        
        # Ordena por pontuação
        move_scores.sort(key=lambda x: x[0], reverse=True)
        
        # Adiciona um pouco de aleatoriedade entre os melhores movimentos
        top_moves = [m for s, m in move_scores[:3] if s > 0]
        
        if top_moves:
            return random.choice(top_moves)
        
        return move_scores[0][1] if move_scores else None
    
    def evaluate_move(self, move, evaluation, game_state):
        """Avalia um movimento específico"""
        score = 0
        
        # Posição após o movimento dos peixes
        predicted_fish = game_state.get('predicted_fish_positions', [])
        
        # Avalia proximidade com peixes
        for fish_pos in predicted_fish:
            dist = manhattan_distance(move, fish_pos)
            
            # Pontuação alta para peixes muito próximos
            if dist <= COLLECTION_DISTANCE:
                score += 100
            elif dist <= 3:
                score += 50 - dist * 10
            elif dist <= 5:
                score += 20 - dist * 2
        
        # Evita cantos e bordas (menos mobilidade)
        x, y = move
        center_x, center_y = BOARD_SIZE // 2, BOARD_SIZE // 2
        distance_from_center = abs(x - center_x) + abs(y - center_y)
        score -= distance_from_center * 0.5
        
        # Evita outros barcos
        for dist, other_boat in evaluation['boat_distances']:
            other_pos = other_boat.get_position()
            dist_to_other = manhattan_distance(move, other_pos)
            
            if dist_to_other < 3:
                score -= (3 - dist_to_other) * 10
        
        # Considera movimentos restantes
        moves_after = self.player.boat.moves_remaining - 1
        if moves_after < 2 and score < 50:
            # Se tem poucos movimentos, prefere posições mais seguras
            score += 10
        
        return score


class AIController:
    """Controlador principal da IA"""
    
    def __init__(self, player, difficulty='MEDIO'):
        self.player = player
        self.card_ai = CardPlayAI(player, difficulty)
        self.movement_ai = MovementAI(player, difficulty)
        
    def choose_card(self, game_state):
        """Escolhe uma carta para jogar"""
        return self.card_ai.make_decision(game_state)
    
    def choose_move(self, game_state):
        """Escolhe um movimento para o barco"""
        return self.movement_ai.make_decision(game_state)
    
    def update(self, dt, game_state, phase):
        """Atualiza a IA baseado na fase do jogo"""
        if phase == 'play_cards':
            self.card_ai.update(dt, game_state)
        elif phase == 'movement':
            self.movement_ai.update(dt, game_state)
    
    def reset_phase(self, phase):
        """Reseta a IA para uma nova fase"""
        if phase == 'play_cards':
            self.card_ai.reset_decision()
        elif phase == 'movement':
            self.movement_ai.reset_decision()