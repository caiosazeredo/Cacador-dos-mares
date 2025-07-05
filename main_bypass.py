# main.py - Versão com bypass de login

import pygame
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import *
from src.menu import MainMenu
from src.utils import create_directories

def main():
    """Função principal com bypass de login"""
    
    # Cria diretórios necessários
    create_directories()
    
    # Inicializa Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Configura a janela
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Clock para controlar FPS
    clock = pygame.time.Clock()
    
    print("BYPASS DE LOGIN ATIVADO - Indo direto para o menu")
    
    # Vai direto para o menu principal (bypass do login)
    try:
        main_menu = MainMenu(screen, "caio")  # Usa "caio" como usuário padrão
        print("Menu principal criado com sucesso")
        
        # Loop principal
        running = True
        while running:
            dt = clock.tick(FPS) / 1000.0
            
            # Eventos
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                
                # Processa eventos do menu
                action = main_menu.handle_event(event)
                if action == 'quit':
                    running = False
            
            # Atualiza e desenha o menu
            main_menu.update(dt)
            main_menu.draw()
            
            # Atualiza a tela
            pygame.display.flip()
            
    except Exception as e:
        print(f"Erro no menu principal: {e}")
        import traceback
        traceback.print_exc()
    
    # Encerra o jogo
    print("Encerrando o jogo...")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
