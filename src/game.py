# src/game.py - Jogo com UI responsiva completa

import pygame
import random
from config import *
from src.board import Board
from src.player import Player
from src.fish import Fish, fish_manager
from src.card import CardDeck
from src.card_system import CardHand, VisualCard
from src.ai import AIController
from src.layout_manager import layout_manager
from src.utils import *

class Game:
    """Classe principal do jogo com UI responsiva"""
    
    def __init__(self, screen, host_player, num_players=2, ai_difficulty='MEDIO'):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Inicializa sprites
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
        
        # Componentes do jogo responsivos
        self.board = Board()
        self.players = []
        self.deck = CardDeck()
        
        # Estado do jogo
        self.current_player_index = 0
        self.turn_number = 1
        self.phase = 'setup'
        self.winner = None
        
        # Controle de turnos
        self.start_player_token = 0
        self.cards_played = {}
        self.fish_to_add = 0
        
        # UI responsiva
        self.ui_message = ""
        self.ui_message_timer = 0
        self.card_hands = {}  # Mãos visuais dos jogadores
        self.selected_card_index = -1
        
        # Animações
        self.animations = []
        self.ui_scale = 1.0
        
        # Inicializa jogadores e UI
        self.setup_players(host_player)
        self.setup_responsive_ui()
        self.setup_game()
    
    def setup_responsive_ui(self):
        """Configura UI responsiva"""
        # Cria mãos de cartas visuais para cada jogador
        for i, player in enumerate(self.players):
            hand = CardHand()
            # Adiciona cartas de exemplo (serão substituídas pelo deck real)
            example_vectors = [(1, 0), (0, 1), (-1, 0)]
            for vector in example_vectors:
                hand.add_card(vector)
            self.card_hands[i] = hand
    
    def setup_players(self, host_player):
        """Configura os jogadores"""
        # Jogador principal
        player = Player(0, host_player, COLORS['PLAYER_COLORS'][0], is_ai=False)
        self.players.append(player)
        
        # Jogadores IA
        for i in range(1, self.num_players):
            ai_name = f"IA {i}"
            player = Player(i, ai_name, COLORS['PLAYER_COLORS'][i], is_ai=True)
            player.ai_controller = AIController(player, self.ai_difficulty)
            self.players.append(player)
    
    def setup_game(self):
        """Inicializa o jogo"""
        # Adiciona peixes iniciais
        occupied = []
        
        for _ in range(self.num_players):
            pos = generate_random_position(occupied)
            if pos:
                fish_manager.add_fish(pos[0], pos[1])
                occupied.append(pos)
        
        self.phase = 'setup'
        self.show_message("Posicione seus barcos no tabuleiro")
    
    def update_screen_size(self, width, height):
        """Atualiza tamanho da tela para responsividade"""
        layout_manager.update_screen_size(width, height)
        self.board.update_screen_size(width, height)
        
        # Atualiza escala da UI
        self.ui_scale = layout_manager.get_element_scale_factor()
    
    def get_ui_areas(self):
        """Retorna áreas da UI responsiva"""
        screen_width, screen_height = self.screen.get_size()
        layout_manager.update_screen_size(screen_width, screen_height)
        
        ui_area = layout_manager.get_ui_area()
        board_area = layout_manager.get_board_area()
        
        # Área de informações do jogo (parte superior da UI)
        info_area = {
            'x': ui_area['x'],
            'y': ui_area['y'],
            'width': ui_area['width'],
            'height': ui_area['height'] // 2
        }
        
        # Área de cartas (parte inferior)
        card_area = {
            'x': board_area['x'],
            'y': board_area['y'] + board_area['height'] + 20,
            'width': board_area['width'],
            'height': screen_height - (board_area['y'] + board_area['height'] + 40)
        }
        
        return {
            'board': board_area,
            'ui': ui_area,
            'info': info_area,
            'cards': card_area
        }
    
    def handle_event(self, event):
        """Processa eventos do jogo"""
        if event.type == pygame.VIDEORESIZE:
            self.update_screen_size(event.w, event.h)
            return None
        
        areas = self.get_ui_areas()
        current_player = self.players[self.current_player_index]
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            # Verifica clique no tabuleiro
            board_pos = self.board.screen_to_board(mouse_pos[0], mouse_pos[1])
            if board_pos:
                return self.handle_board_click(board_pos[0], board_pos[1])
            
            # Verifica clique nas cartas
            if self.phase == 'play_cards' and not current_player.is_ai:
                return self.handle_card_click(mouse_pos)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'pause'
            elif event.key == pygame.K_SPACE and self.phase == 'movement':
                # Pula movimento
                if not current_player.is_ai and not current_player.has_moved:
                    current_player.has_moved = True
                    self.next_movement_player()
        
        return None
    
    def handle_board_click(self, x, y):
        """Processa clique no tabuleiro"""
        current_player = self.players[self.current_player_index]
        
        if self.phase == 'setup' and not current_player.boat:
            # Posiciona barco
            if not self.board.is_occupied(x, y):
                self.place_player_boat(current_player, x, y)
                self.next_setup_player()
        
        elif self.phase == 'movement' and not current_player.is_ai:
            # Move barco
            if not current_player.has_moved and current_player.boat:
                boat_pos = current_player.boat.get_position()
                if (x, y) in self.board.highlight_cells:
                    self.move_player_boat(current_player, x, y)
        
        return None
    
    def handle_card_click(self, mouse_pos):
        """Processa clique nas cartas"""
        current_player = self.players[self.current_player_index]
        
        if current_player.is_ai or current_player.has_played_card:
            return None
        
        # Verifica clique na mão do jogador atual
        hand = self.card_hands.get(self.current_player_index)
        if hand:
            clicked_index = hand.handle_click(mouse_pos)
            if clicked_index >= 0:
                selected_card = hand.get_selected_card()
                if selected_card:
                    # Confirma jogada da carta
                    # TODO: Implementar confirmação
                    pass
        
        return None
    
    def next_setup_player(self):
        """Próximo jogador no setup"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Verifica se todos posicionaram
        if all(p.boat for p in self.players):
            self.start_turn()
    
    def place_player_boat(self, player, x, y):
        """Posiciona barco do jogador"""
        player.create_boat(x, y)
        self.board.place_object(x, y, player.boat)
        self.show_message(f"Barco do {player.name} posicionado!")
    
    def move_player_boat(self, player, x, y):
        """Move barco do jogador"""
        old_pos = player.boat.get_position()
        
        if player.move_boat(x, y):
            self.board.move_object(old_pos[0], old_pos[1], x, y)
            self.board.clear_highlights()
            self.next_movement_player()
    
    def start_turn(self):
        """Inicia novo turno"""
        self.phase = 'preparation'
        
        # Distribui cartas
        for player in self.players:
            while len(player.hand.cards) < 3:
                card = self.deck.draw_card()
                if card:
                    player.hand.add_card(card)
        
        # Atualiza mãos visuais
        self.update_visual_hands()
        
        self.phase = 'play_cards'
        self.current_player_index = self.start_player_token
        self.show_message("Escolha uma carta para jogar")
    
    def update_visual_hands(self):
        """Atualiza mãos visuais com cartas reais"""
        for i, player in enumerate(self.players):
            if i in self.card_hands:
                hand = self.card_hands[i]
                hand.cards.clear()
                
                # Adiciona cartas do deck real
                for card in player.hand.cards:
                    hand.add_card(card.get_vector())
    
    def next_movement_player(self):
        """Próximo jogador no movimento"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Verifica se todos moveram
        if all(p.has_moved for p in self.players):
            self.resolve_turn()
        else:
            # Destaca movimentos do próximo jogador
            self.show_highlights_for_current_player()
    
    def show_highlights_for_current_player(self):
        """Mostra movimentos válidos"""
        player = self.players[self.current_player_index]
        if player.boat and not player.has_moved:
            pos = player.boat.get_position()
            valid_moves = self.board.get_valid_moves(pos[0], pos[1], player.boat.moves_remaining)
            self.board.highlight_moves(valid_moves)
    
    def resolve_turn(self):
        """Resolve turno"""
        # Calcula vetor resultante
        total_vector = [0, 0]
        for player_id, card in self.cards_played.items():
            vector = card.get_vector()
            total_vector[0] += vector[0]
            total_vector[1] += vector[1]
        
        # Move peixes
        fish_manager.move_all_fish(total_vector)
        
        # Coleta peixes
        self.collect_fish()
        
        # Próximo turno ou fim de jogo
        if not self.check_victory():
            self.end_turn()
    
    def collect_fish(self):
        """Coleta peixes próximos"""
        for fish in fish_manager.fish_list[:]:
            fish_pos = fish.get_position()
            closest_player = None
            closest_distance = float('inf')
            
            for player in self.players:
                if player.boat:
                    boat_pos = player.boat.get_position()
                    distance = manhattan_distance(boat_pos, fish_pos)
                    
                    if distance <= COLLECTION_DISTANCE and distance < closest_distance:
                        closest_distance = distance
                        closest_player = player
            
            if closest_player:
                closest_player.collect_fish()
                fish_manager.remove_fish(fish)
                self.show_message(f"{closest_player.name} coletou um peixe!")
    
    def check_victory(self):
        """Verifica vitória"""
        winners = [p for p in self.players if p.fish_collected >= WINNING_FISH_COUNT]
        
        if winners:
            self.winner = winners[0] if len(winners) == 1 else winners
            self.phase = 'game_over'
            return True
        return False
    
    def end_turn(self):
        """Finaliza turno"""
        for player in self.players:
            player.end_turn()
        
        self.start_player_token = (self.start_player_token + 1) % len(self.players)
        self.turn_number += 1
        self.cards_played.clear()
        self.start_turn()
    
    def show_message(self, message):
        """Mostra mensagem temporária"""
        self.ui_message = message
        self.ui_message_timer = 3.0
    
    def update(self, dt):
        """Atualiza o jogo"""
        # Atualiza responsividade
        screen_size = self.screen.get_size()
        layout_manager.update_screen_size(screen_size[0], screen_size[1])
        
        # Atualiza timer de mensagem
        if self.ui_message_timer > 0:
            self.ui_message_timer -= dt
        
        # Atualiza componentes
        self.board.update(dt)
        fish_manager.update(dt)
        
        for player in self.players:
            if hasattr(player, 'update'):
                player.update(dt)
        
        # Atualiza mãos de cartas
        mouse_pos = pygame.mouse.get_pos()
        for hand in self.card_hands.values():
            hand.update(dt, mouse_pos)
        
        # Atualiza IA
        current_player = self.players[self.current_player_index]
        if current_player.is_ai and hasattr(current_player, 'ai_controller'):
            # TODO: Implementar lógica de IA
            pass
    
    def draw(self):
        """Desenha o jogo com UI responsiva"""
        # Limpa tela
        self.screen.fill(COLORS['BACKGROUND'])
        
        # Desenha tabuleiro
        self.board.draw(self.screen)
        
        # Desenha peixes
        fish_manager.draw(self.screen)
        
        # Desenha barcos
        for player in self.players:
            if player.boat:
                player.boat.draw(self.screen)
        
        # Desenha UI responsiva
        self.draw_responsive_ui()
        
        # Desenha cartas
        self.draw_cards()
        
        # Desenha mensagens
        self.draw_messages()
    
    def draw_responsive_ui(self):
        """Desenha interface responsiva"""
        areas = self.get_ui_areas()
        info_area = areas['info']
        
        # Fundo da UI
        ui_bg = pygame.Rect(info_area['x'], info_area['y'], 
                           info_area['width'], info_area['height'])
        pygame.draw.rect(self.screen, (30, 60, 90), ui_bg)
        pygame.draw.rect(self.screen, COLORS['WHITE'], ui_bg, 2)
        
        # Título
        font_size = layout_manager.get_font_size(32)
        draw_text(self.screen, "CAÇADOR DOS MARES", 
                 info_area['x'] + 20, info_area['y'] + 20,
                 size=font_size, color=COLORS['WHITE'])
        
        # Turno
        font_size = layout_manager.get_font_size(24)
        draw_text(self.screen, f"Turno: {self.turn_number}", 
                 info_area['x'] + 20, info_area['y'] + 60,
                 size=font_size, color=COLORS['WHITE'])
        
        # Fase
        phase_names = {
            'setup': 'Posicionamento',
            'preparation': 'Preparação',
            'play_cards': 'Jogar Cartas',
            'movement': 'Movimento',
            'resolution': 'Resolução',
            'game_over': 'Fim de Jogo'
        }
        
        phase_text = phase_names.get(self.phase, self.phase)
        font_size = layout_manager.get_font_size(20)
        draw_text(self.screen, f"Fase: {phase_text}", 
                 info_area['x'] + 20, info_area['y'] + 90,
                 size=font_size, color=COLORS['YELLOW'])
        
        # Informações dos jogadores
        y_offset = 130
        for i, player in enumerate(self.players):
            is_current = (i == self.current_player_index)
            color = player.color if not is_current else COLORS['YELLOW']
            
            player_text = f"{player.name}: {player.fish_collected} peixes"
            font_size = layout_manager.get_font_size(18)
            draw_text(self.screen, player_text,
                     info_area['x'] + 20, info_area['y'] + y_offset,
                     size=font_size, color=color)
            y_offset += 30
    
    def draw_cards(self):
        """Desenha cartas na parte inferior"""
        areas = self.get_ui_areas()
        card_area = areas['cards']
        
        # Desenha mão do jogador atual se for humano
        current_player = self.players[self.current_player_index]
        if not current_player.is_ai and self.current_player_index in self.card_hands:
            hand = self.card_hands[self.current_player_index]
            
            # Posição centralizada na área de cartas
            center_x = card_area['x'] + card_area['width'] // 2
            center_y = card_area['y'] + card_area['height'] // 2
            
            hand.draw(self.screen, center_x, center_y)
    
    def draw_messages(self):
        """Desenha mensagens temporárias"""
        if self.ui_message and self.ui_message_timer > 0:
            screen_width, screen_height = self.screen.get_size()
            
            # Posição centralizada
            font_size = layout_manager.get_font_size(24)
            
            # Calcula alpha baseado no tempo restante
            alpha = min(255, int(255 * self.ui_message_timer / 3.0))
            
            # Desenha fundo semi-transparente
            font = pygame.font.Font(None, font_size)
            text_surface = font.render(self.ui_message, True, COLORS['WHITE'])
            text_rect = text_surface.get_rect()
            text_rect.centerx = screen_width // 2
            text_rect.centery = screen_height // 4
            
            # Fundo
            bg_rect = text_rect.inflate(40, 20)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.set_alpha(alpha // 2)
            bg_surface.fill((0, 0, 0))
            
            self.screen.blit(bg_surface, bg_rect)
            
            # Texto com transparência
            text_surface.set_alpha(alpha)
            self.screen.blit(text_surface, text_rect)
