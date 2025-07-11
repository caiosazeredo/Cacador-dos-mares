# config.py - Configurações responsivas (ATUALIZADO)

import os

# Configurações da janela - SISTEMA RESPONSIVO
WINDOW_WIDTH = 1600   # Resolução padrão
WINDOW_HEIGHT = 900   # Resolução padrão
FPS = 60
TITLE = "Caçador dos Mares"

# Configurações do tabuleiro - RESPONSIVO
BOARD_SIZE = 20
CELL_SIZE = 64        # Tamanho base das células
BOARD_OFFSET_X = 80   # Offset base
BOARD_OFFSET_Y = 80   # Offset base

# Configurações de tiles
TILE_SIZE = 64
WATER_TILE = "tile_73.png"

# Sistema de escala automática
AUTO_SCALE_UI = True
MIN_SCALE_FACTOR = 0.5
MAX_SCALE_FACTOR = 2.0

# Cores
COLORS = {
    'BACKGROUND': (24, 93, 123),
    'BOARD': (64, 164, 223),
    'GRID': (45, 125, 184),
    'SAND': (238, 203, 173),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'ORANGE': (255, 165, 0),
    'PURPLE': (128, 0, 128),
    'PLAYER_COLORS': [
        (255, 0, 0),      # Vermelho
        (0, 0, 255),      # Azul
        (0, 255, 0),      # Verde
        (255, 255, 0)     # Amarelo
    ]
}

# Configurações do jogo
MAX_PLAYERS = 4
MIN_PLAYERS = 2
INITIAL_FISH_PER_PLAYER = 1
MOVEMENT_LIMIT = 7
COLLECTION_DISTANCE = 2
WINNING_FISH_COUNT = 3

# Configurações de rede
DEFAULT_PORT = 5555
TIMEOUT = 30

# Caminhos
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_PATH, 'assets')
IMAGES_PATH = os.path.join(ASSETS_PATH, 'images')
BARCOS_PATH = os.path.join(IMAGES_PATH, 'Barcos')
TILES_PATH = os.path.join(BARCOS_PATH, 'PNG', 'Retina', 'Tiles')
SOUNDS_PATH = os.path.join(ASSETS_PATH, 'sounds')
FONTS_PATH = os.path.join(ASSETS_PATH, 'fonts')
DATA_PATH = os.path.join(BASE_PATH, 'data')
SAVES_PATH = os.path.join(DATA_PATH, 'saves')

# Configurações de IA
AI_DIFFICULTIES = {
    'FACIL': {
        'name': 'Fácil',
        'think_time': 0.5,
        'random_factor': 0.7,
        'strategy_weight': 0.3
    },
    'MEDIO': {
        'name': 'Médio',
        'think_time': 1.0,
        'random_factor': 0.4,
        'strategy_weight': 0.6
    },
    'DIFICIL': {
        'name': 'Difícil',
        'think_time': 1.5,
        'random_factor': 0.1,
        'strategy_weight': 0.9
    }
}

# Cartas de movimento (vetores)
MOVEMENT_CARDS = [
    (0, 0),    # Sem movimento
    (1, 0),    # Direita
    (-1, 0),   # Esquerda
    (0, 1),    # Baixo
    (0, -1),   # Cima
    (1, 1),    # Diagonal direita-baixo
    (-1, -1),  # Diagonal esquerda-cima
    (1, -1),   # Diagonal direita-cima
    (-1, 1),   # Diagonal esquerda-baixo
    (2, 0),    # Direita forte
    (-2, 0),   # Esquerda forte
    (0, 2),    # Baixo forte
    (0, -2),   # Cima forte
    (2, 1),    # Direita forte + baixo
    (-2, -1),  # Esquerda forte + cima
    (1, 2),    # Direita + baixo forte
    (-1, -2)   # Esquerda + cima forte
]

# Configurações do Steam/Login automático
STEAM_APP_ID = None
AUTO_LOGIN_DEFAULT = True
DEFAULT_USERNAME = "Jogador"

# Teclas de atalho
FULLSCREEN_KEYS = ['F11', 'Alt+Enter']
PAUSE_KEY = 'ESC'
QUICK_EXIT = 'Ctrl+Q'
TOGGLE_AUTO_LOGIN = 'Ctrl+L'
