# src/achievements.py - Sistema de conquistas

import pygame
import os
import json
from config import *
from src.utils import draw_text, draw_button, load_json, save_json, create_gradient_surface

class Achievement:
    """Representa uma conquista individual"""
    
    def __init__(self, achievement_data):
        self.id = achievement_data['id']
        self.name = achievement_data['name']
        self.description = achievement_data['description']
        self.icon = achievement_data.get('icon', '🏆')
        self.category = achievement_data.get('category', 'Geral')
        self.points = achievement_data.get('points', 10)
        self.hidden = achievement_data.get('hidden', False)
        
        # Condições para desbloquear
        self.conditions = achievement_data.get('conditions', {})
        
        # Estado
        self.unlocked = False
        self.unlock_date = None
        self.progress = 0
        self.max_progress = achievement_data.get('max_progress', 1)
    
    def check_unlock(self, stats):
        """Verifica se a conquista deve ser desbloqueada"""
        if self.unlocked:
            return False
        
        # Verifica cada condição
        for condition_type, condition_value in self.conditions.items():
            if condition_type == 'fish_collected':
                if stats.get('total_fish', 0) >= condition_value:
                    self.progress = min(stats.get('total_fish', 0), condition_value)
                else:
                    return False
                    
            elif condition_type == 'games_won':
                if stats.get('total_wins', 0) >= condition_value:
                    self.progress = min(stats.get('total_wins', 0), condition_value)
                else:
                    return False
                    
            elif condition_type == 'perfect_game':
                # Venceu sem deixar ninguém coletar peixes
                if stats.get('perfect_games', 0) >= condition_value:
                    self.progress = 1
                else:
                    return False
                    
            elif condition_type == 'story_chapter':
                # Completou um capítulo específico
                if condition_value in stats.get('completed_chapters', []):
                    self.progress = 1
                else:
                    return False
                    
            elif condition_type == 'consecutive_wins':
                if stats.get('win_streak', 0) >= condition_value:
                    self.progress = min(stats.get('win_streak', 0), condition_value)
                else:
                    return False
        
        # Todas as condições foram atendidas
        self.unlocked = True
        self.unlock_date = pygame.time.get_ticks()
        return True
    
    def get_progress_percentage(self):
        """Retorna o progresso em porcentagem"""
        if self.max_progress == 0:
            return 100 if self.unlocked else 0
        return int((self.progress / self.max_progress) * 100)


