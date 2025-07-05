#!/usr/bin/env python3
# diagnosticar_jogo.py - Script para diagnosticar problemas do Caçador dos Mares

import os
import sys
import pygame

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("=== VERIFICANDO DEPENDÊNCIAS ===")
    
    dependencias = ['pygame', 'numpy', 'bcrypt']
    faltando = []
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✓ {dep} - OK")
        except ImportError:
            print(f"✗ {dep} - FALTANDO")
            faltando.append(dep)
    
    if faltando:
        print(f"\nInstale as dependências faltando com:")
        print(f"pip install {' '.join(faltando)}")
        return False
    
    print("✓ Todas as dependências estão instaladas!")
    return True

def verificar_estrutura_arquivos():
    """Verifica se a estrutura de arquivos está correta"""
    print("\n=== VERIFICANDO ESTRUTURA DE ARQUIVOS ===")
    
    arquivos_essenciais = [
        'main.py',
        'config.py',
        'setup_game.py',
        'src/__init__.py',
        'src/game.py',
        'src/card.py',
        'src/sprite_loader.py',
        'src/fish.py',
        'src/player.py',
        'src/board.py',
        'src/menu.py',
        'src/utils.py'
    ]
    
    faltando = []
    for arquivo in arquivos_essenciais:
        if os.path.exists(arquivo):
            print(f"✓ {arquivo}")
        else:
            print(f"✗ {arquivo} - FALTANDO")
            faltando.append(arquivo)
    
    if faltando:
        print(f"\nArquivos faltando: {len(faltando)}")
        return False
    
    print("✓ Estrutura de arquivos OK!")
    return True

def verificar_sprites():
    """Verifica se os sprites estão funcionando"""
    print("\n=== VERIFICANDO SPRITES ===")
    
    # Verifica pastas
    pastas = ['assets', 'assets/images']
    for pasta in pastas:
        if not os.path.exists(pasta):
            print(f"Criando pasta: {pasta}")
            os.makedirs(pasta, exist_ok=True)
        else:
            print(f"✓ Pasta {pasta} existe")
    
    # Verifica arquivos de sprite
    sprites_originais = [
        'assets/images/spritesheet.png',
        'assets/images/spritesheet.xml',
        'spritesheet.png',
        'spritesheet.xml'
    ]
    
    sprites_encontrados = []
    for sprite in sprites_originais:
        if os.path.exists(sprite):
            sprites_encontrados.append(sprite)
            print(f"✓ {sprite}")
    
    if not sprites_encontrados:
        print("⚠ Nenhum sprite original encontrado - usando fallbacks")
        return criar_sprites_fallback()
    else:
        print(f"✓ {len(sprites_encontrados)} arquivos de sprite encontrados")
        return True

def criar_sprites_fallback():
    """Cria sprites de fallback se necessário"""
    print("\n=== CRIANDO SPRITES DE FALLBACK ===")
    
    try:
        pygame.init()
        
        # Cores dos peixes
        cores_peixes = [
            ('fish_orange', (255, 165, 0)),
            ('fish_pink', (255, 192, 203)),
            ('fish_blue', (135, 206, 250)),
            ('fish_green', (152, 251, 152)),
            ('fish_grey', (128, 128, 128)),
            ('fish_brown', (139, 69, 19))
        ]
        
        # Cria spritesheet
        tamanho_sprite = 64
        largura_sheet = 512
        altura_sheet = 512
        
        spritesheet = pygame.Surface((largura_sheet, altura_sheet), pygame.SRCALPHA)
        spritesheet.fill((0, 0, 0, 0))
        
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<TextureAtlas imagePath="spritesheet.png">\n'
        
        x, y = 0, 0
        
        # Cria sprites de peixes
        for nome, cor in cores_peixes:
            sprite_peixe = criar_sprite_peixe(tamanho_sprite, cor)
            spritesheet.blit(sprite_peixe, (x, y))
            xml_content += f'\t<SubTexture name="{nome}" x="{x}" y="{y}" width="{tamanho_sprite}" height="{tamanho_sprite}"/>\n'
            
            x += tamanho_sprite
            if x >= largura_sheet:
                x = 0
                y += tamanho_sprite
        
        # Cria sprites de navios
        cores_navios = [
            (139, 69, 19),   # Marrom
            (70, 130, 180),  # Azul aço
            (107, 142, 35),  # Verde oliva
            (205, 92, 92)    # Rosa indiano
        ]
        
        for i, cor in enumerate(cores_navios):
            sprite_navio = criar_sprite_navio(tamanho_sprite, cor)
            spritesheet.blit(sprite_navio, (x, y))
            xml_content += f'\t<SubTexture name="ship ({i+1}).png" x="{x}" y="{y}" width="{tamanho_sprite}" height="{tamanho_sprite}"/>\n'
            
            x += tamanho_sprite
            if x >= largura_sheet:
                x = 0
                y += tamanho_sprite
        
        xml_content += '</TextureAtlas>\n'
        
        # Salva arquivos
        pygame.image.save(spritesheet, 'assets/images/spritesheet.png')
        
        with open('assets/images/spritesheet.xml', 'w') as f:
            f.write(xml_content)
        
        print("✓ Sprites de fallback criados com sucesso!")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao criar sprites: {e}")
        return False

