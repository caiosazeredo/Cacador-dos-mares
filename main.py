# main.py - Ponto de entrada do jogo (corrigido)

import pygame
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import *
from src.menu import MainMenu
from src.login import LoginScreen
from src.utils import create_directories
from src.sprite_loader import init_sprites

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
    
    # Inicializa sistema de sprites
    print("Carregando sprites...")
    sprite_manager = init_sprites()
    
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
                    # Login bem-sucedido
                    print(f"Login realizado para: {result}")
                    game_state['logged_in'] = True
                    game_state['username'] = result
                    game_state['current_screen'] = 'menu'
                    main_menu = MainMenu(screen, game_state['username'])
                    print("Menu principal criado")
            
            elif game_state['current_screen'] == 'menu' and main_menu:
                try:
                    action = main_menu.handle_event(event)
                    if action == 'quit':
                        running = False
                    elif action == 'logout':
                        print("Fazendo logout...")
                        game_state['logged_in'] = False
                        game_state['username'] = None
                        game_state['current_screen'] = 'login'
                        main_menu = None
                        # Recria a tela de login
                        login_screen = LoginScreen(screen)
                except Exception as e:
                    print(f"Erro no menu: {e}")
                    # Em caso de erro, volta para o login
                    game_state['current_screen'] = 'login'
                    main_menu = None
        
        # Atualiza a tela atual
        try:
            if game_state['current_screen'] == 'login':
                login_screen.update(dt)
                login_screen.draw()
            elif game_state['current_screen'] == 'menu' and main_menu:
                main_menu.update(dt)
                main_menu.draw()
            else:
                # Estado inválido, volta para login
                print("Estado inválido, retornando ao login")
                game_state['current_screen'] = 'login'
                main_menu = None
        except Exception as e:
            print(f"Erro durante atualização/desenho: {e}")
            # Em caso de erro, volta para o login
            game_state['current_screen'] = 'login'
            main_menu = None
        
        # Atualiza a tela
        pygame.display.flip()
    
    # Encerra o jogo
    print("Encerrando o jogo...")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()