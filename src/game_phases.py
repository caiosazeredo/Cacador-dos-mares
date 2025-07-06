# src/game_phases.py - Sistema de fases do jogo

import pygame
from config import *
from src.utils import draw_text, create_gradient_surface

class GamePhaseManager:
    """Gerenciador de fases do jogo Caçador dos Mares"""
    
    def __init__(self):
        self.current_phase = 'setup'
        self.turn_number = 1
        self.current_player_index = 0
        self.total_players = 2
        self.phase_timer = 0
        self.phase_transition_time = 1.0
        self.is_transitioning = False
        
        # Fases do jogo baseadas no documento
        self.phases = {
            'setup': {
                'name': 'Posicionamento Inicial',
                'description': 'Posicione seu barco no tabuleiro',
                'color': (100, 150, 255),
                'instruction': 'Clique em uma posição válida para colocar seu barco',
                'next': 'preparation'
            },
            'preparation': {
                'name': 'Fase de Preparação',
                'description': 'Compre cartas até ter 3 na mão',
                'color': (255, 200, 100),
                'instruction': 'Cartas sendo distribuídas automaticamente...',
                'next': 'play_cards'
            },
            'play_cards': {
                'name': 'Fase de Jogar Cartas',
                'description': 'Escolha uma carta para jogar (face para baixo)',
                'color': (255, 100, 150),
                'instruction': 'Selecione uma carta da sua mão e confirme',
                'next': 'movement'
            },
            'movement': {
                'name': 'Fase de Movimentação',
                'description': 'Mova seu barco pelo tabuleiro',
                'color': (150, 255, 100),
                'instruction': 'Clique onde deseja mover (limite: 7 casas)',
                'next': 'resolution'
            },
            'resolution': {
                'name': 'Fase de Apuração',
                'description': 'Cartas reveladas, peixes se movem',
                'color': (255, 150, 255),
                'instruction': 'Processando resultado das cartas...',
                'next': 'preparation'
            },
            'game_over': {
                'name': 'Fim de Jogo',
                'description': 'Alguém coletou 3 peixes!',
                'color': (255, 255, 100),
                'instruction': 'Parabéns ao vencedor!',
                'next': None
            }
        }
        
        # UI de fases
        self.phase_panel_height = 120
        self.notification_queue = []
        
    def set_phase(self, new_phase, player_index=None):
        """Define nova fase do jogo"""
        if new_phase in self.phases:
            self.current_phase = new_phase
            self.phase_timer = 0
            self.is_transitioning = True
            
            if player_index is not None:
                self.current_player_index = player_index
            
            # Adiciona notificação de mudança de fase
            phase_info = self.phases[new_phase]
            self.add_notification(f"Turno {self.turn_number}: {phase_info['name']}")
    
    def next_phase(self):
        """Avança para a próxima fase"""
        current_info = self.phases[self.current_phase]
        next_phase = current_info['next']
        
        if next_phase:
            # Se voltou para preparação, incrementa turno
            if next_phase == 'preparation':
                self.turn_number += 1
            
            self.set_phase(next_phase)
        return next_phase
    
    def get_current_phase_info(self):
        """Retorna informações da fase atual"""
        return self.phases.get(self.current_phase, {})
    
    def get_phase_instruction(self):
        """Retorna instrução da fase atual"""
        phase_info = self.get_current_phase_info()
        instruction = phase_info.get('instruction', '')
        
        # Personaliza instrução com informações do jogador atual
        if self.current_phase in ['play_cards', 'movement']:
            instruction = f"Jogador {self.current_player_index + 1}: {instruction}"
        
        return instruction
    
    def add_notification(self, message, duration=3.0):
        """Adiciona notificação temporária"""
        self.notification_queue.append({
            'message': message,
            'duration': duration,
            'timer': 0
        })
    
    def update(self, dt):
        """Atualiza sistema de fases"""
        self.phase_timer += dt
        
        # Atualiza transição de fase
        if self.is_transitioning and self.phase_timer >= self.phase_transition_time:
            self.is_transitioning = False
        
        # Atualiza notificações
        for notification in self.notification_queue[:]:
            notification['timer'] += dt
            if notification['timer'] >= notification['duration']:
                self.notification_queue.remove(notification)
    
    def draw_phase_panel(self, surface):
        """Desenha painel de informações da fase"""
        screen_width = surface.get_width()
        panel_rect = pygame.Rect(0, 0, screen_width, self.phase_panel_height)
        
        # Background do painel
        phase_info = self.get_current_phase_info()
        bg_color = phase_info.get('color', (100, 100, 100))
        
        # Gradiente de fundo
        gradient = create_gradient_surface(
            screen_width, self.phase_panel_height,
            bg_color, tuple(max(0, c - 50) for c in bg_color)
        )
        surface.blit(gradient, panel_rect)
        
        # Borda do painel
        pygame.draw.rect(surface, COLORS['WHITE'], panel_rect, 3)
        
        # Efeito de transição
        if self.is_transitioning:
            alpha = int(100 * (1 - self.phase_timer / self.phase_transition_time))
            overlay = pygame.Surface((screen_width, self.phase_panel_height), pygame.SRCALPHA)
            overlay.set_alpha(alpha)
            overlay.fill((255, 255, 255))
            surface.blit(overlay, panel_rect)
        
        # Texto da fase
        y_offset = 15
        
        # Título da fase
        draw_text(surface, f"TURNO {self.turn_number}", 20, y_offset,
                 size=20, color=COLORS['WHITE'])
        
        phase_name = phase_info.get('name', 'Fase Desconhecida')
        draw_text(surface, phase_name, 20, y_offset + 25,
                 size=28, color=COLORS['WHITE'])
        
        # Descrição
        description = phase_info.get('description', '')
        draw_text(surface, description, 20, y_offset + 55,
                 size=18, color=COLORS['WHITE'])
        
        # Instrução
        instruction = self.get_phase_instruction()
        draw_text(surface, instruction, 20, y_offset + 80,
                 size=16, color=COLORS['YELLOW'])
        
        # Indicador de progresso das fases
        self.draw_phase_progress(surface, screen_width - 300, y_offset)
    
    def draw_phase_progress(self, surface, x, y):
        """Desenha indicador de progresso das fases"""
        phase_order = ['preparation', 'play_cards', 'movement', 'resolution']
        circle_radius = 12
        spacing = 60
        
        for i, phase in enumerate(phase_order):
            circle_x = x + i * spacing
            circle_y = y + 30
            
            # Cor do círculo baseada no estado
            if phase == self.current_phase:
                color = COLORS['YELLOW']  # Fase atual
                pygame.draw.circle(surface, color, (circle_x, circle_y), circle_radius + 2)
            elif phase_order.index(phase) < phase_order.index(self.current_phase):
                color = COLORS['GREEN']   # Fase completa
            else:
                color = (100, 100, 100)   # Fase futura
            
            pygame.draw.circle(surface, color, (circle_x, circle_y), circle_radius)
            pygame.draw.circle(surface, COLORS['WHITE'], (circle_x, circle_y), circle_radius, 2)
            
            # Linha conectora
            if i < len(phase_order) - 1:
                line_start = (circle_x + circle_radius, circle_y)
                line_end = (circle_x + spacing - circle_radius, circle_y)
                pygame.draw.line(surface, COLORS['WHITE'], line_start, line_end, 2)
            
            # Nome da fase (abreviado)
            phase_names = {
                'preparation': 'PREP',
                'play_cards': 'CARTAS',
                'movement': 'MOVE',
                'resolution': 'RESOL'
            }
            
            text = phase_names.get(phase, phase[:4].upper())
            draw_text(surface, text, circle_x, circle_y + 25,
                     size=12, color=COLORS['WHITE'], center=True)
    
    def draw_notifications(self, surface):
        """Desenha notificações temporárias"""
        screen_height = surface.get_height()
        y_offset = screen_height - 200
        
        for i, notification in enumerate(self.notification_queue):
            # Calcula alpha baseado no tempo restante
            remaining_ratio = 1 - (notification['timer'] / notification['duration'])
            alpha = int(255 * remaining_ratio)
            
            if alpha > 0:
                # Background da notificação
                text_surface = pygame.font.Font(None, 24).render(
                    notification['message'], True, COLORS['WHITE']
                )
                
                padding = 20
                bg_width = text_surface.get_width() + padding * 2
                bg_height = text_surface.get_height() + padding
                
                bg_rect = pygame.Rect(
                    surface.get_width() - bg_width - 20,
                    y_offset - i * (bg_height + 10),
                    bg_width, bg_height
                )
                
                # Superfície com transparência
                notification_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
                notification_surface.set_alpha(alpha)
                notification_surface.fill((0, 0, 0, 180))
                
                surface.blit(notification_surface, bg_rect)
                pygame.draw.rect(surface, COLORS['WHITE'], bg_rect, 2)
                
                # Texto da notificação
                text_rect = text_surface.get_rect()
                text_rect.center = bg_rect.center
                surface.blit(text_surface, text_rect)

# Instância global
game_phase_manager = GamePhaseManager()
