# src/login.py - Sistema de login

import pygame
import os
import bcrypt
import random
import math
from config import *
from src.utils import draw_text, draw_button, load_json, save_json, create_gradient_surface

class LoginScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Campos de entrada
        self.username = ""
        self.password = ""
        self.active_field = "username"  # username ou password
        
        # Estado
        self.mode = "login"  # login ou register
        self.message = ""
        self.message_color = COLORS['WHITE']
        self.message_timer = 0
        
        # Arquivo de usuários
        self.users_file = os.path.join(DATA_PATH, 'users.json')
        self.users = load_json(self.users_file)
        
        # Visual
        self.box_width = 400
        self.box_height = 350
        self.box_x = (WINDOW_WIDTH - self.box_width) // 2
        self.box_y = (WINDOW_HEIGHT - self.box_height) // 2
        
        # Efeitos visuais
        self.wave_offset = 0
        self.bubble_particles = []
        self.create_bubbles()
        
    def create_bubbles(self):
        """Cria partículas de bolhas para o fundo"""
        for _ in range(20):
            self.bubble_particles.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(0, WINDOW_HEIGHT),
                'size': random.randint(5, 15),
                'speed': random.uniform(0.5, 2.0),
                'wobble': random.uniform(0, math.pi * 2)
            })
    
    def update_bubbles(self, dt):
        """Atualiza as bolhas do fundo"""
        for bubble in self.bubble_particles:
            bubble['y'] -= bubble['speed']
            bubble['wobble'] += dt * 2
            bubble['x'] += math.sin(bubble['wobble']) * 0.5
            
            # Reposiciona bolhas que saíram da tela
            if bubble['y'] < -bubble['size']:
                bubble['y'] = WINDOW_HEIGHT + bubble['size']
                bubble['x'] = random.randint(0, WINDOW_WIDTH)
    
    def handle_event(self, event):
        """Processa eventos"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                # Alterna entre campos
                self.active_field = "password" if self.active_field == "username" else "username"
            
            elif event.key == pygame.K_RETURN:
                # Tenta fazer login/registro
                if self.mode == "login":
                    return self.login()
                else:
                    self.register()
            
            elif event.key == pygame.K_BACKSPACE:
                # Remove último caractere
                if self.active_field == "username":
                    self.username = self.username[:-1]
                else:
                    self.password = self.password[:-1]
            
            else:
                # Adiciona caractere
                if event.unicode.isprintable():
                    if self.active_field == "username" and len(self.username) < 20:
                        self.username += event.unicode
                    elif self.active_field == "password" and len(self.password) < 30:
                        self.password += event.unicode
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                mouse_pos = event.pos
                
                # Verifica clique nos campos
                username_rect = pygame.Rect(self.box_x + 50, self.box_y + 100, 300, 40)
                password_rect = pygame.Rect(self.box_x + 50, self.box_y + 160, 300, 40)
                
                if username_rect.collidepoint(mouse_pos):
                    self.active_field = "username"
                elif password_rect.collidepoint(mouse_pos):
                    self.active_field = "password"
        
        return None
    
    def login(self):
        """Tenta fazer login"""
        if not self.username or not self.password:
            self.show_message("Preencha todos os campos!", COLORS['RED'])
            return None
        
        if self.username in self.users:
            stored_password = self.users[self.username]['password'].encode('utf-8')
            if bcrypt.checkpw(self.password.encode('utf-8'), stored_password):
                self.show_message("Login realizado com sucesso!", COLORS['GREEN'])
                return self.username
            else:
                self.show_message("Senha incorreta!", COLORS['RED'])
        else:
            self.show_message("Usuário não encontrado!", COLORS['RED'])
        
        return None
    
    def register(self):
        """Registra um novo usuário"""
        if not self.username or not self.password:
            self.show_message("Preencha todos os campos!", COLORS['RED'])
            return
        
        if len(self.username) < 3:
            self.show_message("Usuário deve ter pelo menos 3 caracteres!", COLORS['RED'])
            return
        
        if len(self.password) < 6:
            self.show_message("Senha deve ter pelo menos 6 caracteres!", COLORS['RED'])
            return
        
        if self.username in self.users:
            self.show_message("Usuário já existe!", COLORS['RED'])
            return
        
        # Cria hash da senha
        hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        
        # Salva o usuário
        self.users[self.username] = {
            'password': hashed.decode('utf-8'),
            'created_at': pygame.time.get_ticks(),
            'achievements': [],
            'stats': {
                'games_played': 0,
                'games_won': 0,
                'fish_collected': 0,
                'time_played': 0
            }
        }
        
        save_json(self.users_file, self.users)
        self.show_message("Usuário criado com sucesso!", COLORS['GREEN'])
        self.mode = "login"
    
    def show_message(self, message, color):
        """Mostra uma mensagem temporária"""
        self.message = message
        self.message_color = color
        self.message_timer = 3.0  # 3 segundos
    
    def update(self, dt):
        """Atualiza a tela de login"""
        # Atualiza timer da mensagem
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""
        
        # Atualiza efeitos visuais
        self.wave_offset += dt * 50
        self.update_bubbles(dt)
    
    def draw(self):
        """Desenha a tela de login"""
        # Fundo com gradiente
        gradient = create_gradient_surface(WINDOW_WIDTH, WINDOW_HEIGHT, 
                                         (20, 60, 100), (40, 120, 180))
        self.screen.blit(gradient, (0, 0))
        
        # Desenha bolhas
        for bubble in self.bubble_particles:
            color = (*COLORS['WHITE'], 50)  # Transparente
            pygame.draw.circle(self.screen, color[:3], 
                             (int(bubble['x']), int(bubble['y'])), 
                             bubble['size'])
            pygame.draw.circle(self.screen, COLORS['WHITE'], 
                             (int(bubble['x']), int(bubble['y'])), 
                             bubble['size'], 1)
        
        # Caixa de login
        box_surface = pygame.Surface((self.box_width, self.box_height))
        box_surface.set_alpha(230)
        box_surface.fill((30, 30, 50))
        self.screen.blit(box_surface, (self.box_x, self.box_y))
        
        # Borda da caixa
        pygame.draw.rect(self.screen, COLORS['WHITE'], 
                        (self.box_x, self.box_y, self.box_width, self.box_height), 3)
        
        # Título
        title = "CAÇADOR DOS MARES"
        draw_text(self.screen, title, WINDOW_WIDTH // 2, self.box_y - 50,
                 size=48, color=COLORS['WHITE'], center=True)
        
        # Subtítulo
        subtitle = "Login" if self.mode == "login" else "Criar Conta"
        draw_text(self.screen, subtitle, self.box_x + self.box_width // 2, self.box_y + 40,
                 size=32, color=COLORS['WHITE'], center=True)
        
        # Campo de usuário
        username_color = COLORS['YELLOW'] if self.active_field == "username" else COLORS['WHITE']
        draw_text(self.screen, "Usuário:", self.box_x + 50, self.box_y + 80,
                 size=20, color=username_color)
        
        username_rect = pygame.Rect(self.box_x + 50, self.box_y + 100, 300, 40)
        pygame.draw.rect(self.screen, COLORS['WHITE'], username_rect, 2)
        draw_text(self.screen, self.username, username_rect.x + 10, username_rect.y + 10,
                 size=24)
        
        # Campo de senha
        password_color = COLORS['YELLOW'] if self.active_field == "password" else COLORS['WHITE']
        draw_text(self.screen, "Senha:", self.box_x + 50, self.box_y + 140,
                 size=20, color=password_color)
        
        password_rect = pygame.Rect(self.box_x + 50, self.box_y + 160, 300, 40)
        pygame.draw.rect(self.screen, COLORS['WHITE'], password_rect, 2)
        password_display = "*" * len(self.password)
        draw_text(self.screen, password_display, password_rect.x + 10, password_rect.y + 10,
                 size=24)
        
        # Botões
        button_y = self.box_y + 220
        if self.mode == "login":
            if draw_button(self.screen, "Entrar", self.box_x + 50, button_y,
                          140, 40, (0, 150, 0), (0, 200, 0)):
                return self.login()
            
            if draw_button(self.screen, "Criar Conta", self.box_x + 210, button_y,
                          140, 40, (0, 100, 150), (0, 130, 200)):
                self.mode = "register"
                self.message = ""
        else:
            if draw_button(self.screen, "Registrar", self.box_x + 50, button_y,
                          140, 40, (0, 150, 0), (0, 200, 0)):
                self.register()
            
            if draw_button(self.screen, "Voltar", self.box_x + 210, button_y,
                          140, 40, (150, 0, 0), (200, 0, 0)):
                self.mode = "login"
                self.message = ""
        
        # Mensagem
        if self.message:
            draw_text(self.screen, self.message, 
                     self.box_x + self.box_width // 2, self.box_y + 280,
                     size=20, color=self.message_color, center=True)
        
        # Instruções
        instructions = "TAB para alternar campos | ENTER para confirmar"
        draw_text(self.screen, instructions, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30,
                 size=16, color=COLORS['WHITE'], center=True)