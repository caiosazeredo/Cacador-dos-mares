#!/usr/bin/env python3
# corrigir_sprite_loader.py - Corrige sprite loader e busca peixes

import os
import sys

def encontrar_sprites_peixes():
    """Encontra onde estão os sprites de peixes"""
    print("=== PROCURANDO SPRITES DE PEIXES ===")
    
    # Possíveis localizações dos peixes
    locais_possiveis = [
        "assets/images/peixes",
        "assets/images/peixes/PNG", 
        "assets/images/PNG",
        "assets/images",
        "assets",
        "."  # Pasta atual
    ]
    
    peixes_encontrados = []
    
    for local in locais_possiveis:
        if os.path.exists(local):
            print(f"Verificando: {local}")
            
            # Procura recursivamente
            for root, dirs, files in os.walk(local):
                for arquivo in files:
                    if arquivo.startswith('fish_') and arquivo.endswith('.png'):
                        caminho_completo = os.path.join(root, arquivo)
                        peixes_encontrados.append(caminho_completo)
                        print(f"  ✓ Encontrado: {caminho_completo}")
    
    if not peixes_encontrados:
        print("Nenhum peixe encontrado. Procurando outros tipos...")
        
        # Procura por qualquer arquivo que possa ser peixe
        for local in locais_possiveis:
            if os.path.exists(local):
                for root, dirs, files in os.walk(local):
                    for arquivo in files:
                        if any(palavra in arquivo.lower() for palavra in ['fish', 'peixe', 'blue', 'orange', 'green']):
                            if arquivo.endswith('.png'):
                                caminho_completo = os.path.join(root, arquivo)
                                peixes_encontrados.append(caminho_completo)
                                print(f"  ? Possível peixe: {caminho_completo}")
    
    return peixes_encontrados

def copiar_peixes_encontrados():
    """Copia os peixes encontrados para assets/images"""
    print("\n=== COPIANDO PEIXES ENCONTRADOS ===")
    
    peixes = encontrar_sprites_peixes()
    
    if not peixes:
        print("Nenhum peixe encontrado. Usando sprites dos navios copiados.")
        return False
    
    import shutil
    
    # Mapeia arquivos encontrados para nomes esperados
    mapeamento = {
        'fish_blue': ['fish_blue.png', 'blue', 'azul'],
        'fish_orange': ['fish_orange.png', 'orange', 'laranja'], 
        'fish_green': ['fish_green.png', 'green', 'verde'],
        'fish_pink': ['fish_pink.png', 'pink', 'rosa'],
        'fish_brown': ['fish_brown.png', 'brown', 'marrom'],
        'fish_grey': ['fish_grey.png', 'grey', 'gray', 'cinza']
    }
    
    copiados = 0
    for nome_destino, palavras_chave in mapeamento.items():
        for peixe_path in peixes:
            nome_arquivo = os.path.basename(peixe_path).lower()
            
            if any(palavra in nome_arquivo for palavra in palavras_chave):
                destino = f"assets/images/{nome_destino}.png"
                try:
                    shutil.copy2(peixe_path, destino)
                    print(f"✓ {peixe_path} → {destino}")
                    copiados += 1
                    break
                except Exception as e:
                    print(f"✗ Erro ao copiar {peixe_path}: {e}")
    
    print(f"Peixes copiados: {copiados}")
    return copiados > 0

