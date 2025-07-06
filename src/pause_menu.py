# src/pause_menu.py - Menu de pausa com configurações

import pygame
from config import *
from src.utils import draw_text, draw_button, create_gradient_surface
from src.settings_manager import settings_manager

class PauseMenu:
    """Menu de pausa do jogo"""
    
    def __init__(self, screen):
        self.screen = screen
        self.active = False
        self.current_page = 'main'  # main, settings, controls
        self.selected_resolution_index = 0
        
        # UI
        self.menu_width = 600
        self.menu_height = 500
        self.menu_x = (screen.get_width() - self.menu_width) // 2
        self.menu_y = (screen.get_height() - self.menu_height) // 2
        
        # Background
        self.background = create_gradient_surface(self.menu_width, self.menu_height,
                                                (20, 20, 40), (40, 40, 80))
        
        # Encontra índice da resolução atual
        current_res = settings_manager.current_resolution
        for i, res in enumerate(settings_manager.resolutions):
            if res == current_res:
                self.selected_resolution_index = i
                break
    
    def show(self):
        """Mostra o menu de pausa"""
        self.active = True
        self.current_page = 'main'
    
    def hide(self):
        """Esconde o menu de pausa"""
        self.active = False
    
    def toggle(self):
        """Alterna visibilidade do menu"""
        if self.active:
            self.hide()
        else:
            self.show()
    
    def handle_event(self, event):
        """Processa eventos do menu"""
        if not self.active:
            return None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.hide()
                return 'resume'
            elif event.key == pygame.K_F11:
                new_screen = settings_manager.toggle_fullscreen()
                return ('screen_changed', new_screen)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            
            if self.current_page == 'main':
                return self.handle_main_page_click(mouse_x, mouse_y)
            elif self.current_page == 'settings':
                return self.handle_settings_page_click(mouse_x, mouse_y)
        
        return None
    
    def handle_main_page_click(self, mouse_x, mouse_y):
        """Processa cliques na página principal"""
        button_width = 200
        button_height = 40
        button_x = self.menu_x + (self.menu_width - button_width) // 2
        
        # Botão Continuar
        if (button_x <= mouse_x <= button_x + button_width and
            self.menu_y + 150 <= mouse_y <= self.menu_y + 190):
            self.hide()
            return 'resume'
        
        # Botão Configurações
        if (button_x <= mouse_x <= button_x + button_width and
            self.menu_y + 200 <= mouse_y <= self.menu_y + 240):
            self.current_page = 'settings'
            return None
        
        # Botão Menu Principal
        if (button_x <= mouse_x <= button_x + button_width and
            self.menu_y + 250 <= mouse_y <= self.menu_y + 290):
            self.hide()
            return 'main_menu'
        
        # Botão Sair
        if (button_x <= mouse_x <= button_x + button_width and
            self.menu_y + 300 <= mouse_y <= self.menu_y + 340):
            return 'quit'
        
        return None
    
    def handle_settings_page_click(self, mouse_x, mouse_y):
        """Processa cliques na página de configurações"""
        button_width = 150
        button_height = 30
        
        # Resolução - botões anterior/próximo
        res_y = self.menu_y + 150
        if (self.menu_x + 100 <= mouse_x <= self.menu_x + 130 and
            res_y <= mouse_y <= res_y + 30):
            # Botão anterior
            self.selected_resolution_index = max(0, self.selected_resolution_index - 1)
            new_res = settings_manager.resolutions[self.selected_resolution_index]
            new_screen = settings_manager.set_resolution(new_res[0], new_res[1])
            return ('screen_changed', new_screen)
        
        if (self.menu_x + 470 <= mouse_x <= self.menu_x + 500 and
            res_y <= mouse_y <= res_y + 30):
            # Botão próximo
            max_index = len(settings_manager.resolutions) - 1
            self.selected_resolution_index = min(max_index, self.selected_resolution_index + 1)
            new_res = settings_manager.resolutions[self.selected_resolution_index]
            new_screen = settings_manager.set_resolution(new_res[0], new_res[1])
            return ('screen_changed', new_screen)
        
        # Toggle Tela Cheia
        fullscreen_y = self.menu_y + 200
        if (self.menu_x + 350 <= mouse_x <= self.menu_x + 450 and
            fullscreen_y <= mouse_y <= fullscreen_y + 30):
            new_screen = settings_manager.toggle_fullscreen()
            return ('screen_changed', new_screen)
        
        # Botão Voltar
        if (self.menu_x + 50 <= mouse_x <= self.menu_x + 150 and
            self.menu_y + 400 <= mouse_y <= self.menu_y + 430):
            self.current_page = 'main'
        
        return None
    
    def draw(self):
        """Desenha o menu de pausa"""
        if not self.active:
            return
        
        # Overlay semi-transparente
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Menu background
        menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        self.screen.blit(self.background, menu_rect)
        pygame.draw.rect(self.screen, COLORS['WHITE'], menu_rect, 3)
        
        if self.current_page == 'main':
            self.draw_main_page()
        elif self.current_page == 'settings':
            self.draw_settings_page()
    
    def draw_main_page(self):
        """Desenha página principal do menu"""
        # Título
        title_y = self.menu_y + 50
        draw_text(self.screen, "JOGO PAUSADO", 
                 self.menu_x + self.menu_width // 2, title_y,
                 size=36, color=COLORS['WHITE'], center=True)
        
        # Botões
        button_width = 200
        button_height = 40
        button_x = self.menu_x + (self.menu_width - button_width) // 2
        
        buttons = [
            ("Continuar", self.menu_y + 150),
            ("Configurações", self.menu_y + 200),
            ("Menu Principal", self.menu_y + 250),
            ("Sair", self.menu_y + 300)
        ]
        
        for text, y in buttons:
            button_rect = pygame.Rect(button_x, y, button_width, button_height)
            mouse_pos = pygame.mouse.get_pos()
            
            if button_rect.collidepoint(mouse_pos):
                color = (70, 70, 140)
            else:
                color = (50, 50, 100)
            
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, COLORS['WHITE'], button_rect, 2)
            
            draw_text(self.screen, text, 
                     button_x + button_width // 2, y + button_height // 2,
                     size=20, color=COLORS['WHITE'], center=True)
    
    def draw_settings_page(self):
        """Desenha página de configurações"""
        # Título
        title_y = self.menu_y + 50
        draw_text(self.screen, "CONFIGURAÇÕES", 
                 self.menu_x + self.menu_width // 2, title_y,
                 size=32, color=COLORS['WHITE'], center=True)
        
        # Resolução
        res_y = self.menu_y + 150
        current_res = settings_manager.resolutions[self.selected_resolution_index]
        draw_text(self.screen, "Resolução:", self.menu_x + 50, res_y,
                 size=20, color=COLORS['WHITE'])
        
        # Botão anterior
        prev_rect = pygame.Rect(self.menu_x + 200, res_y, 30, 30)
        pygame.draw.rect(self.screen, (100, 100, 100), prev_rect)
        pygame.draw.rect(self.screen, COLORS['WHITE'], prev_rect, 2)
        draw_text(self.screen, "<", prev_rect.centerx, prev_rect.centery,
                 size=20, color=COLORS['WHITE'], center=True)
        
        # Resolução atual
        res_text = f"{current_res[0]} x {current_res[1]}"
        draw_text(self.screen, res_text, self.menu_x + 300, res_y + 15,
                 size=20, color=COLORS['YELLOW'], center=True)
        
        # Botão próximo
        next_rect = pygame.Rect(self.menu_x + 400, res_y, 30, 30)
        pygame.draw.rect(self.screen, (100, 100, 100), next_rect)
        pygame.draw.rect(self.screen, COLORS['WHITE'], next_rect, 2)
        draw_text(self.screen, ">", next_rect.centerx, next_rect.centery,
                 size=20, color=COLORS['WHITE'], center=True)
        
        # Tela cheia
        fullscreen_y = self.menu_y + 200
        draw_text(self.screen, "Tela Cheia:", self.menu_x + 50, fullscreen_y,
                 size=20, color=COLORS['WHITE'])
        
        fullscreen_text = "Ativada" if settings_manager.fullscreen else "Desativada"
        fullscreen_color = COLORS['GREEN'] if settings_manager.fullscreen else COLORS['RED']
        
        fullscreen_rect = pygame.Rect(self.menu_x + 200, fullscreen_y, 120, 30)
        pygame.draw.rect(self.screen, (100, 100, 100), fullscreen_rect)
        pygame.draw.rect(self.screen, COLORS['WHITE'], fullscreen_rect, 2)
        draw_text(self.screen, fullscreen_text, fullscreen_rect.centerx, fullscreen_rect.centery,
                 size=18, color=fullscreen_color, center=True)
        
        # Instruções
        instructions = [
            "F11 - Alternar tela cheia",
            "Alt+Enter - Alternar tela cheia",
            "ESC - Fechar menu"
        ]
        
        for i, instruction in enumerate(instructions):
            draw_text(self.screen, instruction, self.menu_x + 50, self.menu_y + 280 + i * 25,
                     size=16, color=COLORS['WHITE'])
        
        # Botão Voltar
        back_rect = pygame.Rect(self.menu_x + 50, self.menu_y + 400, 100, 30)
        pygame.draw.rect(self.screen, (100, 50, 50), back_rect)
        pygame.draw.rect(self.screen, COLORS['WHITE'], back_rect, 2)
        draw_text(self.screen, "Voltar", back_rect.centerx, back_rect.centery,
                 size=18, color=COLORS['WHITE'], center=True)