class AchievementManager:
    """Gerencia todas as conquistas do jogo"""
    
    def __init__(self):
        self.achievements = self.load_achievements()
        self.categories = self.get_categories()
        
    def load_achievements(self):
        """Carrega todas as conquistas"""
        # Em produção, isso seria carregado de um arquivo JSON
        achievements_data = [
            # Conquistas de Coleta
            {
                'id': 'first_fish',
                'name': 'Primeiro Peixe',
                'description': 'Colete seu primeiro peixe',
                'icon': '🐟',
                'category': 'Coleta',
                'points': 10,
                'conditions': {'fish_collected': 1}
            },
            {
                'id': 'fish_collector_10',
                'name': 'Pescador Iniciante',
                'description': 'Colete 10 peixes no total',
                'icon': '🎣',
                'category': 'Coleta',
                'points': 20,
                'conditions': {'fish_collected': 10},
                'max_progress': 10
            },
            {
                'id': 'fish_collector_50',
                'name': 'Pescador Experiente',
                'description': 'Colete 50 peixes no total',
                'icon': '🐠',
                'category': 'Coleta',
                'points': 50,
                'conditions': {'fish_collected': 50},
                'max_progress': 50
            },
            {
                'id': 'fish_collector_100',
                'name': 'Mestre Pescador',
                'description': 'Colete 100 peixes no total',
                'icon': '🦈',
                'category': 'Coleta',
                'points': 100,
                'conditions': {'fish_collected': 100},
                'max_progress': 100
            },
            
            # Conquistas de Vitória
            {
                'id': 'first_win',
                'name': 'Primeira Vitória',
                'description': 'Vença sua primeira partida',
                'icon': '🏆',
                'category': 'Vitória',
                'points': 15,
                'conditions': {'games_won': 1}
            },
            {
                'id': 'winner_10',
                'name': 'Vencedor',
                'description': 'Vença 10 partidas',
                'icon': '🥇',
                'category': 'Vitória',
                'points': 40,
                'conditions': {'games_won': 10},
                'max_progress': 10
            },
            {
                'id': 'perfect_game',
                'name': 'Jogo Perfeito',
                'description': 'Vença uma partida sem deixar oponentes coletarem peixes',
                'icon': '💎',
                'category': 'Vitória',
                'points': 50,
                'conditions': {'perfect_game': 1}
            },
            {
                'id': 'win_streak_5',
                'name': 'Invencível',
                'description': 'Vença 5 partidas consecutivas',
                'icon': '🔥',
                'category': 'Vitória',
                'points': 60,
                'conditions': {'consecutive_wins': 5},
                'max_progress': 5
            },
            
            # Conquistas de História
            {
                'id': 'story_chapter_1',
                'name': 'Começo da Jornada',
                'description': 'Complete o Capítulo 1',
                'icon': '📖',
                'category': 'História',
                'points': 25,
                'conditions': {'story_chapter': 1}
            },
            {
                'id': 'story_chapter_2',
                'name': 'Águas Profundas',
                'description': 'Complete o Capítulo 2',
                'icon': '🌊',
                'category': 'História',
                'points': 30,
                'conditions': {'story_chapter': 2}
            },
            {
                'id': 'story_chapter_3',
                'name': 'Competidor',
                'description': 'Complete o Capítulo 3',
                'icon': '⚓',
                'category': 'História',
                'points': 40,
                'conditions': {'story_chapter': 3}
            },
            {
                'id': 'story_complete',
                'name': 'Lenda dos Mares',
                'description': 'Complete todos os capítulos da história',
                'icon': '👑',
                'category': 'História',
                'points': 100,
                'conditions': {'story_chapter': 4}
            },
            
            # Conquistas Especiais
            {
                'id': 'lucky_seven',
                'name': 'Número da Sorte',
                'description': 'Colete exatamente 7 peixes em uma partida',
                'icon': '🍀',
                'category': 'Especial',
                'points': 30,
                'hidden': True
            },
            {
                'id': 'explorer',
                'name': 'Explorador',
                'description': 'Visite todos os cantos do tabuleiro em uma partida',
                'icon': '🗺️',
                'category': 'Especial',
                'points': 25,
                'hidden': True
            },
            {
                'id': 'strategist',
                'name': 'Estrategista',
                'description': 'Vença usando apenas cartas de movimento zero',
                'icon': '🧠',
                'category': 'Especial',
                'points': 75,
                'hidden': True
            }
        ]
        
        return [Achievement(data) for data in achievements_data]
    
    def get_categories(self):
        """Retorna todas as categorias de conquistas"""
        categories = set()
        for achievement in self.achievements:
            categories.add(achievement.category)
        return sorted(list(categories))
    
    def check_achievements(self, username, stats):
        """Verifica e desbloqueia conquistas"""
        unlocked = []
        
        for achievement in self.achievements:
            if achievement.check_unlock(stats):
                unlocked.append(achievement)
        
        return unlocked
    
    def get_total_points(self):
        """Retorna o total de pontos desbloqueados"""
        return sum(a.points for a in self.achievements if a.unlocked)
    
    def get_unlocked_count(self):
        """Retorna quantas conquistas foram desbloqueadas"""
        return sum(1 for a in self.achievements if a.unlocked)
    
    def save_progress(self, username):
        """Salva o progresso das conquistas"""
        data = {
            'achievements': {}
        }
        
        for achievement in self.achievements:
            data['achievements'][achievement.id] = {
                'unlocked': achievement.unlocked,
                'unlock_date': achievement.unlock_date,
                'progress': achievement.progress
            }
        
        filepath = os.path.join(SAVES_PATH, f"{username}_achievements.json")
        save_json(filepath, data)
    
    def load_progress(self, username):
        """Carrega o progresso das conquistas"""
        filepath = os.path.join(SAVES_PATH, f"{username}_achievements.json")
        data = load_json(filepath)
        
        if data and 'achievements' in data:
            for achievement in self.achievements:
                if achievement.id in data['achievements']:
                    saved = data['achievements'][achievement.id]
                    achievement.unlocked = saved.get('unlocked', False)
                    achievement.unlock_date = saved.get('unlock_date')
                    achievement.progress = saved.get('progress', 0)


