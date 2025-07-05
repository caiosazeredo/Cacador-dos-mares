# build.py - Script para criar executável do jogo

import PyInstaller.__main__
import os
import shutil
import platform

def build_executable():
    """Cria o executável do jogo"""
    
    # Nome do executável baseado no sistema operacional
    system = platform.system()
    if system == "Windows":
        exe_name = "CacadorDosMares.exe"
        icon_ext = ".ico"
    elif system == "Darwin":  # macOS
        exe_name = "CacadorDosMares"
        icon_ext = ".icns"
    else:  # Linux
        exe_name = "CacadorDosMares"
        icon_ext = ".png"
    
    # Verifica se o ícone existe
    icon_path = f"assets/images/icon{icon_ext}"
    icon_option = []
    if os.path.exists(icon_path):
        icon_option = ["--icon", icon_path]
    
    # Argumentos para o PyInstaller
    args = [
        "main.py",
        "--name", "CacadorDosMares",
        "--onefile",
        "--windowed",
        "--add-data", f"assets{os.pathsep}assets",
        "--add-data", f"data{os.pathsep}data",
        "--hidden-import", "pygame",
        "--hidden-import", "pygame_menu",
        "--hidden-import", "numpy",
        "--clean",
        "--noconfirm",
    ] + icon_option
    
    # Adiciona opções específicas do Windows
    if system == "Windows":
        args.extend([
            "--version-file", "version.txt",
            "--disable-windowed-traceback",
        ])
    
    print("Iniciando build do executável...")
    print(f"Sistema: {system}")
    print(f"Nome do executável: {exe_name}")
    
    try:
        # Executa o PyInstaller
        PyInstaller.__main__.run(args)
        
        print("\n✅ Build concluído com sucesso!")
        print(f"Executável criado em: dist/{exe_name}")
        
        # Cria diretório de distribuição
        dist_dir = f"dist/CacadorDosMares_{system}"
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir)
        os.makedirs(dist_dir)
        
        # Move o executável
        shutil.move(f"dist/{exe_name}", f"{dist_dir}/{exe_name}")
        
        # Copia assets necessários
        shutil.copytree("assets", f"{dist_dir}/assets", dirs_exist_ok=True)
        shutil.copytree("data", f"{dist_dir}/data", dirs_exist_ok=True)
        
        # Copia README e LICENSE
        shutil.copy("README.md", dist_dir)
        shutil.copy("LICENSE", dist_dir)
        
        # Cria arquivo de instruções
        with open(f"{dist_dir}/INSTRUCOES.txt", "w", encoding="utf-8") as f:
            f.write("CAÇADOR DOS MARES\n")
            f.write("================\n\n")
            f.write("Para jogar:\n")
            if system == "Windows":
                f.write("- Dê duplo clique em CacadorDosMares.exe\n")
            else:
                f.write("- Execute ./CacadorDosMares\n")
                f.write("- Pode ser necessário dar permissão de execução: chmod +x CacadorDosMares\n")
            f.write("\nPara mais informações, leia o arquivo README.md\n")
        
        print(f"\n📦 Pacote de distribuição criado em: {dist_dir}")
        
        # Cria arquivo ZIP
        if shutil.which("zip") or system == "Windows":
            zip_name = f"CacadorDosMares_{system}_v1.0.0"
            shutil.make_archive(f"dist/{zip_name}", "zip", dist_dir)
            print(f"📦 Arquivo ZIP criado: dist/{zip_name}.zip")
        
    except Exception as e:
        print(f"\n❌ Erro durante o build: {e}")
        print("\nVerifique se o PyInstaller está instalado:")
        print("pip install pyinstaller")
        return False
    
    return True

def create_version_file():
    """Cria arquivo de versão para Windows"""
    version_content = """
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Caçador dos Mares'),
        StringStruct(u'FileDescription', u'Jogo educativo de estratégia naval'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'CacadorDosMares'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2024'),
        StringStruct(u'OriginalFilename', u'CacadorDosMares.exe'),
        StringStruct(u'ProductName', u'Caçador dos Mares'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    with open("version.txt", "w") as f:
        f.write(version_content)

def create_icon_placeholder():
    """Cria um ícone placeholder se não existir"""
    import pygame
    
    # Verifica se a pasta existe
    os.makedirs("assets/images", exist_ok=True)
    
    # Cria um ícone simples
    pygame.init()
    
    sizes = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
    
    for size in sizes:
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Fundo azul oceano
        surface.fill((24, 93, 123))
        
        # Desenha um barco simples
        center_x, center_y = size[0] // 2, size[1] // 2
        boat_size = size[0] // 4
        
        # Casco
        pygame.draw.polygon(surface, (139, 69, 19), [
            (center_x - boat_size, center_y),
            (center_x + boat_size, center_y),
            (center_x + boat_size // 2, center_y + boat_size),
            (center_x - boat_size // 2, center_y + boat_size)
        ])
        
        # Vela
        pygame.draw.polygon(surface, (255, 255, 255), [
            (center_x, center_y - boat_size),
            (center_x, center_y),
            (center_x + boat_size // 2, center_y - boat_size // 2)
        ])
        
        # Mastro
        pygame.draw.line(surface, (100, 50, 0), 
                        (center_x, center_y), 
                        (center_x, center_y - boat_size), 
                        max(1, size[0] // 32))
        
        # Salva o ícone
        pygame.image.save(surface, f"assets/images/icon_{size[0]}.png")
    
    print("✅ Ícones placeholder criados em assets/images/")

if __name__ == "__main__":
    print("=== Build do Caçador dos Mares ===\n")
    
    # Verifica se os diretórios necessários existem
    if not os.path.exists("assets/images"):
        print("Criando ícones placeholder...")
        create_icon_placeholder()
    
    # Cria arquivo de versão para Windows
    if platform.system() == "Windows":
        create_version_file()
    
    # Executa o build
    if build_executable():
        print("\n✅ Processo de build finalizado com sucesso!")
    else:
        print("\n❌ O processo de build falhou.")