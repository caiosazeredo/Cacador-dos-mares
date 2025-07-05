# main.py - Ponto de entrada do jogo

import pygame
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import *
from src.menu import MainMenu
from src.login import LoginScreen
from src.utils import create_directories

def main():
    """Função principal do jogo"""
    
    # Cria diretórios necessários
    create_directories()
    
    # Inicializa Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Configura a janela
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Ícone (será criado posteriormente)
    # icon = pygame.image.load(os.path.join(IMAGES_PATH, 'icon.png'))
    # pygame.display.set_icon(icon)
    
    # Clock para controlar FPS
    clock = pygame.time.Clock()
    
    # Estado do jogo
    game_state = {
        'logged_in': False,
        'username': None,
        'current_screen': 'login'
    }
    
    # Telas do jogo
    login_screen = LoginScreen(screen)
    main_menu = None
    
    # Loop principal
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time em segundos
        
        # Eventos
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            # Processa eventos da tela atual
            if game_state['current_screen'] == 'login':
                result = login_screen.handle_event(event)
                if result:
                    game_state['logged_in'] = True
                    game_state['username'] = result
                    game_state['current_screen'] = 'menu'
                    main_menu = MainMenu(screen, game_state['username'])
            
            elif game_state['current_screen'] == 'menu' and main_menu:
                action = main_menu.handle_event(event)
                if action == 'quit':
                    running = False
                elif action == 'logout':
                    game_state['logged_in'] = False
                    game_state['username'] = None
                    game_state['current_screen'] = 'login'
                    main_menu = None
        
        # Atualiza a tela atual
        if game_state['current_screen'] == 'login':
            login_screen.update(dt)
            login_screen.draw()
        elif game_state['current_screen'] == 'menu' and main_menu:
            main_menu.update(dt)
            main_menu.draw()
        
        # Atualiza a tela
        pygame.display.flip()
    
    # Encerra o jogo
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()