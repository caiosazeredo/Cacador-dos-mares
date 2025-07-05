# src/story.py - Modo história do jogo

import pygame
import json
import os
from config import *
from src.game import Game
from src.utils import draw_text, draw_button, create_gradient_surface, load_json, save_json

class StoryChapter:
    """Representa um capítulo da história"""
    
    def __init__(self, chapter_data):
        self.id = chapter_data['id']
        self.title = chapter_data['title']
        self.description = chapter_data['description']
        self.objectives = chapter_data['objectives']
        self.dialogue = chapter_data.get('dialogue', [])
        self.rewards = chapter_data.get('rewards', {})
        
        # Configurações especiais do capítulo
        self.num_opponents = chapter_data.get('num_opponents', 1)
        self.ai_difficulty = chapter_data.get('ai_difficulty', 'MEDIO')
        self.special_rules = chapter_data.get('special_rules', {})
        self.win_conditions = chapter_data.get('win_conditions', {})
        
        # Estado
        self.completed = False
        self.best_score = None
        self.attempts = 0


class StoryMode:
    """Modo história do jogo"""
    
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.clock = pygame.time.Clock()
        
        # Capítulos
        self.chapters = self.load_chapters()
        self.current_chapter_index = 0
        self.current_chapter = None
        
        # Estado
        self.state = 'menu'  # menu, intro, game, victory, defeat
        self.current_game = None
        self.dialogue_index = 0
        self.dialogue_timer = 0
        
        # Progresso
        self.progress_file = os.path.join(SAVES_PATH, f"{username}_story.json")
        self.progress = self.load_progress()
        
        # Visual
        self.background = create_gradient_surface(WINDOW_WIDTH, WINDOW_HEIGHT,
                                                (20, 40, 60), (40, 80, 120))
        
    def load_chapters(self):
        """Carrega os capítulos da história"""
        # Por enquanto, vamos criar capítulos hardcoded
        # Em produção, isso seria carregado de um arquivo JSON
        chapters_data = [
            {
                'id': 1,
                'title': 'O Pescador Iniciante',
                'description': 'Aprenda os conceitos básicos da pesca em alto mar.',
                'objectives': [
                    'Colete 3 peixes',
                    'Vença seu primeiro oponente'
                ],
                'dialogue': [
                    {
                        'speaker': 'Capitão Silva',
                        'text': 'Bem-vindo ao mar, jovem pescador!'
                    },
                    {
                        'speaker': 'Capitão Silva',
                        'text': 'Vou te ensinar os segredos da pesca.'
                    },
                    {
                        'speaker': 'Capitão Silva',
                        'text': 'Use as correntes marítimas a seu favor!'
                    }
                ],
                'num_opponents': 1,
                'ai_difficulty': 'FACIL',
                'rewards': {
                    'xp': 100,
                    'title': 'Pescador Novato'
                }
            },
            {
                'id': 2,
                'title': 'Águas Turbulentas',
                'description': 'As correntes estão mais fortes. Adapte sua estratégia!',
                'objectives': [
                    'Colete 3 peixes',
                    'Vença em menos de 10 turnos'
                ],
                'dialogue': [
                    {
                        'speaker': 'Capitão Silva',
                        'text': 'As águas estão agitadas hoje...'
                    },
                    {
                        'speaker': 'Capitão Silva',
                        'text': 'Você precisará ser mais estratégico!'
                    }
                ],
                'num_opponents': 1,
                'ai_difficulty': 'MEDIO',
                'special_rules': {
                    'stronger_currents': True  # Cartas têm efeito dobrado
                },
                'rewards': {
                    'xp': 200,
                    'title': 'Navegador'
                }
            },
            {
                'id': 3,
                'title': 'Competição no Porto',
                'description': 'Enfrente múltiplos pescadores experientes!',
                'objectives': [
                    'Colete 3 peixes',
                    'Termine em primeiro lugar'
                ],
                'dialogue': [
                    {
                        'speaker': 'Pescador Rival',
                        'text': 'Acha que pode competir conosco?'
                    },
                    {
                        'speaker': 'Você',
                        'text': 'Vou mostrar quem é o melhor pescador!'
                    }
                ],
                'num_opponents': 2,
                'ai_difficulty': 'MEDIO',
                'rewards': {
                    'xp': 300,
                    'title': 'Competidor'
                }
            },
            {
                'id': 4,
                'title': 'O Torneio dos Mestres',
                'description': 'O desafio final! Prove que você é o melhor!',
                'objectives': [
                    'Colete 5 peixes',
                    'Vença 3 oponentes difíceis'
                ],
                'dialogue': [
                    {
                        'speaker': 'Mestre dos Mares',
                        'text': 'Poucos chegaram até aqui...'
                    },
                    {
                        'speaker': 'Mestre dos Mares',
                        'text': 'Mostre-me suas habilidades!'
                    }
                ],
                'num_opponents': 3,
                'ai_difficulty': 'DIFICIL',
                'win_conditions': {
                    'fish_required': 5  # Precisa de 5 peixes para vencer
                },
                'rewards': {
                    'xp': 500,
                    'title': 'Mestre dos Mares'
                }
            }
        ]
        
        return [StoryChapter(data) for data in chapters_data]
    
    def load_progress(self):
        """Carrega o progresso salvo"""
        progress = load_json(self.progress_file)
        
        if not progress:
            # Novo progresso
            progress = {
                'current_chapter': 0,
                'completed_chapters': [],
                'total_xp': 0,
                'titles': [],
                'statistics': {
                    'total_fish': 0,
                    'total_wins': 0,
                    'total_games': 0
                }
            }
        
        # Atualiza estado dos capítulos
        for chapter_id in progress.get('completed_chapters', []):
            for chapter in self.chapters:
                if chapter.id == chapter_id:
                    chapter.completed = True
        
        return progress
    
    def save_progress(self):
        """Salva o progresso"""
        save_json(self.progress_file, self.progress)
    
    def start_chapter(self, chapter_index):
        """Inicia um capítulo"""
        if 0 <= chapter_index < len(self.chapters):
            self.current_chapter_index = chapter_index
            self.current_chapter = self.chapters[chapter_index]
            self.dialogue_index = 0
            self.state = 'intro'
            
            # Incrementa tentativas
            self.current_chapter.attempts += 1
    
    def start_chapter_game(self):
        """Inicia o jogo do capítulo atual"""
        chapter = self.current_chapter
        
        # Cria jogo com configurações do capítulo
        self.current_game = StoryGame(
            self.screen,
            self.username,
            chapter.num_opponents + 1,
            chapter.ai_difficulty,
            chapter
        )
        
        self.state = 'game'
    
    def handle_event(self, event):
        """Processa eventos"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == 'menu':
                    return 'quit'
                else:
                    self.state = 'menu'
                    return None
        
        if self.state == 'menu':
            return self.handle_menu_event(event)
        
        elif self.state == 'intro':
            return self.handle_intro_event(event)
        
        elif self.state == 'game':
            if self.current_game:
                result = self.current_game.handle_event(event)
                
                if result == 'quit':
                    self.state = 'menu'
                    self.current_game = None
                
                return None
        
        elif self.state in ['victory', 'defeat']:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'menu'
        
        return None
    
    def handle_menu_event(self, event):
        """Processa eventos do menu"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            
            # Verifica clique nos capítulos
            for i, (x, y, w, h) in enumerate(self.chapter_rects):
                if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                    # Verifica se o capítulo está desbloqueado
                    if i == 0 or self.chapters[i-1].completed:
                        self.start_chapter(i)
                    return None
        
        return None
    
    def handle_intro_event(self, event):
        """Processa eventos da introdução"""
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.dialogue_index += 1
            
            if self.dialogue_index >= len(self.current_chapter.dialogue):
                # Fim do diálogo, inicia o jogo
                self.start_chapter_game()
        
        return None
    
    def update(self, dt):
        """Atualiza o modo história"""
        if self.state == 'game' and self.current_game:
            self.current_game.update(dt)
            
            # Verifica se o jogo terminou
            if self.current_game.phase == 'game_over':
                if self.current_game.winner:
                    # Verifica se o jogador venceu
                    player_won = False
                    
                    if isinstance(self.current_game.winner, list):
                        # Empate - verifica se o jogador está entre os vencedores
                        for winner in self.current_game.winner:
                            if winner.id == 0:  # Jogador principal é sempre ID 0
                                player_won = True
                                break
                    else:
                        # Vitória única
                        if self.current_game.winner.id == 0:
                            player_won = True
                    
                    if player_won:
                        self.on_chapter_victory()
                    else:
                        self.on_chapter_defeat()
        
        elif self.state == 'intro':
            self.dialogue_timer += dt
    
    def on_chapter_victory(self):
        """Chamado quando o jogador vence o capítulo"""
        self.state = 'victory'
        
        # Marca capítulo como completo
        if not self.current_chapter.completed:
            self.current_chapter.completed = True
            self.progress['completed_chapters'].append(self.current_chapter.id)
            
            # Adiciona recompensas
            rewards = self.current_chapter.rewards
            if 'xp' in rewards:
                self.progress['total_xp'] += rewards['xp']
            if 'title' in rewards and rewards['title'] not in self.progress['titles']:
                self.progress['titles'].append(rewards['title'])
        
        # Atualiza estatísticas
        stats = self.current_game.players[0].get_stats()
        self.progress['statistics']['total_fish'] += stats['fish_collected']
        self.progress['statistics']['total_wins'] += 1
        self.progress['statistics']['total_games'] += 1
        
        # Desbloqueia próximo capítulo
        if self.current_chapter_index < len(self.chapters) - 1:
            self.progress['current_chapter'] = self.current_chapter_index + 1
        
        self.save_progress()
    
    def on_chapter_defeat(self):
        """Chamado quando o jogador perde o capítulo"""
        self.state = 'defeat'
        
        # Atualiza estatísticas
        self.progress['statistics']['total_games'] += 1
        self.save_progress()
    
    def draw(self):
        """Desenha o modo história"""
        if self.state == 'menu':
            self.draw_menu()
        elif self.state == 'intro':
            self.draw_intro()
        elif self.state == 'game':
            if self.current_game:
                self.current_game.draw()
        elif self.state == 'victory':
            self.draw_victory()
        elif self.state == 'defeat':
            self.draw_defeat()
    
    def draw_menu(self):
        """Desenha o menu de seleção de capítulos"""
        self.screen.blit(self.background, (0, 0))
        
        # Título
        draw_text(self.screen, "MODO HISTÓRIA", WINDOW_WIDTH // 2, 50,
                 size=48, color=COLORS['WHITE'], center=True)
        
        # Informações do jogador
        draw_text(self.screen, f"Jogador: {self.username}", 50, 100,
                 size=24, color=COLORS['WHITE'])
        draw_text(self.screen, f"XP Total: {self.progress['total_xp']}", 50, 130,
                 size=20, color=COLORS['YELLOW'])
        
        # Capítulos
        self.chapter_rects = []
        x_start = 100
        y_start = 200
        chapter_width = 250
        chapter_height = 150
        spacing = 30
        
        for i, chapter in enumerate(self.chapters):
            x = x_start + (i % 3) * (chapter_width + spacing)
            y = y_start + (i // 3) * (chapter_height + spacing)
            
            # Verifica se está desbloqueado
            locked = i > 0 and not self.chapters[i-1].completed
            
            # Cor do capítulo
            if chapter.completed:
                color = (50, 150, 50)  # Verde
                border_color = (100, 255, 100)
            elif locked:
                color = (50, 50, 50)  # Cinza
                border_color = (100, 100, 100)
            else:
                color = (50, 50, 150)  # Azul
                border_color = (100, 100, 255)
            
            # Desenha capítulo
            rect = pygame.Rect(x, y, chapter_width, chapter_height)
            self.chapter_rects.append((x, y, chapter_width, chapter_height))
            
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, border_color, rect, 3)
            
            # Título do capítulo
            draw_text(self.screen, f"Capítulo {chapter.id}", x + chapter_width // 2, y + 20,
                     size=24, color=COLORS['WHITE'], center=True)
            
            # Nome do capítulo
            draw_text(self.screen, chapter.title, x + chapter_width // 2, y + 50,
                     size=20, color=COLORS['WHITE'], center=True)
            
            # Status
            if chapter.completed:
                draw_text(self.screen, "COMPLETO", x + chapter_width // 2, y + 80,
                         size=18, color=(100, 255, 100), center=True)
                
                # Tentativas
                draw_text(self.screen, f"Tentativas: {chapter.attempts}", 
                         x + chapter_width // 2, y + 100,
                         size=16, color=COLORS['WHITE'], center=True)
            elif locked:
                draw_text(self.screen, "BLOQUEADO", x + chapter_width // 2, y + 80,
                         size=18, color=(200, 200, 200), center=True)
            else:
                draw_text(self.screen, "DISPONÍVEL", x + chapter_width // 2, y + 80,
                         size=18, color=COLORS['YELLOW'], center=True)
        
        # Instruções
        draw_text(self.screen, "Clique em um capítulo para jogar | ESC para voltar",
                 WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50,
                 size=20, color=COLORS['WHITE'], center=True)
    
    def draw_intro(self):
        """Desenha a introdução do capítulo"""
        self.screen.blit(self.background, (0, 0))
        
        # Título do capítulo
        draw_text(self.screen, f"Capítulo {self.current_chapter.id}: {self.current_chapter.title}",
                 WINDOW_WIDTH // 2, 100,
                 size=36, color=COLORS['WHITE'], center=True)
        
        # Descrição
        draw_text(self.screen, self.current_chapter.description,
                 WINDOW_WIDTH // 2, 160,
                 size=24, color=COLORS['WHITE'], center=True)
        
        # Objetivos
        draw_text(self.screen, "Objetivos:", WINDOW_WIDTH // 2 - 200, 220,
                 size=28, color=COLORS['YELLOW'])
        
        y_offset = 260
        for objective in self.current_chapter.objectives:
            draw_text(self.screen, f"• {objective}", WINDOW_WIDTH // 2 - 180, y_offset,
                     size=22, color=COLORS['WHITE'])
            y_offset += 30
        
        # Diálogo
        if self.dialogue_index < len(self.current_chapter.dialogue):
            dialogue = self.current_chapter.dialogue[self.dialogue_index]
            
            # Caixa de diálogo
            dialogue_rect = pygame.Rect(100, WINDOW_HEIGHT - 200, WINDOW_WIDTH - 200, 150)
            pygame.draw.rect(self.screen, (30, 30, 50), dialogue_rect)
            pygame.draw.rect(self.screen, COLORS['WHITE'], dialogue_rect, 3)
            
            # Speaker
            draw_text(self.screen, dialogue['speaker'] + ":", 120, WINDOW_HEIGHT - 180,
                     size=24, color=COLORS['YELLOW'])
            
            # Texto
            draw_text(self.screen, dialogue['text'], 120, WINDOW_HEIGHT - 140,
                     size=22, color=COLORS['WHITE'])
            
            # Indicador de continuação
            if int(self.dialogue_timer * 2) % 2 == 0:
                draw_text(self.screen, "▼", WINDOW_WIDTH - 150, WINDOW_HEIGHT - 70,
                         size=24, color=COLORS['WHITE'])
        
        # Instruções
        draw_text(self.screen, "Pressione qualquer tecla para continuar",
                 WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30,
                 size=18, color=COLORS['WHITE'], center=True)
    
    def draw_victory(self):
        """Desenha a tela de vitória"""
        self.screen.blit(self.background, (0, 0))
        
        # Mensagem de vitória
        draw_text(self.screen, "VITÓRIA!", WINDOW_WIDTH // 2, 150,
                 size=72, color=COLORS['YELLOW'], center=True)
        
        draw_text(self.screen, f"Capítulo {self.current_chapter.id} Completo!",
                 WINDOW_WIDTH // 2, 230,
                 size=36, color=COLORS['WHITE'], center=True)
        
        # Recompensas
        if self.current_chapter.rewards:
            draw_text(self.screen, "Recompensas:", WINDOW_WIDTH // 2, 300,
                     size=28, color=COLORS['GREEN'], center=True)
            
            y_offset = 340
            for reward_type, reward_value in self.current_chapter.rewards.items():
                if reward_type == 'xp':
                    text = f"+{reward_value} XP"
                elif reward_type == 'title':
                    text = f'Novo Título: "{reward_value}"'
                else:
                    text = f"{reward_type}: {reward_value}"
                
                draw_text(self.screen, text, WINDOW_WIDTH // 2, y_offset,
                         size=24, color=COLORS['WHITE'], center=True)
                y_offset += 40
        
        # Estatísticas
        if self.current_game:
            stats = self.current_game.players[0].get_stats()
            draw_text(self.screen, f"Peixes coletados: {stats['fish_collected']}",
                     WINDOW_WIDTH // 2, 450,
                     size=22, color=COLORS['WHITE'], center=True)
            draw_text(self.screen, f"Turnos: {stats['turns_played']}",
                     WINDOW_WIDTH // 2, 480,
                     size=22, color=COLORS['WHITE'], center=True)
        
        # Instruções
        draw_text(self.screen, "Pressione qualquer tecla para continuar",
                 WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50,
                 size=20, color=COLORS['WHITE'], center=True)
    
    def draw_defeat(self):
        """Desenha a tela de derrota"""
        self.screen.blit(self.background, (0, 0))
        
        # Mensagem de derrota
        draw_text(self.screen, "DERROTA", WINDOW_WIDTH // 2, 200,
                 size=72, color=COLORS['RED'], center=True)
        
        draw_text(self.screen, "Não desista! Tente novamente!",
                 WINDOW_WIDTH // 2, 300,
                 size=32, color=COLORS['WHITE'], center=True)
        
        # Dicas
        tips = [
            "Use as correntes a seu favor",
            "Observe os movimentos dos oponentes",
            "Planeje seus movimentos com antecedência",
            "Colete peixes próximos primeiro"
        ]
        
        import random
        tip = random.choice(tips)
        
        draw_text(self.screen, f"Dica: {tip}",
                 WINDOW_WIDTH // 2, 400,
                 size=24, color=COLORS['YELLOW'], center=True)
        
        # Estatísticas
        if self.current_game:
            stats = self.current_game.players[0].get_stats()
            draw_text(self.screen, f"Você coletou {stats['fish_collected']} peixes",
                     WINDOW_WIDTH // 2, 480,
                     size=22, color=COLORS['WHITE'], center=True)
        
        # Instruções
        draw_text(self.screen, "Pressione qualquer tecla para continuar",
                 WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50,
                 size=20, color=COLORS['WHITE'], center=True)


class StoryGame(Game):
    """Versão modificada do jogo para o modo história"""
    
    def __init__(self, screen, username, num_players, ai_difficulty, chapter):
        super().__init__(screen, username, num_players, ai_difficulty)
        self.chapter = chapter
        
        # Aplica regras especiais
        self.apply_special_rules()
        
        # Modifica condições de vitória
        if 'fish_required' in chapter.win_conditions:
            global WINNING_FISH_COUNT
            self.original_winning_count = WINNING_FISH_COUNT
            WINNING_FISH_COUNT = chapter.win_conditions['fish_required']
    
    def apply_special_rules(self):
        """Aplica regras especiais do capítulo"""
        if 'stronger_currents' in self.chapter.special_rules:
            # Dobra o efeito das cartas
            for player in self.players:
                # Isso seria implementado modificando as cartas
                pass
    
    def __del__(self):
        """Restaura configurações originais"""
        if hasattr(self, 'original_winning_count'):
            global WINNING_FISH_COUNT
            WINNING_FISH_COUNT = self.original_winning_count