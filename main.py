# main.py - Sistema responsivo corrigido

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
from src.settings_manager import settings_manager

def detect_steam_user():
    """Detecta usuário do Steam"""
    return settings_manager.steam_username

def safe_apply_resolution():
    """Aplica resolução de forma segura"""
    try:
        return settings_manager.apply_resolution()
    except Exception as e:
        print(f"Erro ao aplicar resolução: {e}")
        # Fallback seguro
        return pygame.display.set_mode((1280, 720), pygame.RESIZABLE | pygame.DOUBLEBUF)

def safe_toggle_fullscreen():
    """Alterna tela cheia de forma segura"""
    try:
        return settings_manager.toggle_fullscreen()
    except Exception as e:
        print(f"Erro ao alternar tela cheia: {e}")
        # Fallback para resolução atual
        current_size = pygame.display.get_surface().get_size()
        return pygame.display.set_mode(current_size, pygame.RESIZABLE | pygame.DOUBLEBUF)

def main():
    """Função principal corrigida"""
    
    print("🚀 Iniciando Caçador dos Mares - Versão Responsiva")
    print("=" * 60)
    
    # Cria diretórios necessários
    create_directories()
    
    # Inicializa Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Configura janela responsiva de forma segura
    try:
        screen = safe_apply_resolution()
    except Exception as e:
        print(f"Erro na configuração inicial: {e}")
        screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE | pygame.DOUBLEBUF)
    
    pygame.display.set_caption(TITLE)
    
    # Verifica se screen é válido
    if not isinstance(screen, pygame.Surface):
        print("Erro: Tela não foi criada corretamente")
        screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE | pygame.DOUBLEBUF)
    
    # Inicializa sistema de sprites
    print("📦 Carregando recursos...")
    try:
        sprite_manager = init_sprites()
        print("✓ Sprites carregados")
    except Exception as e:
        print(f"⚠ Aviso sprites: {e}")
    
    # Clock para controlar FPS
    clock = pygame.time.Clock()
    
    # Estado do jogo
    if settings_manager.auto_login:
        username = detect_steam_user()
        print(f"🔑 Login automático: {username}")
        game_state = {
            'logged_in': True,
            'username': username,
            'current_screen': 'menu'
        }
        main_menu = MainMenu(screen, username)
        login_screen = None
    else:
        print("🔑 Tela de login")
        game_state = {
            'logged_in': False,
            'username': None,
            'current_screen': 'login'
        }
        login_screen = LoginScreen(screen)
        main_menu = None
    
    print("✓ Sistema inicializado")
    print()
    print("🎮 CONTROLES:")
    print("  F11 / Alt+Enter - Tela cheia")
    print("  ESC - Menu de pausa")
    print("  Ctrl+Q - Sair")
    print("  Mouse - Interação")
    print()
    
    # Loop principal
    running = True
    last_screen_size = screen.get_size()
    
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        # Verifica se a tela ainda é válida
        if not isinstance(screen, pygame.Surface):
            print("Erro: Tela inválida detectada, recriando...")
            screen = pygame.display.set_mode(last_screen_size, pygame.RESIZABLE | pygame.DOUBLEBUF)
        
        # Eventos
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            # Redimensionamento
            elif event.type == pygame.VIDEORESIZE:
                try:
                    new_screen = pygame.display.set_mode((event.w, event.h), 
                                                       pygame.RESIZABLE | pygame.DOUBLEBUF)
                    if isinstance(new_screen, pygame.Surface):
                        screen = new_screen
                        last_screen_size = screen.get_size()
                        
                        # Atualiza telas com novo tamanho
                        if login_screen and hasattr(login_screen, 'screen'):
                            login_screen.screen = screen
                        if main_menu and hasattr(main_menu, 'screen'):
                            main_menu.screen = screen
                            
                except Exception as e:
                    print(f"Erro no redimensionamento: {e}")
            
            # Atalhos globais
            elif event.type == pygame.KEYDOWN:
                # Tela cheia
                if (event.key == pygame.K_F11 or 
                    (event.key == pygame.K_RETURN and event.mod & pygame.KMOD_ALT)):
                    try:
                        new_screen = safe_toggle_fullscreen()
                        if isinstance(new_screen, pygame.Surface):
                            screen = new_screen
                            last_screen_size = screen.get_size()
                            
                            if login_screen and hasattr(login_screen, 'screen'):
                                login_screen.screen = screen
                            if main_menu and hasattr(main_menu, 'screen'):
                                main_menu.screen = screen
                    except Exception as e:
                        print(f"Erro ao alternar tela cheia: {e}")
                
                # Sair rápido
                elif event.key == pygame.K_q and event.mod & pygame.KMOD_CTRL:
                    running = False
            
            # Processa eventos das telas
            if game_state['current_screen'] == 'login' and login_screen:
                try:
                    result = login_screen.handle_event(event)
                    if result:
                        print(f"✓ Login: {result}")
                        game_state['logged_in'] = True
                        game_state['username'] = result
                        game_state['current_screen'] = 'menu'
                        main_menu = MainMenu(screen, result)
                        login_screen = None
                except Exception as e:
                    print(f"Erro no login: {e}")
            
            elif game_state['current_screen'] == 'menu' and main_menu:
                try:
                    action = main_menu.handle_event(event)
                    if action == 'quit':
                        running = False
                    elif action == 'logout':
                        print("🔑 Logout")
                        game_state['logged_in'] = False
                        game_state['username'] = None
                        game_state['current_screen'] = 'login'
                        main_menu = None
                        login_screen = LoginScreen(screen)
                    elif isinstance(action, tuple) and action[0] == 'screen_changed':
                        new_screen = action[1]
                        if isinstance(new_screen, pygame.Surface):
                            screen = new_screen
                            main_menu.screen = screen
                except Exception as e:
                    print(f"Erro no menu: {e}")
                    game_state['current_screen'] = 'login'
                    main_menu = None
                    login_screen = LoginScreen(screen)
        
        # Renderização segura
        try:
            # Verifica se screen é válido antes de usar
            if not isinstance(screen, pygame.Surface):
                continue
            
            # Limpa tela
            screen.fill(COLORS['BACKGROUND'])
            
            # Renderiza tela atual
            if game_state['current_screen'] == 'login' and login_screen:
                login_screen.update(dt)
                login_screen.draw()
            elif game_state['current_screen'] == 'menu' and main_menu:
                main_menu.update(dt)
                main_menu.draw()
            
            # Debug info (F12)
            if pygame.key.get_pressed()[pygame.K_F12]:
                from src.utils import draw_text
                from src.layout_manager import layout_manager
                
                debug_info = layout_manager.get_debug_info()
                debug_texts = [
                    f"FPS: {int(clock.get_fps())}",
                    f"Tela: {debug_info['screen_size']}",
                    f"Margens: {debug_info['margins']}",
                    f"Escala: {debug_info['scale_factor']:.2f}",
                    f"Cache: {debug_info['cache_size']}"
                ]
                
                for i, text in enumerate(debug_texts):
                    draw_text(screen, text, 10, 10 + i * 25, size=18, color=COLORS['WHITE'])
        
        except Exception as e:
            print(f"Erro de renderização: {e}")
            try:
                if isinstance(screen, pygame.Surface):
                    screen.fill((20, 20, 40))
            except:
                pass
        
        # Atualiza tela de forma segura
        try:
            pygame.display.flip()
        except Exception as e:
            print(f"Erro ao atualizar display: {e}")
    
    # Salva configurações e encerra
    try:
        settings_manager.save_settings()
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")
    
    print("👋 Encerrando Caçador dos Mares...")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
