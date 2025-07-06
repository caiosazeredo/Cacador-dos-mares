# src/game.py - Classe principal do jogo (atualizada para sprites)

import pygame
import random
from config import *
from src.board import Board
from src.player import Player
from src.fish import Fish
from src.card import CardDeck
from src.ai import AIController
from src.utils import *

class Game:
    """Classe principal que gerencia o jogo"""
    
    def __init__(self, screen, host_player, num_players=2, ai_difficulty='MEDIO'):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Inicializa sprites se ainda não foram inicializados
        try:
            from src.sprite_loader import get_sprite_manager
            self.sprite_manager = get_sprite_manager()
            print("Sistema de sprites inicializado no jogo")
        except Exception as e:
            print(f"Aviso: Erro ao inicializar sprites: {e}")
            self.sprite_manager = None
        
        # Configurações
        self.num_players = num_players
        self.ai_difficulty = ai_difficulty
        
        # Componentes do jogo
        self.board = Board()
        self.players = []
        self.fish_list = []
        self.deck = CardDeck()
        
        # Estado do jogo
        self.current_player_index = 0
        self.turn_number = 1
        self.phase = 'setup'  # setup, play_cards, movement, resolution, game_over
        self.winner = None
        
        # Controle de turnos
        self.start_player_token = 0  # Índice do jogador que começa
        self.cards_played = {}  # Cartas jogadas no turno
        self.fish_to_add = 0  # Peixes para adicionar no próximo turno
        
        # UI
        self.ui_message = ""
        self.ui_message_timer = 0
        
        # Animações
        self.animations = []
        
        # Inicializa jogadores
        self.setup_players(host_player)
        
        # Inicializa o jogo
        self.setup_game()
        
    def setup_players(self, host_player):
        """Configura os jogadores"""
        # Jogador principal (humano)
        player = Player(0, host_player, COLORS['PLAYER_COLORS'][0], is_ai=False)
        self.players.append(player)
        
        # Jogadores IA
        for i in range(1, self.num_players):
            ai_player = Player(i, f"CPU {i}", COLORS['PLAYER_COLORS'][i], 
                             is_ai=True, ai_difficulty=self.ai_difficulty)
            ai_player.ai_controller = AIController(ai_player, self.ai_difficulty)
            self.players.append(ai_player)
    
    def setup_game(self):
        """Configura o estado inicial do jogo"""
        # Distribui cartas iniciais
        for player in self.players:
            for _ in range(3):
                card = self.deck.draw_card()
                player.hand.add_card(card)
        
        # Adiciona peixes iniciais
        num_initial_fish = len(self.players)
        occupied_positions = set()
        
        for _ in range(num_initial_fish):
            pos = generate_random_position(occupied_positions)
            if pos:
                x, y = pos
                fish = Fish(x, y)
                self.fish_list.append(fish)
                self.board.place_object(x, y, fish)
                occupied_positions.add(pos)
        
        self.phase = 'placement'
        self.show_message(f"Fase de Posicionamento - Jogador {self.current_player_index + 1}, escolha onde colocar seu barco")
    
    def handle_event(self, event):
        """Processa eventos do jogo"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'quit'
        
        current_player = self.players[self.current_player_index]
        
        # Fase de posicionamento inicial
        if self.phase == 'placement':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not current_player.is_ai:
                    pos = screen_to_board(event.pos[0], event.pos[1])
                    if pos and not self.board.is_occupied(pos[0], pos[1]):
                        self.place_player_boat(current_player, pos[0], pos[1])
                        self.next_placement()
        
        # Fase de jogar cartas
        elif self.phase == 'play_cards':
            if not current_player.is_ai:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Clique nas cartas
                    current_player.hand.handle_click(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Confirma carta selecionada
                        card = current_player.hand.get_selected_card()
                        if card:
                            self.play_card(current_player, card)
                            self.next_card_player()
        
        # Fase de movimento
        elif self.phase == 'movement':
            if not current_player.is_ai and not current_player.has_moved:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = screen_to_board(event.pos[0], event.pos[1])
                    if pos and pos in self.board.highlight_cells:
                        self.move_player_boat(current_player, pos[0], pos[1])
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Pula movimento
                        current_player.has_moved = True
                        self.next_movement_player()
        
        return None
    
    def place_player_boat(self, player, x, y):
        """Posiciona o barco de um jogador"""
        player.create_boat(x, y)
        self.board.place_object(x, y, player.boat)
        self.show_message(f"Barco do Jogador {player.id + 1} posicionado em ({x}, {y})")
    
    def play_card(self, player, card):
        """Jogador joga uma carta"""
        if player.play_card(card):
            self.cards_played[player.id] = card
            self.show_message(f"Jogador {player.id + 1} jogou uma carta")
            return True
        return False
    
    def move_player_boat(self, player, x, y):
        """Move o barco de um jogador"""
        old_x, old_y = player.boat.get_position()
        
        if player.move_boat(x, y):
            # Atualiza o tabuleiro
            self.board.move_object(old_x, old_y, x, y)
            self.board.clear_highlights()
            
            self.show_message(f"Jogador {player.id + 1} moveu para ({x}, {y})")
            
            # Verifica próximo jogador
            self.next_movement_player()
    
    def next_placement(self):
        """Avança para o próximo jogador na fase de posicionamento"""
        self.current_player_index += 1
        
        if self.current_player_index >= len(self.players):
            # Todos posicionaram - inicia o jogo
            self.current_player_index = self.start_player_token
            self.phase = 'preparation'
            self.start_turn()
        else:
            # Próximo jogador posiciona
            current_player = self.players[self.current_player_index]
            
            if current_player.is_ai:
                # IA escolhe posição
                occupied = self.board.get_all_occupied_positions()
                pos = generate_random_position(set(occupied))
                if pos:
                    self.place_player_boat(current_player, pos[0], pos[1])
                    self.next_placement()
            else:
                self.show_message(f"Jogador {self.current_player_index + 1}, escolha onde colocar seu barco")
    
    def start_turn(self):
        """Inicia um novo turno"""
        self.show_message(f"Turno {self.turn_number} - Fase de Preparação")
        
        # Adiciona peixes
        num_fish_to_add = self.fish_to_add + 1
        occupied_positions = set(self.board.get_all_occupied_positions())
        
        for _ in range(num_fish_to_add):
            pos = generate_random_position(occupied_positions)
            if pos:
                x, y = pos
                fish = Fish(x, y)
                self.fish_list.append(fish)
                self.board.place_object(x, y, fish)
                occupied_positions.add(pos)
        
        self.fish_to_add = 0
        
        # Distribui cartas
        for player in self.players:
            while len(player.hand.cards) < 3:
                card = self.deck.draw_card()
                player.hand.add_card(card)
        
        # Inicia fase de jogar cartas
        self.phase = 'play_cards'
        self.current_player_index = self.start_player_token
        self.cards_played = {}
        
        # Reseta IA
        for player in self.players:
            if player.is_ai:
                player.ai_controller.reset_phase('play_cards')
        
        self.show_message(f"Fase de Cartas - Todos jogam uma carta (virada para baixo)")
    
    def next_card_player(self):
        """Avança para o próximo jogador na fase de cartas"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Verifica se todos jogaram
        if len(self.cards_played) == len(self.players):
            self.phase = 'movement'
            self.current_player_index = self.start_player_token
            self.show_highlights_for_current_player()
            
            # Reseta IA
            for player in self.players:
                if player.is_ai:
                    player.ai_controller.reset_phase('movement')
            
            self.show_message("Fase de Movimento - Mova seu barco")
    
    def show_highlights_for_current_player(self):
        """Mostra movimentos válidos para o jogador atual"""
        player = self.players[self.current_player_index]
        if player.boat and not player.has_moved:
            boat_x, boat_y = player.boat.get_position()
            valid_moves = self.board.get_valid_moves(boat_x, boat_y, player.boat.moves_remaining)
            self.board.highlight_moves(valid_moves)
    
    def next_movement_player(self):
        """Avança para o próximo jogador na fase de movimento"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Verifica se todos moveram
        all_moved = all(p.has_moved for p in self.players)
        
        if all_moved:
            self.phase = 'resolution'
            self.resolve_turn()
        else:
            # Mostra opções para o próximo jogador
            self.show_highlights_for_current_player()
    
    def resolve_turn(self):
        """Resolve o turno - move peixes e coleta"""
        self.show_message("Fase de Resolução")
        
        # Calcula vetor resultante das cartas
        total_vector = [0, 0]
        for player_id, card in self.cards_played.items():
            vector = card.get_vector()
            total_vector[0] += vector[0]
            total_vector[1] += vector[1]
            
            # Retorna carta ao baralho
            self.deck.return_card(card)
        
        # Move todos os peixes
        fish_out_of_bounds = []
        
        for fish in self.fish_list:
            old_x, old_y = fish.get_position()
            new_x = old_x + total_vector[0]
            new_y = old_y + total_vector[1]
            
            # Remove do tabuleiro atual
            self.board.remove_object(old_x, old_y)
            
            # Verifica se saiu do tabuleiro
            if not self.board.is_valid_position(new_x, new_y):
                fish_out_of_bounds.append(fish)
            else:
                # Move o peixe
                fish.set_target_position(new_x, new_y)
                fish.x = new_x
                fish.y = new_y
                self.board.place_object(new_x, new_y, fish)
        
        # Remove peixes que saíram
        for fish in fish_out_of_bounds:
            self.fish_list.remove(fish)
        
        self.fish_to_add += len(fish_out_of_bounds)
        
        # Coleta peixes
        self.collect_fish()
        
        # Verifica vitória
        self.check_victory()
        
        if not self.winner:
            # Prepara próximo turno
            self.end_turn()
    
    def collect_fish(self):
        """Coleta peixes próximos aos barcos"""
        collected = []
        
        for fish in self.fish_list:
            fish_x, fish_y = fish.get_position()
            closest_boat = None
            closest_distance = float('inf')
            
            # Encontra o barco mais próximo
            for player in self.players:
                if player.boat:
                    boat_x, boat_y = player.boat.get_position()
                    distance = manhattan_distance((boat_x, boat_y), (fish_x, fish_y))
                    
                    if distance <= COLLECTION_DISTANCE and distance < closest_distance:
                        closest_distance = distance
                        closest_boat = player
            
            # Coleta o peixe
            if closest_boat:
                closest_boat.collect_fish()
                collected.append(fish)
                self.board.remove_object(fish_x, fish_y)
                
                self.show_message(f"Jogador {closest_boat.id + 1} coletou um peixe! Total: {closest_boat.fish_collected}")
        
        # Remove peixes coletados
        for fish in collected:
            self.fish_list.remove(fish)
    
    def check_victory(self):
        """Verifica se algum jogador venceu"""
        winners = [p for p in self.players if p.is_winner()]
        
        if winners:
            if len(winners) == 1:
                self.winner = winners[0]
                self.show_message(f"Jogador {self.winner.id + 1} ({self.winner.name}) venceu!")
            else:
                # Empate
                self.winner = winners
                winner_names = ", ".join([f"Jogador {w.id + 1}" for w in winners])
                self.show_message(f"Empate entre {winner_names}!")
            
            self.phase = 'game_over'
    
    def end_turn(self):
        """Finaliza o turno"""
        # Atualiza jogadores
        for player in self.players:
            player.end_turn()
        
        # Passa o marcador de início
        self.start_player_token = (self.start_player_token + 1) % len(self.players)
        
        # Próximo turno
        self.turn_number += 1
        self.start_turn()
    
    def show_message(self, message):
        """Mostra uma mensagem temporária"""
        self.ui_message = message
        self.ui_message_timer = 3.0
    
    def update(self, dt):
        """Atualiza o jogo"""
        # Atualiza timer de mensagem
        if self.ui_message_timer > 0:
            self.ui_message_timer -= dt
        
        # Atualiza componentes
        self.board.update(dt)
        
        for player in self.players:
            player.update(dt)
        
        for fish in self.fish_list:
            fish.update(dt)
        
        # Atualiza IA
        current_player = self.players[self.current_player_index]
        
        if current_player.is_ai and self.phase in ['play_cards', 'movement']:
            game_state = self.get_game_state()
            current_player.ai_controller.update(dt, game_state, self.phase)
            
            # Verifica se a IA tomou decisão
            if self.phase == 'play_cards':
                if current_player.ai_controller.card_ai.decision_made and not current_player.has_played_card:
                    card = current_player.ai_controller.choose_card(game_state)
                    if card:
                        self.play_card(current_player, card)
                        self.next_card_player()
            
            elif self.phase == 'movement':
                if current_player.ai_controller.movement_ai.decision_made and not current_player.has_moved:
                    move = current_player.ai_controller.choose_move(game_state)
                    if move:
                        self.move_player_boat(current_player, move[0], move[1])
                    else:
                        # IA pula o movimento
                        current_player.has_moved = True
                        self.next_movement_player()
        
        # Atualiza mouse para hover nas cartas
        if not current_player.is_ai and self.phase == 'play_cards':
            mouse_pos = pygame.mouse.get_pos()
            current_player.hand.update(mouse_pos)
    
    def get_game_state(self):
        """Retorna o estado atual do jogo para a IA"""
        current_player = self.players[self.current_player_index]
        
        # Posições dos peixes
        fish_positions = [fish.get_position() for fish in self.fish_list]
        
        # Outros barcos
        other_boats = [p.boat for p in self.players if p.boat and p != current_player]
        
        # Movimentos válidos
        valid_moves = []
        if current_player.boat and self.phase == 'movement':
            boat_x, boat_y = current_player.boat.get_position()
            valid_moves = self.board.get_valid_moves(boat_x, boat_y, current_player.boat.moves_remaining)
        
        # Posições previstas dos peixes (após movimento)
        predicted_fish = []
        if self.cards_played:
            total_vector = [0, 0]
            for card in self.cards_played.values():
                vector = card.get_vector()
                total_vector[0] += vector[0]
                total_vector[1] += vector[1]
            
            for fish_pos in fish_positions:
                new_pos = (fish_pos[0] + total_vector[0], fish_pos[1] + total_vector[1])
                if self.board.is_valid_position(new_pos[0], new_pos[1]):
                    predicted_fish.append(new_pos)
        
        return {
            'fish_positions': fish_positions,
            'other_boats': other_boats,
            'valid_moves': valid_moves,
            'predicted_fish_positions': predicted_fish,
            'cards_played': self.cards_played,
            'turn_number': self.turn_number
        }
    
    def draw(self):
        """Desenha o jogo"""
        # Fundo
        self.screen.fill(COLORS['BACKGROUND'])
        
        # Tabuleiro
        self.board.draw(self.screen)
        
        # Peixes
        for fish in self.fish_list:
            fish.draw(self.screen)
        
        # Barcos
        for player in self.players:
            if player.boat:
                player.boat.draw(self.screen)
        
        # UI - Informações do jogo
        info_x = BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE + 50
        info_y = BOARD_OFFSET_Y
        
        # Título
        draw_text(self.screen, "CAÇADOR DOS MARES", info_x, info_y, 
                 size=32, color=COLORS['WHITE'])
        
        # Turno
        draw_text(self.screen, f"Turno: {self.turn_number}", info_x, info_y + 50,
                 size=24, color=COLORS['WHITE'])
        
        # Fase
        phase_text = {
            'placement': 'Posicionamento',
            'preparation': 'Preparação',
            'play_cards': 'Jogar Cartas',
            'movement': 'Movimento',
            'resolution': 'Resolução',
            'game_over': 'Fim de Jogo'
        }
        draw_text(self.screen, f"Fase: {phase_text.get(self.phase, self.phase)}", 
                 info_x, info_y + 80, size=20, color=COLORS['YELLOW'])
        
        # Jogadores
        draw_text(self.screen, "Jogadores:", info_x, info_y + 120, 
                 size=24, color=COLORS['WHITE'])
        
        for i, player in enumerate(self.players):
            y_pos = info_y + 150 + i * 80
            
            # Fundo do jogador
            player_rect = pygame.Rect(info_x - 10, y_pos - 5, 300, 70)
            if i == self.current_player_index and self.phase != 'game_over':
                pygame.draw.rect(self.screen, (50, 50, 100), player_rect)
            pygame.draw.rect(self.screen, player.color, player_rect, 3)
            
            # Nome
            name_text = f"{player.name}"
            if player.is_ai:
                name_text += " (IA)"
            draw_text(self.screen, name_text, info_x, y_pos,
                     size=20, color=player.color)
            
            # Peixes coletados
            draw_text(self.screen, f"Peixes: {player.fish_collected}/{WINNING_FISH_COUNT}",
                     info_x, y_pos + 25, size=18, color=COLORS['WHITE'])
            
            # Movimentos restantes
            if player.boat:
                draw_text(self.screen, f"Movimentos: {player.boat.moves_remaining}",
                         info_x + 150, y_pos + 25, size=18, color=COLORS['WHITE'])
        
        # Cartas (apenas para jogadores humanos ou na fase de resolução)
        if self.phase == 'play_cards':
            current_player = self.players[self.current_player_index]
            if not current_player.is_ai:
                current_player.draw_hand(self.screen, 50, WINDOW_HEIGHT - 180, True)
        
        elif self.phase == 'resolution':
            # Mostra todas as cartas jogadas
            draw_text(self.screen, "Cartas Jogadas:", 50, WINDOW_HEIGHT - 200,
                     size=24, color=COLORS['WHITE'])
            
            x_offset = 50
            for player_id, card in self.cards_played.items():
                card.set_position(x_offset, WINDOW_HEIGHT - 170)
                card.draw(self.screen, face_up=True)
                
                # Nome do jogador
                player_name = self.players[player_id].name
                draw_text(self.screen, player_name, x_offset + 40, WINDOW_HEIGHT - 40,
                         size=16, color=self.players[player_id].color, center=True)
                
                x_offset += 100
        
        # Mensagem
        if self.ui_message and self.ui_message_timer > 0:
            # Fundo da mensagem
            msg_rect = pygame.Rect(WINDOW_WIDTH // 2 - 300, 10, 600, 50)
            pygame.draw.rect(self.screen, (30, 30, 50), msg_rect)
            pygame.draw.rect(self.screen, COLORS['WHITE'], msg_rect, 2)
            
            draw_text(self.screen, self.ui_message, WINDOW_WIDTH // 2, 35,
                     size=24, color=COLORS['WHITE'], center=True)
        
        # Tela de fim de jogo
        if self.phase == 'game_over':
            # Overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Mensagem de vitória
            if isinstance(self.winner, list):
                draw_text(self.screen, "EMPATE!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100,
                         size=64, color=COLORS['YELLOW'], center=True)
            else:
                draw_text(self.screen, "VITÓRIA!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100,
                         size=64, color=COLORS['YELLOW'], center=True)
                draw_text(self.screen, f"{self.winner.name}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30,
                         size=48, color=self.winner.color, center=True)
            
            # Estatísticas
            y_offset = WINDOW_HEIGHT // 2 + 50
            for player in self.players:
                stats = player.get_stats()
                stats_text = f"{stats['name']}: {stats['fish_collected']} peixes, {stats['turns_played']} turnos"
                draw_text(self.screen, stats_text, WINDOW_WIDTH // 2, y_offset,
                         size=24, color=player.color, center=True)
                y_offset += 40
            
            # Instruções
            draw_text(self.screen, "Pressione ESC para voltar ao menu", 
                     WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50,
                     size=20, color=COLORS['WHITE'], center=True)