# src/utils.py - Funções utilitárias responsivas (CORRIGIDO)

import os
import json
import random
import math
import pygame
from config import *

def create_directories():
    """Cria os diretórios necessários para o jogo"""
    directories = [
        ASSETS_PATH,
        IMAGES_PATH,
        BARCOS_PATH,
        TILES_PATH,
        SOUNDS_PATH,
        FONTS_PATH,
        DATA_PATH,
        SAVES_PATH
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def get_responsive_scale():
    """Retorna escala responsiva baseada na tela atual"""
    try:
        from src.layout_manager import layout_manager
        return layout_manager.get_element_scale_factor()
    except:
        # Fallback se layout_manager não estiver disponível
        try:
            screen = pygame.display.get_surface()
            if screen:
                current_width = screen.get_width()
                return current_width / 1280.0  # Escala baseada em 1280 como referência
            return 1.0
        except:
            return 1.0

def get_responsive_font_size(base_size):
    """Retorna tamanho de fonte responsivo"""
    try:
        from src.layout_manager import layout_manager
        return layout_manager.get_font_size(base_size)
    except:
        scale = get_responsive_scale()
        return max(12, int(base_size * scale))

def load_json(filepath):
    """Carrega um arquivo JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_json(filepath, data):
    """Salva dados em um arquivo JSON"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def manhattan_distance(pos1, pos2):
    """Calcula a distância de Manhattan entre duas posições"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def euclidean_distance(pos1, pos2):
    """Calcula a distância euclidiana entre duas posições"""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def is_valid_position(x, y):
    """Verifica se uma posição é válida no tabuleiro"""
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def get_neighbors(x, y):
    """Retorna as posições vizinhas válidas"""
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid_position(nx, ny):
            neighbors.append((nx, ny))
    
    return neighbors

def board_to_screen(board_x, board_y):
    """Converte coordenadas do tabuleiro para coordenadas da tela (responsivo)"""
    try:
        from src.layout_manager import layout_manager
        return layout_manager.get_scaled_board_coordinates(board_x, board_y)
    except:
        # Fallback básico
        scale = get_responsive_scale()
        cell_size = int(64 * scale)
        offset_x = int(80 * scale)
        offset_y = int(80 * scale)
        
        screen_x = offset_x + board_x * cell_size + cell_size // 2
        screen_y = offset_y + board_y * cell_size + cell_size // 2
        return (screen_x, screen_y)

def screen_to_board(screen_x, screen_y):
    """Converte coordenadas da tela para coordenadas do tabuleiro (responsivo)"""
    try:
        from src.layout_manager import layout_manager
        return layout_manager.get_screen_to_board_coordinates(screen_x, screen_y)
    except:
        # Fallback básico
        scale = get_responsive_scale()
        cell_size = int(64 * scale)
        offset_x = int(80 * scale)
        offset_y = int(80 * scale)
        
        board_x = (screen_x - offset_x) // cell_size
        board_y = (screen_y - offset_y) // cell_size
        
        if is_valid_position(board_x, board_y):
            return (board_x, board_y)
        return None

def draw_text(surface, text, x, y, size=24, color=COLORS['WHITE'], center=False, font_name=None):
    """Desenha texto na tela (responsivo)"""
    # Usa tamanho responsivo
    responsive_size = get_responsive_font_size(size)
    
    if font_name and os.path.exists(os.path.join(FONTS_PATH, font_name)):
        font = pygame.font.Font(os.path.join(FONTS_PATH, font_name), responsive_size)
    else:
        font = pygame.font.Font(None, responsive_size)
    
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()
    
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    
    surface.blit(text_surface, text_rect)
    return text_rect

def draw_button(surface, text, x, y, width, height, color, hover_color, text_color=COLORS['WHITE']):
    """Desenha um botão responsivo"""
    # Aplica escala responsiva
    scale = get_responsive_scale()
    scaled_width = int(width * scale)
    scaled_height = int(height * scale)
    
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    
    button_rect = pygame.Rect(x, y, scaled_width, scaled_height)
    
    # Verifica hover
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, button_rect)
        if click:
            return True
    else:
        pygame.draw.rect(surface, color, button_rect)
    
    pygame.draw.rect(surface, COLORS['BLACK'], button_rect, 2)
    
    # Texto centralizado responsivo
    draw_text(surface, text, 
             button_rect.centerx, button_rect.centery,
             size=18, color=text_color, center=True)
    
    return False

def lerp(start, end, progress):
    """Interpolação linear"""
    return start + (end - start) * progress

def clamp(value, min_value, max_value):
    """Limita um valor entre min e max"""
    return max(min_value, min(value, max_value))

def normalize_vector(vector):
    """Normaliza um vetor"""
    length = math.sqrt(vector[0]**2 + vector[1]**2)
    if length == 0:
        return (0, 0)
    return (vector[0] / length, vector[1] / length)

def point_in_rect(point, rect):
    """Verifica se um ponto está dentro de um retângulo"""
    x, y = point
    return rect.x <= x <= rect.x + rect.width and rect.y <= y <= rect.y + rect.height

def create_gradient_surface(width, height, start_color, end_color, vertical=True):
    """Cria uma superfície com gradiente (responsivo)"""
    scale = get_responsive_scale()
    scaled_width = max(1, int(width * scale))
    scaled_height = max(1, int(height * scale))
    
    surface = pygame.Surface((scaled_width, scaled_height))
    
    if vertical:
        for y in range(scaled_height):
            t = y / scaled_height if scaled_height > 0 else 0
            color = [
                int(lerp(start_color[i], end_color[i], t))
                for i in range(3)
            ]
            pygame.draw.line(surface, color, (0, y), (scaled_width, y))
    else:
        for x in range(scaled_width):
            t = x / scaled_width if scaled_width > 0 else 0
            color = [
                int(lerp(start_color[i], end_color[i], t))
                for i in range(3)
            ]
            pygame.draw.line(surface, color, (x, 0), (x, scaled_height))
    
    return surface

def generate_random_position(occupied_positions):
    """Gera uma posição aleatória não ocupada no tabuleiro"""
    available_positions = []
    
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if (x, y) not in occupied_positions:
                available_positions.append((x, y))
    
    if available_positions:
        return random.choice(available_positions)
    return None

def format_time(seconds):
    """Formata tempo em segundos para MM:SS"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def show_notification(surface, message, duration=3.0):
    """Mostra notificação temporária na tela"""
    font_size = get_responsive_font_size(20)
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(message, True, COLORS['WHITE'])
    
    # Posição responsiva no canto superior direito
    scale = get_responsive_scale()
    margin = int(20 * scale)
    
    x = surface.get_width() - text_surface.get_width() - margin
    y = margin
    
    # Background responsivo
    bg_rect = text_surface.get_rect()
    bg_rect.x = x - int(10 * scale)
    bg_rect.y = y - int(5 * scale)
    bg_rect.width += int(20 * scale)
    bg_rect.height += int(10 * scale)
    
    pygame.draw.rect(surface, (0, 0, 0, 180), bg_rect)
    pygame.draw.rect(surface, COLORS['WHITE'], bg_rect, 2)
    
    surface.blit(text_surface, (x, y))