def criar_sprite_peixe(tamanho, cor):
    """Cria um sprite de peixe"""
    surface = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    
    # Corpo do peixe
    corpo_rect = pygame.Rect(8, tamanho//2-12, tamanho-20, 24)
    pygame.draw.ellipse(surface, cor, corpo_rect)
    pygame.draw.ellipse(surface, (0, 0, 0), corpo_rect, 2)
    
    # Cauda
    pontos_cauda = [
        (8, tamanho//2),
        (0, tamanho//2-8),
        (0, tamanho//2+8)
    ]
    pygame.draw.polygon(surface, cor, pontos_cauda)
    pygame.draw.polygon(surface, (0, 0, 0), pontos_cauda, 2)
    
    # Olho
    centro_olho = (tamanho-16, tamanho//2-4)
    pygame.draw.circle(surface, (255, 255, 255), centro_olho, 4)
    pygame.draw.circle(surface, (0, 0, 0), centro_olho, 3)
    
    return surface

def criar_sprite_navio(tamanho, cor):
    """Cria um sprite de navio"""
    surface = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    
    # Casco
    pontos_casco = [
        (tamanho//2-16, tamanho//2+8),
        (tamanho//2+16, tamanho//2+8),
        (tamanho//2+12, tamanho//2+20),
        (tamanho//2-12, tamanho//2+20)
    ]
    pygame.draw.polygon(surface, cor, pontos_casco)
    pygame.draw.polygon(surface, (0, 0, 0), pontos_casco, 2)
    
    # Vela
    pontos_vela = [
        (tamanho//2, tamanho//2+8),
        (tamanho//2, tamanho//2-20),
        (tamanho//2+16, tamanho//2-6)
    ]
    pygame.draw.polygon(surface, (255, 255, 255), pontos_vela)
    pygame.draw.polygon(surface, (0, 0, 0), pontos_vela, 2)
    
    # Mastro
    pygame.draw.line(surface, (101, 67, 33),
                    (tamanho//2, tamanho//2+8),
                    (tamanho//2, tamanho//2-24), 3)
    
    return surface

def testar_pygame():
    """Testa se o pygame está funcionando"""
    print("\n=== TESTANDO PYGAME ===")
    
    try:
        pygame.init()
        
        # Testa criação de superfície
        test_surface = pygame.Surface((100, 100))
        print("✓ Pygame Surface criada com sucesso")
        
        # Testa modo de vídeo
        pygame.display.set_mode((800, 600), pygame.NOFRAME)
        print("✓ Modo de vídeo inicializado")
        
        pygame.quit()
        print("✓ Pygame funcionando corretamente!")
        return True
        
    except Exception as e:
        print(f"✗ Erro no pygame: {e}")
        return False

def executar_jogo_teste():
    """Executa um teste rápido do jogo"""
    print("\n=== TESTE RÁPIDO DO JOGO ===")
    
    try:
        # Adiciona src ao path se não estiver
        src_path = os.path.join(os.getcwd(), 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Testa imports básicos
        import config
        print("✓ Config importado com sucesso")
        
        from src.card import Card, CardDeck
        print("✓ Módulos de carta importados com sucesso")
        
        # Testa criação de carta
        carta = Card((1, 0))
        print("✓ Carta criada com sucesso")
        
        # Testa baralho
        baralho = CardDeck()
        print(f"✓ Baralho criado com {len(baralho.cards)} cartas")
        
        carta_comprada = baralho.draw_card()
        print("✓ Carta comprada do baralho")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro no teste: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal de diagnóstico"""
    print("DIAGNÓSTICO DO CAÇADOR DOS MARES")
    print("=" * 50)
    
    resultados = []
    
    # Executa todos os testes
    resultados.append(verificar_dependencias())
    resultados.append(verificar_estrutura_arquivos())
    resultados.append(verificar_sprites())
    resultados.append(testar_pygame())
    resultados.append(executar_jogo_teste())
    
    # Relatório final
    print("\n" + "=" * 50)
    print("RELATÓRIO FINAL")
    print("=" * 50)
    
    total_testes = len(resultados)
    testes_ok = sum(resultados)
    
    print(f"Testes realizados: {total_testes}")
    print(f"Testes bem-sucedidos: {testes_ok}")
    print(f"Testes falharam: {total_testes - testes_ok}")
    
    if all(resultados):
        print("\n✓ DIAGNÓSTICO: JOGO PRONTO PARA EXECUÇÃO!")
        print("Execute: python main.py")
    else:
        print("\n⚠ DIAGNÓSTICO: PROBLEMAS ENCONTRADOS")
        print("Resolva os problemas acima antes de executar o jogo.")
    
    return all(resultados)

if __name__ == "__main__":
    main()