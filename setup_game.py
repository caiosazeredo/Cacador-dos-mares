#!/usr/bin/env python3
# setup_simples.py - Setup simplificado para resolver problemas do jogo

import os
import pygame
import shutil

def verificar_e_instalar_dependencias():
    """Verifica e instala dependências"""
    print("=== VERIFICANDO DEPENDÊNCIAS ===")
    
    try:
        import pygame
        print("✓ pygame - OK")
    except ImportError:
        print("✗ pygame - INSTALANDO...")
        os.system("pip install pygame")
    
    try:
        import numpy
        print("✓ numpy - OK")
    except ImportError:
        print("⚠ numpy - Instalando (opcional)...")
        os.system("pip install numpy")
    
    try:
        import bcrypt
        print("✓ bcrypt - OK")
    except ImportError:
        print("⚠ bcrypt - Instalando (opcional)...")
        os.system("pip install bcrypt")

def criar_estrutura_pastas():
    """Cria a estrutura de pastas necessária"""
    print("\n=== CRIANDO ESTRUTURA DE PASTAS ===")
    
    pastas = [
        'assets',
        'assets/images',
        'assets/sounds',
        'assets/fonts',
        'data',
        'data/saves'
    ]
    
    for pasta in pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"✓ Pasta criada: {pasta}")
        else:
            print(f"✓ Pasta existe: {pasta}")

def criar_sprites_basicos():
    """Cria sprites básicos para o jogo funcionar"""
    print("\n=== CRIANDO SPRITES BÁSICOS ===")
    
    pygame.init()
    
    # Cores
    CORES = {
        'LARANJA': (255, 165, 0),
        'ROSA': (255, 192, 203),
        'AZUL': (135, 206, 250),
        'VERDE': (152, 251, 152),
        'CINZA': (128, 128, 128),
        'MARROM': (139, 69, 19)
    }
    
    # Tamanho dos sprites
    TAMANHO = 64
    
    # Cria spritesheet
    spritesheet = pygame.Surface((512, 512), pygame.SRCALPHA)
    spritesheet.fill((0, 0, 0, 0))
    
    # XML para mapear sprites
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<TextureAtlas imagePath="spritesheet.png">
'''
    
    x, y = 0, 0
    
    # Sprites de peixes
    for nome, cor in CORES.items():
        sprite = criar_peixe(TAMANHO, cor)
        spritesheet.blit(sprite, (x, y))
        
        nome_sprite = f"fish_{nome.lower()}"
        xml_content += f'    <SubTexture name="{nome_sprite}" x="{x}" y="{y}" width="{TAMANHO}" height="{TAMANHO}"/>\n'
        
        x += TAMANHO
        if x >= 512:
            x = 0
            y += TAMANHO
    
    # Sprites de navios
    cores_navios = [(139, 69, 19), (70, 130, 180), (107, 142, 35), (205, 92, 92)]
    for i, cor in enumerate(cores_navios):
        sprite = criar_navio(TAMANHO, cor)
        spritesheet.blit(sprite, (x, y))
        
        xml_content += f'    <SubTexture name="ship ({i+1}).png" x="{x}" y="{y}" width="{TAMANHO}" height="{TAMANHO}"/>\n'
        
        x += TAMANHO
        if x >= 512:
            x = 0
            y += TAMANHO
    
    xml_content += '</TextureAtlas>\n'
    
    # Salva arquivos
    pygame.image.save(spritesheet, 'assets/images/spritesheet.png')
    
    with open('assets/images/spritesheet.xml', 'w') as f:
        f.write(xml_content)
    
    print("✓ Sprites criados: assets/images/spritesheet.png")
    print("✓ XML criado: assets/images/spritesheet.xml")

def criar_peixe(tamanho, cor):
    """Cria sprite de peixe"""
    surface = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    
    # Corpo
    corpo = pygame.Rect(8, tamanho//2-10, tamanho-20, 20)
    pygame.draw.ellipse(surface, cor, corpo)
    pygame.draw.ellipse(surface, (0, 0, 0), corpo, 2)
    
    # Cauda
    cauda = [(8, tamanho//2), (0, tamanho//2-8), (0, tamanho//2+8)]
    pygame.draw.polygon(surface, cor, cauda)
    pygame.draw.polygon(surface, (0, 0, 0), cauda, 2)
    
    # Olho
    olho = (tamanho-12, tamanho//2-3)
    pygame.draw.circle(surface, (255, 255, 255), olho, 3)
    pygame.draw.circle(surface, (0, 0, 0), olho, 2)
    
    return surface

def criar_navio(tamanho, cor):
    """Cria sprite de navio"""
    surface = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    
    # Casco
    casco = [
        (tamanho//2-12, tamanho//2+6),
        (tamanho//2+12, tamanho//2+6),
        (tamanho//2+8, tamanho//2+16),
        (tamanho//2-8, tamanho//2+16)
    ]
    pygame.draw.polygon(surface, cor, casco)
    pygame.draw.polygon(surface, (0, 0, 0), casco, 2)
    
    # Vela
    vela = [
        (tamanho//2, tamanho//2+6),
        (tamanho//2, tamanho//2-16),
        (tamanho//2+12, tamanho//2-4)
    ]
    pygame.draw.polygon(surface, (255, 255, 255), vela)
    pygame.draw.polygon(surface, (0, 0, 0), vela, 2)
    
    # Mastro
    pygame.draw.line(surface, (101, 67, 33),
                    (tamanho//2, tamanho//2+6),
                    (tamanho//2, tamanho//2-20), 3)
    
    return surface

def verificar_arquivos_principais():
    """Verifica se os arquivos principais existem"""
    print("\n=== VERIFICANDO ARQUIVOS PRINCIPAIS ===")
    
    arquivos = [
        'main.py',
        'config.py',
        'src/game.py',
        'src/card.py',
        'src/player.py',
        'src/board.py'
    ]
    
    todos_ok = True
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"✓ {arquivo}")
        else:
            print(f"✗ {arquivo} - FALTANDO")
            todos_ok = False
    
    return todos_ok

def testar_jogo_basico():
    """Teste básico para ver se o jogo inicia"""
    print("\n=== TESTE BÁSICO DO JOGO ===")
    
    try:
        # Tenta importar módulos básicos
        import sys
        sys.path.insert(0, 'src')
        
        import config
        print("✓ Config importado")
        
        # Testa pygame
        pygame.init()
        test_screen = pygame.display.set_mode((800, 600), pygame.NOFRAME)
        print("✓ Pygame inicializado")
        pygame.quit()
        
        return True
        
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

def main():
    """Executa o setup completo"""
    print("SETUP SIMPLIFICADO - CAÇADOR DOS MARES")
    print("=" * 50)
    
    # Executa todas as etapas
    verificar_e_instalar_dependencias()
    criar_estrutura_pastas()
    
    if verificar_arquivos_principais():
        criar_sprites_basicos()
        
        if testar_jogo_basico():
            print("\n" + "=" * 50)
            print("✓ SETUP CONCLUÍDO COM SUCESSO!")
            print("Execute agora: python main.py")
            print("=" * 50)
        else:
            print("\n⚠ Setup parcialmente concluído")
            print("Pode haver problemas com imports")
    else:
        print("\n✗ Arquivos principais faltando")
        print("Verifique se está na pasta correta do jogo")

if __name__ == "__main__":
    main()