def criar_sprite_loader_corrigido():
    """Cria sprite loader corrigido sem erros de sintaxe"""
    print("\n=== CRIANDO SPRITE LOADER CORRIGIDO ===")
    
    # Linhas do código sem problemas de sintaxe
    linhas = [
        "# src/sprite_loader.py - Sistema PNG profissional corrigido",
        "",
        "import pygame", 
        "import os",
        "from config import *",
        "",
        "# Inicializa pygame",
        "pygame.init()",
        "pygame.display.set_mode((1, 1), pygame.NOFRAME)",
        "",
        "class SpriteManager:",
        '    """Gerenciador de sprites PNG"""',
        "    ",
        "    def __init__(self):",
        "        self.sprites = {}",
        "        self.load_png_sprites()",
        "    ",
        "    def load_png_sprites(self):",
        '        """Carrega sprites PNG individuais"""',
        '        print("Carregando sprites PNG profissionais...")',
        "        ",
        "        # Sprites necessários",
        "        sprites_necessarios = [",
        "            'fish_blue.png',",
        "            'fish_brown.png',",
        "            'fish_green.png',",
        "            'fish_orange.png', ", 
        "            'fish_pink.png',",
        "            'fish_grey.png',",
        "            'ship (1).png',",
        "            'ship (2).png',",
        "            'ship (3).png',",
        "            'ship (4).png'",
        "        ]",
        "        ",
        "        sprites_carregados = 0",
        "        ",
        "        for sprite_name in sprites_necessarios:",
        "            sprite_path = os.path.join(IMAGES_PATH, sprite_name)",
        "            ",
        "            if os.path.exists(sprite_path):",
        "                try:",
        "                    sprite = pygame.image.load(sprite_path).convert_alpha()",
        "                    ",
        "                    # Remove extensão para compatibilidade",
        "                    nome_limpo = sprite_name.replace('.png', '')",
        "                    self.sprites[nome_limpo] = sprite",
        "                    self.sprites[sprite_name] = sprite",
        "                    ",
        '                    print(f"Sprite carregado: {sprite_name} - {sprite.get_size()}")',
        "                    sprites_carregados += 1",
        "                    ",
        "                except Exception as e:",
        '                    print(f"Erro ao carregar {sprite_name}: {e}")',
        "            else:",
        '                print(f"Nao encontrado: {sprite_path}")',
        "        ",
        '        print(f"Sprites PNG carregados: {sprites_carregados}")',
        "        self.criar_mapeamentos()",
        "    ",
        "    def criar_mapeamentos(self):",
        '        """Cria mapeamentos alternativos"""',
        "        # Mapeia fish_gray para fish_grey",
        "        if 'fish_grey' in self.sprites:",
        "            self.sprites['fish_gray'] = self.sprites['fish_grey']",
        "    ",
        "    def get_sprite(self, sprite_name, sheet_name=None):",
        '        """Retorna sprite pelo nome"""',
        "        nome_limpo = sprite_name.replace('.png', '')",
        "        ",
        "        if sprite_name in self.sprites:",
        "            return self.sprites[sprite_name]",
        "        elif nome_limpo in self.sprites:",
        "            return self.sprites[nome_limpo]",
        "        ",
        "        return None",
        "    ",
        "    def get_fish_sprite(self, fish_color):",
        '        """Retorna peixe por cor"""',
        "        color_map = {",
        "            (255, 165, 0): 'fish_orange',",
        "            (255, 192, 203): 'fish_pink',",
        "            (135, 206, 250): 'fish_blue',",
        "            (152, 251, 152): 'fish_green',",
        "            (128, 128, 128): 'fish_grey',",
        "            (139, 69, 19): 'fish_brown',",
        "        }",
        "        ",
        "        closest_color = min(color_map.keys(),",
        "                          key=lambda c: sum((a-b)**2 for a, b in zip(c, fish_color)))",
        "        ",
        "        sprite_name = color_map[closest_color]",
        "        return self.get_sprite(sprite_name)",
        "    ",
        "    def get_ship_sprite(self, player_id):",
        '        """Retorna navio por ID do jogador"""',
        "        ship_names = ['ship (1)', 'ship (2)', 'ship (3)', 'ship (4)']",
        "        ship_name = ship_names[player_id % len(ship_names)]",
        "        return self.get_sprite(ship_name)",
        "    ",
        "    def debug_sprites(self):",
        '        """Lista sprites carregados"""',
        '        print(f"Sprites carregados: {len(self.sprites)}")',
        "        for nome in sorted(self.sprites.keys()):",
        "            sprite = self.sprites[nome]",
        '            print(f"  {nome}: {sprite.get_size()}")',
        "",
        "# Instância global",
        "sprite_manager = None",
        "",
        "def get_sprite_manager():",
        "    global sprite_manager",
        "    if sprite_manager is None:",
        "        sprite_manager = SpriteManager()",
        "    return sprite_manager",
        "",
        "def init_sprites():",
        "    global sprite_manager", 
        "    sprite_manager = SpriteManager()",
        "    return sprite_manager",
        ""
    ]
    
    try:
        # Escreve linha por linha para evitar erros
        with open('src/sprite_loader.py', 'w', encoding='utf-8') as f:
            for linha in linhas:
                f.write(linha + '\n')
        
        print("✓ Sprite loader corrigido criado!")
        return True
        
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

def testar_sprite_loader_corrigido():
    """Testa o sprite loader corrigido"""
    print("\n=== TESTANDO SPRITE LOADER CORRIGIDO ===")
    
    try:
        # Remove cache
        if 'src.sprite_loader' in sys.modules:
            del sys.modules['src.sprite_loader']
        
        sys.path.insert(0, 'src')
        
        from src.sprite_loader import get_sprite_manager
        
        manager = get_sprite_manager()
        
        # Debug completo
        manager.debug_sprites()
        
        # Testa sprites
        sprites_teste = ['ship (1)', 'ship (2)', 'fish_orange', 'fish_blue']
        sucessos = 0
        
        print("\nTestando sprites:")
        for sprite_name in sprites_teste:
            sprite = manager.get_sprite(sprite_name)
            if sprite:
                print(f"✓ {sprite_name}: {sprite.get_size()}")
                sucessos += 1
            else:
                print(f"✗ {sprite_name}: não encontrado")
        
        # Testa funções
        print("\nTestando funções:")
        
        fish = manager.get_fish_sprite((255, 165, 0))
        if fish:
            print(f"✓ get_fish_sprite: {fish.get_size()}")
            sucessos += 1
        
        ship = manager.get_ship_sprite(0)
        if ship:
            print(f"✓ get_ship_sprite: {ship.get_size()}")
            sucessos += 1
        
        if sucessos >= 2:  # Pelo menos navios funcionando
            print(f"\n🎉 {sucessos} SPRITES FUNCIONANDO!")
            return True
        else:
            print(f"\n⚠ Apenas {sucessos} funcionando")
            return False
            
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Corrige sprite loader e configura PNG"""
    print("CORREÇÃO DO SPRITE LOADER PNG")
    print("=" * 50)
    
    # Procura e copia peixes
    copiar_peixes_encontrados()
    
    # Cria sprite loader corrigido
    if criar_sprite_loader_corrigido():
        if testar_sprite_loader_corrigido():
            print("\n✅ SPRITE LOADER PNG FUNCIONANDO!")
            print("🎮 Execute: python main.py")
            print("⛵ Pelo menos os navios devem estar bonitos!")
        else:
            print("\n⚠ Criado mas teste falhou")
            print("Execute o jogo para verificar")
    else:
        print("\n✗ Falha na correção")

if __name__ == "__main__":
    main()