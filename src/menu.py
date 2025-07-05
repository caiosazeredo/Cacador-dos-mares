# src/menu.py - Menu principal do jogo (corrigido)

import pygame
import sys
from config import *
from src.game import Game
from src.story import StoryMode
from src.achievements import AchievementScreen
from src.utils import draw_text, draw_button, create_gradient_surface

class MainMenu:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.clock = pygame.time.Clock()
        
        # Estado
        self.current_game = None
        self.current_submenu = None
        
        # Configurações para jogo solo
        self.ai_players = 1
        self.ai_difficulty = 'MEDIO'
        
        # Configurações multiplayer
        self.room_name = ""
        self.server_ip = "localhost"
        self.port = DEFAULT_PORT
        
        # Visual
        self.background = create_gradient_surface(WINDOW_WIDTH, WINDOW_HEIGHT,
                                                (20, 60, 100), (40, 120, 180))
        
        # Botões do menu principal
        self.main_buttons = [
            {'text': 'Jogar Solo', 'action': 'single_player', 'y': 250},
            {'text': 'Modo História', 'action': 'story', 'y': 310},
            {'text': 'Conquistas', 'action': 'achievements', 'y': 370},
            {'text': 'Configurações', 'action': 'settings', 'y': 430},
            {'text': 'Sair', 'action': 'quit', 'y': 490}
        ]
        
        # Botões do submenu solo
        self.solo_buttons = [
            {'text': 'Iniciar', 'action': 'start_solo', 'y': 400},
            {'text': 'Voltar', 'action': 'back', 'y': 460}
        ]
        
        print(f"Menu principal inicializado para {username}")
        
    def handle_event(self, event):
        """Processa eventos"""
        if self.current_game:
            result = self.current_game.handle_event(event)
            if result == 'quit':
                self.current_game = None
                return None
            return result
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.current_submenu:
                    self.current_submenu = None
                else:
                    return 'quit'
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                return self.handle_click(event.pos)
        
        return None
    
    def handle_click(self, pos):
        """Processa cliques do mouse"""
        mouse_x, mouse_y = pos
        
        if self.current_submenu == 'single_player':
            return self.handle_solo_menu_click(mouse_x, mouse_y)
        elif self.current_submenu == 'settings':
            return self.handle_settings_click(mouse_x, mouse_y)
        else:
            return self.handle_main_menu_click(mouse_x, mouse_y)
    
    def handle_main_menu_click(self, mouse_x, mouse_y):
        """Processa cliques no menu principal"""
        button_width = 200
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        
        for button in self.main_buttons:
            button_rect = pygame.Rect(button_x, button['y'], button_width, button_height)
            
            if button_rect.collidepoint(mouse_x, mouse_y):
                action = button['action']
                
                if action == 'single_player':
                    self.current_submenu = 'single_player'
                elif action == 'story':
                    self.start_story_mode()
                elif action == 'achievements':
                    self.show_achievements()
                elif action == 'settings':
                    self.current_submenu = 'settings'
                elif action == 'quit':
                    return 'quit'
                
                return None
        
        return None
    
    def handle_solo_menu_click(self, mouse_x, mouse_y):
        """Processa cliques no menu de jogo solo"""
        button_width = 200
        button_height = 40
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        
        # Botões de configuração
        # Número de jogadores IA
        ai_buttons_y = 280
        for i, count in enumerate([1, 2, 3]):
            btn_x = WINDOW_WIDTH // 2 - 120 + i * 80
            btn_rect = pygame.Rect(btn_x, ai_buttons_y, 60, 30)
            
            if btn_rect.collidepoint(mouse_x, mouse_y):
                self.ai_players = count
                return None
        
        # Dificuldade
        diff_buttons_y = 340
        difficulties = [('Fácil', 'FACIL'), ('Médio', 'MEDIO'), ('Difícil', 'DIFICIL')]
        for i, (name, diff) in enumerate(difficulties):
            btn_x = WINDOW_WIDTH // 2 - 150 + i * 100
            btn_rect = pygame.Rect(btn_x, diff_buttons_y, 90, 30)
            
            if btn_rect.collidepoint(mouse_x, mouse_y):
                self.ai_difficulty = diff
                return None
        
        # Botões de ação
        for button in self.solo_buttons:
            button_rect = pygame.Rect(button_x, button['y'], button_width, button_height)
            
            if button_rect.collidepoint(mouse_x, mouse_y):
                action = button['action']
                
                if action == 'start_solo':
                    self.start_solo_game()
                elif action == 'back':
                    self.current_submenu = None
                
                return None
        
        return None
    
    def handle_settings_click(self, mouse_x, mouse_y):
        """Processa cliques no menu de configurações"""
        button_width = 200
        button_height = 40
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        
        # Botão voltar
        back_rect = pygame.Rect(button_x, 400, button_width, button_height)
        if back_rect.collidepoint(mouse_x, mouse_y):
            self.current_submenu = None
        
        return None
    
    def start_solo_game(self):
        """Inicia um jogo solo"""
        print(f"Iniciando jogo solo: {self.ai_players + 1} jogadores, dificuldade {self.ai_difficulty}")
        try:
            self.current_game = Game(self.screen, self.username, 
                                    self.ai_players + 1, self.ai_difficulty)
            self.current_submenu = None
            print("Jogo solo iniciado com sucesso")
        except Exception as e:
            print(f"Erro ao iniciar jogo solo: {e}")
    
    def start_story_mode(self):
        """Inicia o modo história"""
        print("Iniciando modo história")
        try:
            self.current_game = StoryMode(self.screen, self.username)
            print("Modo história iniciado com sucesso")
        except Exception as e:
            print(f"Erro ao iniciar modo história: {e}")
    
    def show_achievements(self):
        """Mostra a tela de conquistas"""
        print("Abrindo conquistas")
        try:
            achievements_screen = AchievementScreen(self.screen, self.username)
            achievements_screen.run()
            print("Tela de conquistas fechada")
        except Exception as e:
            print(f"Erro na tela de conquistas: {e}")
    
    def update(self, dt):
        """Atualiza o menu ou jogo atual"""
        if self.current_game:
            try:
                self.current_game.update(dt)
            except Exception as e:
                print(f"Erro ao atualizar jogo: {e}")
                self.current_game = None
    
    def draw(self):
        """Desenha o menu ou jogo atual"""
        if self.current_game:
            try:
                self.current_game.draw()
            except Exception as e:
                print(f"Erro ao desenhar jogo: {e}")
                self.current_game = None
        else:
            self.draw_menu()
    
    def draw_menu(self):
        """Desenha o menu"""
        # Fundo
        self.screen.blit(self.background, (0, 0))
        
        if self.current_submenu == 'single_player':
            self.draw_solo_menu()
        elif self.current_submenu == 'settings':
            self.draw_settings_menu()
        else:
            self.draw_main_menu()
    
    def draw_main_menu(self):
        """Desenha o menu principal"""
        # Título
        draw_text(self.screen, "CAÇADOR DOS MARES", WINDOW_WIDTH // 2, 100,
                 size=48, color=COLORS['WHITE'], center=True)
        
        # Bem-vindo
        draw_text(self.screen, f"Bem-vindo, {self.username}!", WINDOW_WIDTH // 2, 160,
                 size=24, color=COLORS['YELLOW'], center=True)
        
        # Botões
        button_width = 200
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.main_buttons:
            button_rect = pygame.Rect(button_x, button['y'], button_width, button_height)
            
            # Cor do botão
            if button_rect.collidepoint(mouse_pos):
                color = (70, 70, 120)
                text_color = COLORS['YELLOW']
            else:
                color = (50, 50, 100)
                text_color = COLORS['WHITE']
            
            # Desenha botão
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, COLORS['WHITE'], button_rect, 2)
            
            # Texto do botão
            draw_text(self.screen, button['text'], 
                     button_rect.centerx, button_rect.centery,
                     size=24, color=text_color, center=True)
    
    def draw_solo_menu(self):
        """Desenha o menu de configuração do jogo solo"""
        # Título
        draw_text(self.screen, "CONFIGURAR PARTIDA", WINDOW_WIDTH // 2, 100,
                 size=36, color=COLORS['WHITE'], center=True)
        
        # Número de jogadores IA
        draw_text(self.screen, "Jogadores IA:", WINDOW_WIDTH // 2, 250,
                 size=24, color=COLORS['WHITE'], center=True)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, count in enumerate([1, 2, 3]):
            btn_x = WINDOW_WIDTH // 2 - 120 + i * 80
            btn_rect = pygame.Rect(btn_x, 280, 60, 30)
            
            # Cor baseada na seleção e hover
            if count == self.ai_players:
                color = (100, 150, 100)
            elif btn_rect.collidepoint(mouse_pos):
                color = (70, 70, 120)
            else:
                color = (50, 50, 100)
            
            pygame.draw.rect(self.screen, color, btn_rect)
            pygame.draw.rect(self.screen, COLORS['WHITE'], btn_rect, 2)
            
            draw_text(self.screen, str(count), 
                     btn_rect.centerx, btn_rect.centery,
                     size=20, color=COLORS['WHITE'], center=True)
        
        # Dificuldade
        draw_text(self.screen, "Dificuldade:", WINDOW_WIDTH // 2, 320,
                 size=24, color=COLORS['WHITE'], center=True)
        
        difficulties = [('Fácil', 'FACIL'), ('Médio', 'MEDIO'), ('Difícil', 'DIFICIL')]
        for i, (name, diff) in enumerate(difficulties):
            btn_x = WINDOW_WIDTH // 2 - 150 + i * 100
            btn_rect = pygame.Rect(btn_x, 350, 90, 30)
            
            # Cor baseada na seleção e hover
            if diff == self.ai_difficulty:
                color = (100, 150, 100)
            elif btn_rect.collidepoint(mouse_pos):
                color = (70, 70, 120)
            else:
                color = (50, 50, 100)
            
            pygame.draw.rect(self.screen, color, btn_rect)
            pygame.draw.rect(self.screen, COLORS['WHITE'], btn_rect, 2)
            
            draw_text(self.screen, name, 
                     btn_rect.centerx, btn_rect.centery,
                     size=18, color=COLORS['WHITE'], center=True)
        
        # Botões de ação
        button_width = 200
        button_height = 40
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        
        for button in self.solo_buttons:
            button_rect = pygame.Rect(button_x, button['y'], button_width, button_height)
            
            # Cor do botão
            if button_rect.collidepoint(mouse_pos):
                if button['action'] == 'start_solo':
                    color = (0, 150, 0)
                else:
                    color = (150, 0, 0)
                text_color = COLORS['WHITE']
            else:
                color = (50, 50, 100)
                text_color = COLORS['WHITE']
            
            # Desenha botão
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, COLORS['WHITE'], button_rect, 2)
            
            # Texto do botão
            draw_text(self.screen, button['text'], 
                     button_rect.centerx, button_rect.centery,
                     size=20, color=text_color, center=True)
    
    def draw_settings_menu(self):
        """Desenha o menu de configurações"""
        # Título
        draw_text(self.screen, "CONFIGURAÇÕES", WINDOW_WIDTH // 2, 100,
                 size=36, color=COLORS['WHITE'], center=True)
        
        # Placeholder para configurações
        draw_text(self.screen, "Configurações em desenvolvimento", 
                 WINDOW_WIDTH // 2, 250,
                 size=24, color=COLORS['WHITE'], center=True)
        
        # Botão voltar
        button_width = 200
        button_height = 40
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        button_rect = pygame.Rect(button_x, 400, button_width, button_height)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Cor do botão
        if button_rect.collidepoint(mouse_pos):
            color = (150, 0, 0)
        else:
            color = (50, 50, 100)
        
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, COLORS['WHITE'], button_rect, 2)
        
        draw_text(self.screen, "Voltar", 
                 button_rect.centerx, button_rect.centery,
                 size=20, color=COLORS['WHITE'], center=True)