class AchievementScreen:
    """Tela de visualização de conquistas"""
    
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.clock = pygame.time.Clock()
        
        # Gerenciador de conquistas
        self.manager = AchievementManager()
        self.manager.load_progress(username)
        
        # Visual
        self.background = create_gradient_surface(WINDOW_WIDTH, WINDOW_HEIGHT,
                                                (30, 30, 50), (50, 50, 100))
        
        # Estado
        self.selected_category = 'Todas'
        self.scroll_offset = 0
        self.max_scroll = 0
        
    def run(self):
        """Executa a tela de conquistas"""
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clique esquerdo
                        self.handle_click(event.pos)
                    elif event.button == 4:  # Scroll up
                        self.scroll_offset = max(0, self.scroll_offset - 50)
                    elif event.button == 5:  # Scroll down
                        self.scroll_offset = min(self.max_scroll, self.scroll_offset + 50)
            
            self.draw()
            pygame.display.flip()
    
    def handle_click(self, pos):
        """Processa cliques"""
        x, y = pos
        
        # Verifica clique nas categorias
        category_y = 120
        category_x = 50
        
        for i, category in enumerate(['Todas'] + self.manager.categories):
            button_rect = pygame.Rect(category_x + i * 150, category_y, 140, 40)
            if button_rect.collidepoint(pos):
                self.selected_category = category
                self.scroll_offset = 0
                break
    
    def get_filtered_achievements(self):
        """Retorna conquistas filtradas pela categoria"""
        if self.selected_category == 'Todas':
            return self.manager.achievements
        
        return [a for a in self.manager.achievements 
                if a.category == self.selected_category]
    
    def draw(self):
        """Desenha a tela de conquistas"""
        self.screen.blit(self.background, (0, 0))
        
        # Título
        draw_text(self.screen, "CONQUISTAS", WINDOW_WIDTH // 2, 40,
                 size=48, color=COLORS['WHITE'], center=True)
        
        # Estatísticas
        total_unlocked = self.manager.get_unlocked_count()
        total_achievements = len(self.manager.achievements)
        total_points = self.manager.get_total_points()
        
        stats_text = f"Desbloqueadas: {total_unlocked}/{total_achievements} | Pontos: {total_points}"
        draw_text(self.screen, stats_text, WINDOW_WIDTH // 2, 80,
                 size=24, color=COLORS['YELLOW'], center=True)
        
        # Categorias
        category_y = 120
        category_x = 50
        
        for i, category in enumerate(['Todas'] + self.manager.categories):
            color = COLORS['YELLOW'] if category == self.selected_category else COLORS['WHITE']
            
            if draw_button(self.screen, category, category_x + i * 150, category_y,
                          140, 40, (50, 50, 100), (70, 70, 120), color):
                self.selected_category = category
                self.scroll_offset = 0
        
        # Área de conquistas com clipping
        achievements_area = pygame.Rect(50, 180, WINDOW_WIDTH - 100, WINDOW_HEIGHT - 230)
        self.screen.set_clip(achievements_area)
        
        # Conquistas
        achievements = self.get_filtered_achievements()
        y_offset = 180 - self.scroll_offset
        achievement_height = 100
        
        for achievement in achievements:
            if y_offset + achievement_height > 180 and y_offset < WINDOW_HEIGHT - 50:
                self.draw_achievement(achievement, 70, y_offset)
            
            y_offset += achievement_height + 10
        
        # Calcula scroll máximo
        self.max_scroll = max(0, y_offset + self.scroll_offset - WINDOW_HEIGHT + 100)
        
        # Remove clipping
        self.screen.set_clip(None)
        
        # Barra de scroll
        if self.max_scroll > 0:
            scroll_height = achievements_area.height
            scroll_bar_height = max(20, (scroll_height / (self.max_scroll + scroll_height)) * scroll_height)
            scroll_bar_y = 180 + (self.scroll_offset / self.max_scroll) * (scroll_height - scroll_bar_height)
            
            pygame.draw.rect(self.screen, (100, 100, 100),
                           (WINDOW_WIDTH - 40, scroll_bar_y, 20, scroll_bar_height))
        
        # Instruções
        draw_text(self.screen, "ESC para voltar | Use o scroll do mouse para navegar",
                 WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30,
                 size=18, color=COLORS['WHITE'], center=True)
    
    def draw_achievement(self, achievement, x, y):
        """Desenha uma conquista individual"""
        width = WINDOW_WIDTH - 140
        height = 90
        
        # Fundo
        if achievement.unlocked:
            bg_color = (40, 80, 40)  # Verde escuro
            border_color = (100, 200, 100)
        else:
            bg_color = (40, 40, 40)  # Cinza escuro
            border_color = (80, 80, 80)
        
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, bg_color, rect)
        pygame.draw.rect(self.screen, border_color, rect, 2)
        
        # Ícone
        icon_size = 60
        icon_x = x + 20
        icon_y = y + 15
        
        # Fundo do ícone
        icon_bg_color = (60, 60, 60) if not achievement.unlocked else (80, 120, 80)
        pygame.draw.rect(self.screen, icon_bg_color,
                        (icon_x, icon_y, icon_size, icon_size))
        pygame.draw.rect(self.screen, border_color,
                        (icon_x, icon_y, icon_size, icon_size), 2)
        
        # Emoji do ícone (simulado com texto)
        if achievement.unlocked or not achievement.hidden:
            draw_text(self.screen, achievement.icon, icon_x + icon_size // 2, icon_y + icon_size // 2,
                     size=40, color=COLORS['WHITE'], center=True)
        else:
            draw_text(self.screen, "?", icon_x + icon_size // 2, icon_y + icon_size // 2,
                     size=40, color=COLORS['WHITE'], center=True)
        
        # Nome
        name_x = icon_x + icon_size + 20
        name_y = y + 10
        
        if achievement.unlocked or not achievement.hidden:
            name_color = COLORS['WHITE'] if achievement.unlocked else (150, 150, 150)
            draw_text(self.screen, achievement.name, name_x, name_y,
                     size=24, color=name_color)
        else:
            draw_text(self.screen, "???", name_x, name_y,
                     size=24, color=(150, 150, 150))
        
        # Descrição
        if achievement.unlocked or not achievement.hidden:
            desc_color = (200, 200, 200) if achievement.unlocked else (120, 120, 120)
            draw_text(self.screen, achievement.description, name_x, name_y + 30,
                     size=18, color=desc_color)
        else:
            draw_text(self.screen, "Conquista secreta", name_x, name_y + 30,
                     size=18, color=(120, 120, 120))
        
        # Pontos
        points_text = f"{achievement.points} pts"
        points_color = COLORS['YELLOW'] if achievement.unlocked else (100, 100, 100)
        draw_text(self.screen, points_text, x + width - 100, y + 20,
                 size=20, color=points_color)
        
        # Barra de progresso
        if not achievement.unlocked and achievement.max_progress > 1:
            progress_bar_x = name_x
            progress_bar_y = y + 65
            progress_bar_width = 300
            progress_bar_height = 10
            
            # Fundo da barra
            pygame.draw.rect(self.screen, (60, 60, 60),
                           (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
            
            # Progresso
            progress_width = int((achievement.progress / achievement.max_progress) * progress_bar_width)
            pygame.draw.rect(self.screen, (100, 150, 100),
                           (progress_bar_x, progress_bar_y, progress_width, progress_bar_height))
            
            # Borda
            pygame.draw.rect(self.screen, (100, 100, 100),
                           (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 1)
            
            # Texto de progresso
            progress_text = f"{achievement.progress}/{achievement.max_progress}"
            draw_text(self.screen, progress_text, progress_bar_x + progress_bar_width + 10, progress_bar_y - 2,
                     size=16, color=(150, 150, 150))