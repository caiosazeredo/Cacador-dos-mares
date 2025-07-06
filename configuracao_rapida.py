#!/usr/bin/env python3
"""
Script de configuração rápida para Caçador dos Mares
Execute este script para configurar rapidamente o jogo
"""

import pygame
import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.settings_manager import settings_manager

def main():
    """Configuração rápida do jogo"""
    print("⚙️  CONFIGURAÇÃO RÁPIDA - CAÇADOR DOS MARES")
    print("=" * 50)
    
    pygame.init()
    info = pygame.display.Info()
    
    print(f"🖥️  Monitor detectado: {info.current_w}x{info.current_h}")
    print(f"📐 Resolução atual: {settings_manager.current_resolution}")
    print(f"🖼️  Tela cheia: {'Sim' if settings_manager.fullscreen else 'Não'}")
    print(f"🔑 Login automático: {'Sim' if settings_manager.auto_login else 'Não'}")
    
    print("\n🎮 OPÇÕES DISPONÍVEIS:")
    print("1. Configurar resolução")
    print("2. Alternar tela cheia")
    print("3. Configurar login automático")
    print("4. Definir usuário padrão")
    print("5. Restaurar padrões")
    print("6. Sair")
    
    while True:
        try:
            choice = input("\nEscolha uma opção (1-6): ").strip()
            
            if choice == '1':
                configure_resolution()
            elif choice == '2':
                toggle_fullscreen()
            elif choice == '3':
                configure_auto_login()
            elif choice == '4':
                configure_username()
            elif choice == '5':
                restore_defaults()
            elif choice == '6':
                break
            else:
                print("❌ Opção inválida!")
                
        except KeyboardInterrupt:
            print("\n👋 Configuração cancelada")
            break
    
    print("✅ Configurações salvas!")
    pygame.quit()

def configure_resolution():
    """Configura resolução"""
    print("\n📐 CONFIGURAÇÃO DE RESOLUÇÃO")
    print("Resoluções disponíveis:")
    
    for i, res in enumerate(settings_manager.resolutions):
        current = " (atual)" if res == settings_manager.current_resolution else ""
        print(f"  {i+1}. {res[0]}x{res[1]}{current}")
    
    try:
        choice = int(input("Escolha uma resolução (número): ")) - 1
        if 0 <= choice < len(settings_manager.resolutions):
            width, height = settings_manager.resolutions[choice]
            settings_manager.set_resolution(width, height)
            print(f"✅ Resolução definida para {width}x{height}")
        else:
            print("❌ Opção inválida!")
    except ValueError:
        print("❌ Número inválido!")

def toggle_fullscreen():
    """Alterna tela cheia"""
    settings_manager.fullscreen = not settings_manager.fullscreen
    settings_manager.save_settings()
    status = "ativada" if settings_manager.fullscreen else "desativada"
    print(f"✅ Tela cheia {status}")

def configure_auto_login():
    """Configura login automático"""
    current = "ativado" if settings_manager.auto_login else "desativado"
    print(f"\n🔑 Login automático atualmente: {current}")
    
    choice = input("Ativar login automático? (s/N): ").lower().strip()
    settings_manager.auto_login = choice in ['s', 'sim', 'y', 'yes']
    settings_manager.save_settings()
    
    status = "ativado" if settings_manager.auto_login else "desativado"
    print(f"✅ Login automático {status}")

def configure_username():
    """Configura usuário padrão"""
    print(f"\n👤 Usuário atual: {settings_manager.steam_username}")
    
    new_username = input("Novo nome de usuário (Enter para manter atual): ").strip()
    if new_username:
        settings_manager.steam_username = new_username
        settings_manager.save_settings()
        print(f"✅ Usuário definido como: {new_username}")
    else:
        print("✅ Usuário mantido como: {settings_manager.steam_username}")

def restore_defaults():
    """Restaura configurações padrão"""
    print("\n⚠️  Isso irá restaurar todas as configurações padrão!")
    choice = input("Tem certeza? (s/N): ").lower().strip()
    
    if choice in ['s', 'sim', 'y', 'yes']:
        settings_manager.current_resolution = (1600, 900)
        settings_manager.fullscreen = False
        settings_manager.vsync = True
        settings_manager.sound_volume = 100
        settings_manager.music_volume = 80
        settings_manager.ui_scale = 1.0
        settings_manager.auto_login = True
        settings_manager.steam_username = "Jogador"
        settings_manager.save_settings()
        print("✅ Configurações restauradas para os padrões")
    else:
        print("❌ Operação cancelada")

if __name__ == "__main__":
    main()
