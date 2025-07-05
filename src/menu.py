# src/menu.py - Menu principal do jogo

import pygame
import pygame_menu
from pygame_menu import themes
from config import *
from src.game import Game
from src.network import NetworkGame, GameServer
from src.story import StoryMode
from src.achievements import AchievementScreen

class MainMenu:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.clock = pygame.time.Clock()
        
        # Estado
        self.current_game = None
        self.server = None
        
        # Cria o tema customizado
        mytheme = themes.THEME_BLUE.copy()
        mytheme.title_background_color = (30, 80, 120)
        mytheme.widget_font_color = COLORS['WHITE']
        mytheme.widget_selection_color = COLORS['YELLOW']
        mytheme.widget_font_size = 25
        
        # Menu principal
        self.menu = pygame_menu.Menu(
            'Caçador dos Mares',
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            theme=mytheme
        )
        
        # Adiciona widgets
        self.menu.add.label(f'Bem-vindo, {username}!', font_size=30)
        self.menu.add.vertical_margin(30)
        
        self.menu.add.button('Jogar Solo', self.start_single_player)
        self.menu.add.button('Criar Sala Multiplayer', self.create_multiplayer_room)
        self.menu.add.button('Entrar em Sala', self.join_multiplayer_room)
        self.menu.add.button('Modo História', self.start_story_mode)
        self.menu.add.button('Conquistas', self.show_achievements)
        self.menu.add.button('Configurações', self.show_settings)
        self.menu.add.button('Sair', pygame_menu.events.EXIT)
        
        # Menus secundários
        self.create_single_player_menu()
        self.create_multiplayer_menu()
        self.create_settings_menu()
        
    def create_single_player_menu(self):
        """Cria o menu de jogo solo"""
        self.single_player_menu = pygame_menu.Menu(
            'Configurar Partida',
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            theme=self.menu.get_theme()
        )
        
        # Número de jogadores IA
        self.ai_players = 1
        self.single_player_menu.add.selector(
            'Jogadores IA: ',
            [('1', 1), ('2', 2), ('3', 3)],
            onchange=self.set_ai_players
        )
        
        # Dificuldade
        self.ai_difficulty = 'MEDIO'
        self.single_player_menu.add.selector(
            'Dificuldade: ',
            [('Fácil', 'FACIL'), ('Médio', 'MEDIO'), ('Difícil', 'DIFICIL')],
            onchange=self.set_ai_difficulty
        )
        
        self.single_player_menu.add.vertical_margin(30)
        self.single_player_menu.add.button('Iniciar', self.start_solo_game)
        self.single_player_menu.add.button('Voltar', self.back_to_main)
        
    def create_multiplayer_menu(self):
        """Cria o menu multiplayer"""
        self.multiplayer_menu = pygame_menu.Menu(
            'Multiplayer',
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            theme=self.menu.get_theme()
        )
        
        # Criar sala
        self.room_name = ""
        self.port = str(DEFAULT_PORT)
        
        self.multiplayer_menu.add.text_input(
            'Nome da Sala: ',
            default='',
            onchange=self.set_room_name
        )
        
        self.multiplayer_menu.add.text_input(
            'Porta: ',
            default=str(DEFAULT_PORT),
            onchange=self.set_port,
            input_type=pygame_menu.locals.INPUT_INT
        )
        
        self.multiplayer_menu.add.vertical_margin(30)
        self.multiplayer_menu.add.button('Criar Sala', self.create_room)
        
        # Entrar em sala
        self.server_ip = "localhost"
        self.multiplayer_menu.add.vertical_margin(50)
        self.multiplayer_menu.add.label('Entrar em Sala Existente:', font_size=28)
        
        self.multiplayer_menu.add.text_input(
            'IP do Servidor: ',
            default='localhost',
            onchange=self.set_server_ip
        )
        
        self.multiplayer_menu.add.button('Conectar', self.connect_to_room)
        self.multiplayer_menu.add.vertical_margin(30)
        self.multiplayer_menu.add.button('Voltar', self.back_to_main)
        
    def create_settings_menu(self):
        """Cria o menu de configurações"""
        self.settings_menu = pygame_menu.Menu(
            'Configurações',
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            theme=self.menu.get_theme()
        )
        
        # Volume
        self.volume = 70
        self.settings_menu.add.slider(
            'Volume: ',
            default=70,
            range=(0, 100),
            onchange=self.set_volume
        )
        
        # Tela cheia
        self.fullscreen = False
        self.settings_menu.add.toggle_switch(
            'Tela Cheia: ',
            default=False,
            onchange=self.toggle_fullscreen
        )
        
        self.settings_menu.add.vertical_margin(50)
        self.settings_menu.add.button('Voltar', self.back_to_main)
        
    def set_ai_players(self, value, players):
        self.ai_players = players
        
    def set_ai_difficulty(self, value, difficulty):
        self.ai_difficulty = difficulty
        
    def set_room_name(self, value):
        self.room_name = value
        
    def set_port(self, value):
        self.port = value
        
    def set_server_ip(self, value):
        self.server_ip = value
        
    def set_volume(self, value):
        self.volume = value
        pygame.mixer.music.set_volume(value / 100)
        
    def toggle_fullscreen(self, value):
        self.fullscreen = value
        if value:
            pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    def start_single_player(self):
        """Abre o menu de configuração do jogo solo"""
        self.single_player_menu.mainloop(self.screen)
        
    def start_solo_game(self):
        """Inicia um jogo solo"""
        self.current_game = Game(self.screen, self.username, 
                                self.ai_players + 1, self.ai_difficulty)
        self.single_player_menu.disable()
        
    def create_multiplayer_room(self):
        """Abre o menu multiplayer para criar sala"""
        self.multiplayer_menu.mainloop(self.screen)
        
    def join_multiplayer_room(self):
        """Abre o menu multiplayer para entrar em sala"""
        self.multiplayer_menu.mainloop(self.screen)
        
    def create_room(self):
        """Cria uma sala multiplayer"""
        if not self.room_name:
            return
            
        try:
            self.server = GameServer(int(self.port), self.room_name)
            self.server.start()
            
            # Conecta como host
            self.current_game = NetworkGame(self.screen, self.username, 
                                          'localhost', int(self.port), is_host=True)
            self.multiplayer_menu.disable()
        except Exception as e:
            print(f"Erro ao criar sala: {e}")
            
    def connect_to_room(self):
        """Conecta a uma sala multiplayer"""
        try:
            self.current_game = NetworkGame(self.screen, self.username,
                                          self.server_ip, int(self.port), is_host=False)
            self.multiplayer_menu.disable()
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            
    def start_story_mode(self):
        """Inicia o modo história"""
        self.current_game = StoryMode(self.screen, self.username)
        self.menu.disable()
        
    def show_achievements(self):
        """Mostra a tela de conquistas"""
        achievements_screen = AchievementScreen(self.screen, self.username)
        achievements_screen.run()
        
    def show_settings(self):
        """Abre o menu de configurações"""
        self.settings_menu.mainloop(self.screen)
        
    def back_to_main(self):
        """Volta ao menu principal"""
        if hasattr(self, 'single_player_menu'):
            self.single_player_menu.disable()
        if hasattr(self, 'multiplayer_menu'):
            self.multiplayer_menu.disable()
        if hasattr(self, 'settings_menu'):
            self.settings_menu.disable()
    
    def handle_event(self, event):
        """Processa eventos"""
        if self.current_game:
            result = self.current_game.handle_event(event)
            if result == 'quit':
                self.current_game = None
                if self.server:
                    self.server.stop()
                    self.server = None
                self.menu.enable()
                return None
            return result
        
        if self.menu.is_enabled():
            self.menu.update([event])
            
        return None
    
    def update(self, dt):
        """Atualiza o menu ou jogo atual"""
        if self.current_game:
            self.current_game.update(dt)
    
    def draw(self):
        """Desenha o menu ou jogo atual"""
        if self.current_game:
            self.current_game.draw()
        elif self.menu.is_enabled():
            self.menu.draw(self.screen)