#!/usr/bin/env python3
"""
Script de teste de responsividade
Execute para testar o sistema responsivo
"""

import pygame
import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.layout_manager import layout_manager
from config import *

def test_responsiveness():
    """Testa sistema de responsividade"""
    pygame.init()
    
    # Testa diferentes resoluções
    resolutions = [
        (1000, 700),   # Mínimo
        (1280, 720),   # HD
        (1600, 900),   # Padrão
        (1920, 1080),  # Full HD
        (2560, 1440)   # QHD
    ]
    
    print("🧪 TESTE DE RESPONSIVIDADE")
    print("=" * 40)
    
    for width, height in resolutions:
        layout_manager.update_screen_size(width, height)
        
        board_area = layout_manager.get_board_area()
        ui_area = layout_manager.get_ui_area()
        margins = layout_manager.get_margins()
        scale = layout_manager.get_element_scale_factor()
        
        print(f"\n📐 Resolução: {width}x{height}")
        print(f"   Margens: {margins}")
        print(f"   Tabuleiro: {board_area['width']}x{board_area['height']}")
        print(f"   Célula: {board_area['cell_size']}px")
        print(f"   UI: {ui_area['width']}x{ui_area['height']}")
        print(f"   Escala: {scale:.2f}x")
        
        # Testa conversões de coordenadas
        test_pos = layout_manager.get_scaled_board_coordinates(10, 10)
        back_pos = layout_manager.get_screen_to_board_coordinates(test_pos[0], test_pos[1])
        
        if back_pos == (10, 10):
            print(f"   ✓ Conversão de coordenadas OK")
        else:
            print(f"   ✗ Erro na conversão: {back_pos}")
    
    print("\n✅ Teste de responsividade concluído!")
    pygame.quit()

if __name__ == "__main__":
    test_responsiveness()
