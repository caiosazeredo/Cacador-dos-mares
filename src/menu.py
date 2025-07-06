# src/menu.py - Menu responsivo

import pygame
import sys
from config import *
from src.game import Game
from src.story import StoryMode
from src.achievements import AchievementScreen
from src.layout_manager import layout_manager
from src.utils import draw_text, draw_button, create_gradient_surface

class MainMenu:
    """Menu principal responsivo"""
    
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.clock = pygame.time.Clock()
        
        # Estado
        self.current_game = None
        self.current_submenu = None
        
        # Configurações
        self.ai_players = 1
        self.ai_difficulty = 'MEDIO'
        
        # Visual responsivo
        self.update_layout()
        
        print(f"Menu principal inicializado para {username}")
    
    def update_layout(self):
        """Atualiza layout responsivo"""
        screen_size = self.screen.get_size()
        layout_manager.update_screen_size(screen_size[0], screen_size[1])
        
        # Fundo responsivo
        self.background = create_gradient_surface(
            screen_size[0], screen_size[1],
            (20, 60, 100), (40, 120, 180)
        )
    
    def handle_event(self, event):
        """Processa eventos do menu"""
        if event.type == pygame.VIDEORESIZE:
            self.update_layout()
            return None
        
        if self.current_game:
            result = self.current_game.handle_event(event)
            if result == 'quit' or result == 'pause':
                self.current_game = None
                return None
            return result
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.current_submenu:
                    self.current_submenu = None
                else:
                    return 'quit'
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.handle_menu_click(event.pos)
        
        return None
    
    def handle_menu_click(self, mouse_pos):
        """Processa cliques no menu"""
        screen_width, screen_height = self.screen.get_size()
        
        if self.current_submenu == 'single_player':
            return self.handle_solo_menu_click(mouse_pos)
        else:
            return self.handle_main_menu_click(mouse_pos)
    
    def handle_main_menu_click(self, mouse_pos):
        """Processa cliques no menu principal"""
        screen_width, screen_height = self.screen.get_size()
        
        # Botões do menu principal
        button_width = max(200, int(300 * layout_manager.get_element_scale_factor()))
        button_height = max(40, int(50 * layout_manager.get_element_scale_factor()))
        
        center_x = screen_width // 2
        start_y = screen_height // 2 - 100
        spacing = button_height + 20
        
        buttons = [
            ('Jogar Solo', 'single_player'),
            ('Modo História', 'story'),
            ('Conquistas', 'achievements'),
            ('Configurações', 'settings'),
            ('Sair', 'quit')
        ]
        
        for i, (text, action) in enumerate(buttons):
            button_rect = pygame.Rect(
                center_x - button_width // 2,
                start_y + i * spacing,
                button_width, button_height
            )
            
            if button_rect.collidepoint(mouse_pos):
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
    
    def handle_solo_menu_click(self, mouse_pos):
        """Processa cliques no menu solo"""
        screen_width, screen_height = self.screen.get_size()
        
        button_width = max(150, int(200 * layout_manager.get_element_scale_factor()))
        button_height = max(35, int(45 * layout_manager.get_element_scale_factor()))
        
        center_x = screen_width // 2
        
        # Botão Iniciar
        start_button = pygame.Rect(
            center_x - button_width // 2,
            screen_height // 2 + 100,
            button_width, button_height
        )
        
        # Botão Voltar
        back_button = pygame.Rect(
            center_x - button_width // 2,
            screen_height // 2 + 160,
            button_width, button_height
        )
        
        if start_button.collidepoint(mouse_pos):
            self.start_solo_game()
        elif back_button.collidepoint(mouse_pos):
            self.current_submenu = None
        
        return None
    
    def start_solo_game(self):
        """Inicia jogo solo"""
        print(f"Iniciando jogo solo: {self.ai_players + 1} jogadores, dificuldade {self.ai_difficulty}")
        try:
            self.current_game = Game(self.screen, self.username, 
                                   self.ai_players + 1, self.ai_difficulty)
            print("Jogo solo iniciado com sucesso")
        except Exception as e:
            print(f"Erro ao iniciar jogo solo: {e}")
    
    def start_story_mode(self):
        """Inicia modo história"""
        print("Iniciando modo história")
        try:
            self.current_game = StoryMode(self.screen, self.username)
            print("Modo história iniciado com sucesso")
        except Exception as e:
            print(f"Erro ao iniciar modo história: {e}")
    
    def show_achievements(self):
        """Mostra conquistas"""
        print("Abrindo conquistas")
        try:
            achievements_screen = AchievementScreen(self.screen, self.username)
            achievements_screen.run()
            print("Tela de conquistas fechada")
        except Exception as e:
            print(f"Erro na tela de conquistas: {e}")
    
    def update(self, dt):
        """Atualiza menu"""
        if self.current_game:
            try:
                self.current_game.update(dt)
            except Exception as e:
                print(f"Erro ao atualizar jogo: {e}")
                self.current_game = None
    
    def draw(self):
        """Desenha menu responsivo"""
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
        # Fundo responsivo
        self.screen.blit(self.background, (0, 0))
        
        if self.current_submenu == 'single_player':
            self.draw_solo_menu()
        elif self.current_submenu == 'settings':
            self.draw_settings_menu()
        else:
            self.draw_main_menu()
    
    def draw_main_menu(self):
        """Desenha menu principal responsivo"""
        screen_width, screen_height = self.screen.get_size()
        
        # Título responsivo
        title_size = layout_manager.get_font_size(48)
        draw_text(self.screen, "CAÇADOR DOS MARES", 
                 screen_width // 2, screen_height // 4,
                 size=title_size, color=COLORS['WHITE'], center=True)
        
        # Bem-vindo responsivo
        welcome_size = layout_manager.get_font_size(24)
        draw_text(self.screen, f"Bem-vindo, {self.username}!", 
                 screen_width // 2, screen_height // 4 + 60,
                 size=welcome_size, color=COLORS['YELLOW'], center=True)
        
        # Botões responsivos
        self.draw_menu_buttons()
    
    def draw_menu_buttons(self):
        """Desenha botões do menu responsivos"""
        screen_width, screen_height = self.screen.get_size()
        
        button_width = max(200, int(300 * layout_manager.get_element_scale_factor()))
        button_height = max(40, int(50 * layout_manager.get_element_scale_factor()))
        
        center_x = screen_width // 2
        start_y = screen_height // 2 - 100
        spacing = button_height + 20
        
        buttons = [
            ('Jogar Solo', (0, 150, 0), (0, 200, 0)),
            ('Modo História', (150, 0, 150), (200, 0, 200)),
            ('Conquistas', (150, 150, 0), (200, 200, 0)),
            ('Configurações', (0, 0, 150), (0, 0, 200)),
            ('Sair', (150, 0, 0), (200, 0, 0))
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (text, normal_color, hover_color) in enumerate(buttons):
            button_rect = pygame.Rect(
                center_x - button_width // 2,
                start_y + i * spacing,
                button_width, button_height
            )
            
            # Cor baseada em hover
            color = hover_color if button_rect.collidepoint(mouse_pos) else normal_color
            
            # Desenha botão
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, COLORS['WHITE'], button_rect, 2)
            
            # Texto responsivo
            text_size = layout_manager.get_font_size(20)
            draw_text(self.screen, text, 
                     button_rect.centerx, button_rect.centery,
                     size=text_size, color=COLORS['WHITE'], center=True)
    
    def draw_solo_menu(self):
        """Desenha menu de jogo solo responsivo"""
        screen_width, screen_height = self.screen.get_size()
        
        # Título
        title_size = layout_manager.get_font_size(36)
        draw_text(self.screen, "JOGO SOLO", 
                 screen_width // 2, screen_height // 3,
                 size=title_size, color=COLORS['WHITE'], center=True)
        
        # Configurações responsivas
        config_size = layout_manager.get_font_size(20)
        y_offset = screen_height // 2 - 50
        
        draw_text(self.screen, f"Oponentes IA: {self.ai_players}", 
                 screen_width // 2, y_offset,
                 size=config_size, color=COLORS['WHITE'], center=True)
        
        draw_text(self.screen, f"Dificuldade: {self.ai_difficulty}", 
                 screen_width // 2, y_offset + 30,
                 size=config_size, color=COLORS['WHITE'], center=True)
        
        # Botões responsivos
        self.draw_solo_buttons()
    
    def draw_solo_buttons(self):
        """Desenha botões do menu solo"""
        screen_width, screen_height = self.screen.get_size()
        
        button_width = max(150, int(200 * layout_manager.get_element_scale_factor()))
        button_height = max(35, int(45 * layout_manager.get_element_scale_factor()))
        
        center_x = screen_width // 2
        mouse_pos = pygame.mouse.get_pos()
        
        # Botão Iniciar
        start_rect = pygame.Rect(
            center_x - button_width // 2,
            screen_height // 2 + 100,
            button_width, button_height
        )
        
        start_color = (0, 200, 0) if start_rect.collidepoint(mouse_pos) else (0, 150, 0)
        pygame.draw.rect(self.screen, start_color, start_rect)
        pygame.draw.rect(self.screen, COLORS['WHITE'], start_rect, 2)
        
        text_size = layout_manager.get_font_size(18)
        draw_text(self.screen, "Iniciar", 
                 start_rect.centerx, start_rect.centery,
                 size=text_size, color=COLORS['WHITE'], center=True)
        
        # Botão Voltar
        back_rect = pygame.Rect(
            center_x - button_width // 2,
            screen_height // 2 + 160,
            button_width, button_height
        )
        
        back_color = (200, 0, 0) if back_rect.collidepoint(mouse_pos) else (150, 0, 0)
        pygame.draw.rect(self.screen, back_color, back_rect)
        pygame.draw.rect(self.screen, COLORS['WHITE'], back_rect, 2)
        
        draw_text(self.screen, "Voltar", 
                 back_rect.centerx, back_rect.centery,
                 size=text_size, color=COLORS['WHITE'], center=True)
    
    def draw_settings_menu(self):
        """Desenha menu de configurações responsivo"""
        screen_width, screen_height = self.screen.get_size()
        
        title_size = layout_manager.get_font_size(36)
        draw_text(self.screen, "CONFIGURAÇÕES", 
                 screen_width // 2, screen_height // 3,
                 size=title_size, color=COLORS['WHITE'], center=True)
        
        info_size = layout_manager.get_font_size(24)
        draw_text(self.screen, "Em desenvolvimento...", 
                 screen_width // 2, screen_height // 2,
                 size=info_size, color=COLORS['WHITE'], center=True)
        
        # Botão voltar
        button_width = max(120, int(150 * layout_manager.get_element_scale_factor()))
        button_height = max(30, int(40 * layout_manager.get_element_scale_factor()))
        
        back_rect = pygame.Rect(
            screen_width // 2 - button_width // 2,
            screen_height // 2 + 100,
            button_width, button_height
        )
        
        mouse_pos = pygame.mouse.get_pos()
        color = (200, 0, 0) if back_rect.collidepoint(mouse_pos) else (150, 0, 0)
        
        pygame.draw.rect(self.screen, color, back_rect)
        pygame.draw.rect(self.screen, COLORS['WHITE'], back_rect, 2)
        
        text_size = layout_manager.get_font_size(16)
        draw_text(self.screen, "Voltar", 
                 back_rect.centerx, back_rect.centery,
                 size=text_size, color=COLORS['WHITE'], center=True)
        
        if back_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.current_submenu = None
