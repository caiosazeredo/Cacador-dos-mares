# setup_game.py - Script para configurar e preparar o jogo

import os
import shutil
import pygame

def setup_sprite_files():
    """Configura os arquivos de sprite necessários"""
    
    # Lista de arquivos de sprite que devem existir
    sprite_files = [
        ('spritesheet.png', 'assets/images/spritesheet.png'),
        ('spritesheet.xml', 'assets/images/spritesheet.xml'),
        ('spritesheet-double.png', 'assets/images/spritesheet-double.png'),
        ('spritesheet-double.xml', 'assets/images/spritesheet-double.xml'),
    ]
    
    # Cria o diretório se não existir
    os.makedirs('assets/images', exist_ok=True)
    
    # Copia arquivos se existirem na raiz
    for src_file, dest_file in sprite_files:
        if os.path.exists(src_file) and not os.path.exists(dest_file):
            print(f"Copiando {src_file} para {dest_file}")
            shutil.copy2(src_file, dest_file)
    
    # Verifica se algum arquivo foi encontrado
    found_files = []
    for src_file, dest_file in sprite_files:
        if os.path.exists(dest_file) or os.path.exists(src_file):
            found_files.append(src_file)
    
    if found_files:
        print(f"Arquivos de sprite encontrados: {', '.join(found_files)}")
    else:
        print("Nenhum arquivo de sprite encontrado, usando fallbacks")
        create_fallback_sprites()
    
    return len(found_files) > 0

def create_fallback_sprites():
    """Cria sprites de fallback se os originais não forem encontrados"""
    print("Criando sprites de fallback...")
    
    # Inicializa pygame para criar sprites
    pygame.init()
    
    # Cria diretório
    os.makedirs('assets/images', exist_ok=True)
    
    # Sprites de peixes
    fish_colors = [
        ('fish_orange', (255, 165, 0)),
        ('fish_pink', (255, 192, 203)),
        ('fish_blue', (135, 206, 250)),
        ('fish_green', (152, 251, 152)),
        ('fish_grey', (128, 128, 128)),
        ('fish_brown', (139, 69, 19))
    ]
    
    # Cria um spritesheet simples
    sheet_width = 512
    sheet_height = 512
    sprite_size = 64
    
    spritesheet = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)
    spritesheet.fill((0, 0, 0, 0))  # Transparente
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<TextureAtlas imagePath="spritesheet.png">\n'
    
    # Cria sprites de peixe
    x, y = 0, 0
    for name, color in fish_colors:
        # Cria sprite do peixe
        fish_surface = create_fish_sprite(sprite_size, color)
        spritesheet.blit(fish_surface, (x, y))
        
        # Adiciona ao XML
        xml_content += f'\t<SubTexture name="{name}" x="{x}" y="{y}" width="{sprite_size}" height="{sprite_size}"/>\n'
        
        x += sprite_size
        if x >= sheet_width:
            x = 0
            y += sprite_size
    
    # Cria sprites de navios
    ship_colors = [
        (139, 69, 19),  # Marrom
        (70, 130, 180),  # Azul aço
        (107, 142, 35),  # Verde oliva
        (205, 92, 92)   # Rosa indiano
    ]
    
    for i, color in enumerate(ship_colors):
        ship_surface = create_ship_sprite(sprite_size, color)
        spritesheet.blit(ship_surface, (x, y))
        
        xml_content += f'\t<SubTexture name="ship ({i+1}).png" x="{x}" y="{y}" width="{sprite_size}" height="{sprite_size}"/>\n'
        
        x += sprite_size
        if x >= sheet_width:
            x = 0
            y += sprite_size
    
    xml_content += '</TextureAtlas>\n'
    
    # Salva o spritesheet
    pygame.image.save(spritesheet, 'assets/images/spritesheet.png')
    
    # Salva o XML
    with open('assets/images/spritesheet.xml', 'w') as f:
        f.write(xml_content)
    
    print("Sprites de fallback criados com sucesso!")

def create_fish_sprite(size, color):
    """Cria um sprite de peixe"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Corpo do peixe
    body_rect = pygame.Rect(8, size//2-12, size-20, 24)
    pygame.draw.ellipse(surface, color, body_rect)
    pygame.draw.ellipse(surface, (0, 0, 0), body_rect, 2)
    
    # Cauda
    tail_points = [
        (8, size//2),
        (0, size//2-8),
        (0, size//2+8)
    ]
    pygame.draw.polygon(surface, color, tail_points)
    pygame.draw.polygon(surface, (0, 0, 0), tail_points, 2)
    
    # Olho
    eye_center = (size-16, size//2-4)
    pygame.draw.circle(surface, (255, 255, 255), eye_center, 4)
    pygame.draw.circle(surface, (0, 0, 0), eye_center, 3)
    
    # Barbatana
    fin_points = [
        (size//2, size//2-12),
        (size//2-6, size//2-20),
        (size//2+6, size//2-20)
    ]
    pygame.draw.polygon(surface, color, fin_points)
    pygame.draw.polygon(surface, (0, 0, 0), fin_points, 1)
    
    return surface

def create_ship_sprite(size, color):
    """Cria um sprite de navio"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Casco
    hull_points = [
        (size//2-16, size//2+8),
        (size//2+16, size//2+8),
        (size//2+12, size//2+20),
        (size//2-12, size//2+20)
    ]
    pygame.draw.polygon(surface, color, hull_points)
    pygame.draw.polygon(surface, (0, 0, 0), hull_points, 2)
    
    # Vela
    sail_points = [
        (size//2, size//2+8),
        (size//2, size//2-20),
        (size//2+16, size//2-6)
    ]
    pygame.draw.polygon(surface, (255, 255, 255), sail_points)
    pygame.draw.polygon(surface, (0, 0, 0), sail_points, 2)
    
    # Mastro
    pygame.draw.line(surface, (101, 67, 33),
                    (size//2, size//2+8),
                    (size//2, size//2-24), 3)
    
    return surface

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    required_modules = ['pygame', 'numpy', 'bcrypt']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"Módulos faltando: {', '.join(missing_modules)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("Todas as dependências estão instaladas!")
    return True

def main():
    """Função principal de setup"""
    print("=== Setup do Caçador dos Mares ===")
    
    # Verifica dependências
    if not check_dependencies():
        return False
    
    # Configura sprites
    setup_sprite_files()
    
    print("Setup concluído com sucesso!")
    print("Execute 'python main.py' para iniciar o jogo")
    return True

if __name__ == "__main__":
    main()