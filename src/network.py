# src/network.py - Sistema de multiplayer em rede

import socket
import threading
import pickle
import time
from config import *
from src.game import Game
from src.utils import draw_text

class GameServer:
    """Servidor do jogo multiplayer"""
    
    def __init__(self, port, room_name):
        self.port = port
        self.room_name = room_name
        self.socket = None
        self.clients = []
        self.game_state = None
        self.running = False
        self.thread = None
        
        # Informações dos jogadores
        self.players_info = {}
        self.ready_players = set()
        
    def start(self):
        """Inicia o servidor"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.socket.bind(('', self.port))
            self.socket.listen(4)
            self.running = True
            
            # Thread para aceitar conexões
            self.thread = threading.Thread(target=self.accept_clients)
            self.thread.daemon = True
            self.thread.start()
            
            print(f"Servidor iniciado na porta {self.port}")
            return True
            
        except Exception as e:
            print(f"Erro ao iniciar servidor: {e}")
            return False
    
    def accept_clients(self):
        """Aceita novas conexões"""
        while self.running:
            try:
                client_socket, address = self.socket.accept()
                
                # Thread para lidar com o cliente
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except:
                break
    
    def handle_client(self, client_socket, address):
        """Lida com um cliente conectado"""
        client_id = len(self.clients)
        self.clients.append({
            'socket': client_socket,
            'address': address,
            'id': client_id,
            'username': None
        })
        
        print(f"Cliente conectado: {address}")
        
        while self.running:
            try:
                # Recebe dados do cliente
                data = client_socket.recv(4096)
                if not data:
                    break
                
                # Processa mensagem
                message = pickle.loads(data)
                self.process_message(client_id, message)
                
            except Exception as e:
                print(f"Erro com cliente {address}: {e}")
                break
        
        # Remove cliente desconectado
        self.disconnect_client(client_id)
    
    def process_message(self, client_id, message):
        """Processa mensagem recebida"""
        msg_type = message.get('type')
        
        if msg_type == 'join':
            # Jogador entrando na sala
            username = message.get('username')
            self.players_info[client_id] = {
                'username': username,
                'ready': False
            }
            
            # Envia informações da sala
            self.send_to_client(client_id, {
                'type': 'room_info',
                'room_name': self.room_name,
                'players': self.get_players_list()
            })
            
            # Notifica outros jogadores
            self.broadcast({
                'type': 'player_joined',
                'player_id': client_id,
                'username': username
            }, exclude=client_id)
            
        elif msg_type == 'ready':
            # Jogador pronto
            self.ready_players.add(client_id)
            self.players_info[client_id]['ready'] = True
            
            self.broadcast({
                'type': 'player_ready',
                'player_id': client_id
            })
            
            # Verifica se todos estão prontos
            if len(self.ready_players) == len(self.clients) and len(self.clients) >= MIN_PLAYERS:
                self.start_game()
                
        elif msg_type == 'game_action':
            # Ação do jogo
            if self.game_state:
                self.broadcast({
                    'type': 'game_update',
                    'action': message.get('action'),
                    'player_id': client_id,
                    'data': message.get('data')
                })
    
    def get_players_list(self):
        """Retorna lista de jogadores"""
        players = []
        for client_id, info in self.players_info.items():
            players.append({
                'id': client_id,
                'username': info['username'],
                'ready': info['ready']
            })
        return players
    
    def start_game(self):
        """Inicia o jogo"""
        self.game_state = {
            'started': True,
            'players': self.get_players_list(),
            'seed': int(time.time())  # Para sincronizar random
        }
        
        self.broadcast({
            'type': 'game_start',
            'game_state': self.game_state
        })
    
    def send_to_client(self, client_id, message):
        """Envia mensagem para um cliente específico"""
        try:
            client = next(c for c in self.clients if c['id'] == client_id)
            data = pickle.dumps(message)
            client['socket'].send(data)
        except:
            pass
    
    def broadcast(self, message, exclude=None):
        """Envia mensagem para todos os clientes"""
        for client in self.clients:
            if exclude is None or client['id'] != exclude:
                try:
                    data = pickle.dumps(message)
                    client['socket'].send(data)
                except:
                    pass
    
    def disconnect_client(self, client_id):
        """Desconecta um cliente"""
        # Remove das listas
        self.clients = [c for c in self.clients if c['id'] != client_id]
        self.ready_players.discard(client_id)
        
        if client_id in self.players_info:
            username = self.players_info[client_id]['username']
            del self.players_info[client_id]
            
            # Notifica outros
            self.broadcast({
                'type': 'player_left',
                'player_id': client_id,
                'username': username
            })
    
    def stop(self):
        """Para o servidor"""
        self.running = False
        if self.socket:
            self.socket.close()
        
        # Desconecta todos os clientes
        for client in self.clients:
            try:
                client['socket'].close()
            except:
                pass


class NetworkGame(Game):
    """Versão em rede do jogo"""
    
    def __init__(self, screen, username, server_ip, port, is_host=False):
        self.screen = screen
        self.username = username
        self.server_ip = server_ip
        self.port = port
        self.is_host = is_host
        
        # Conexão
        self.socket = None
        self.connected = False
        self.receive_thread = None
        
        # Estado do jogo
        self.local_player_id = None
        self.players_info = {}
        self.game_started = False
        
        # Fila de mensagens
        self.message_queue = []
        self.message_lock = threading.Lock()
        
        # Conecta ao servidor
        self.connect()
        
    def connect(self):
        """Conecta ao servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.port))
            self.connected = True
            
            # Thread para receber mensagens
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            # Envia informações de entrada
            self.send_message({
                'type': 'join',
                'username': self.username
            })
            
            print(f"Conectado ao servidor {self.server_ip}:{self.port}")
            return True
            
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return False
    
    def receive_messages(self):
        """Recebe mensagens do servidor"""
        while self.connected:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                
                message = pickle.loads(data)
                
                with self.message_lock:
                    self.message_queue.append(message)
                    
            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")
                break
        
        self.connected = False
    
    def send_message(self, message):
        """Envia mensagem ao servidor"""
        if self.connected:
            try:
                data = pickle.dumps(message)
                self.socket.send(data)
            except:
                self.connected = False
    
    def process_server_messages(self):
        """Processa mensagens recebidas do servidor"""
        with self.message_lock:
            messages = self.message_queue[:]
            self.message_queue.clear()
        
        for message in messages:
            msg_type = message.get('type')
            
            if msg_type == 'room_info':
                # Informações da sala
                self.process_room_info(message)
                
            elif msg_type == 'player_joined':
                # Novo jogador
                player_id = message.get('player_id')
                username = message.get('username')
                self.players_info[player_id] = {
                    'username': username,
                    'ready': False
                }
                
            elif msg_type == 'player_ready':
                # Jogador pronto
                player_id = message.get('player_id')
                if player_id in self.players_info:
                    self.players_info[player_id]['ready'] = True
                    
            elif msg_type == 'player_left':
                # Jogador saiu
                player_id = message.get('player_id')
                if player_id in self.players_info:
                    del self.players_info[player_id]
                    
            elif msg_type == 'game_start':
                # Jogo iniciado
                self.start_network_game(message.get('game_state'))
                
            elif msg_type == 'game_update':
                # Atualização do jogo
                self.process_game_update(message)
    
    def process_room_info(self, message):
        """Processa informações da sala"""
        players = message.get('players', [])
        
        # Identifica o ID local do jogador
        for player in players:
            if player['username'] == self.username:
                self.local_player_id = player['id']
            
            self.players_info[player['id']] = {
                'username': player['username'],
                'ready': player['ready']
            }
    
    def start_network_game(self, game_state):
        """Inicia o jogo em rede"""
        # Define seed para sincronizar random
        import random
        random.seed(game_state['seed'])
        
        # Cria jogadores
        players = game_state['players']
        super().__init__(self.screen, self.username, len(players))
        
        # Substitui jogadores pelos jogadores reais
        self.players = []
        for i, player_info in enumerate(players):
            from src.player import Player
            
            is_local = player_info['id'] == self.local_player_id
            player = Player(
                i,
                player_info['username'],
                COLORS['PLAYER_COLORS'][i],
                is_ai=False
            )
            
            # Marca jogador local
            player.is_local = is_local
            self.players.append(player)
        
        self.game_started = True
    
    def process_game_update(self, message):
        """Processa atualização do jogo"""
        if not self.game_started:
            return
            
        action = message.get('action')
        player_id = message.get('player_id')
        data = message.get('data')
        
        # Ignora ações próprias (já processadas localmente)
        if player_id == self.local_player_id:
            return
        
        # Processa ação
        if action == 'place_boat':
            player = self.players[player_id]
            self.place_player_boat(player, data['x'], data['y'])
            
        elif action == 'play_card':
            player = self.players[player_id]
            card_index = data['card_index']
            if 0 <= card_index < len(player.hand.cards):
                card = player.hand.cards[card_index]
                self.play_card(player, card)
                
        elif action == 'move_boat':
            player = self.players[player_id]
            self.move_player_boat(player, data['x'], data['y'])
    
    def handle_event(self, event):
        """Processa eventos (override)"""
        # Processa mensagens do servidor primeiro
        self.process_server_messages()
        
        if not self.game_started:
            # Tela de espera
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.disconnect()
                    return 'quit'
                elif event.key == pygame.K_RETURN:
                    # Marca como pronto
                    self.send_message({'type': 'ready'})
            return None
        
        # Processa eventos do jogo
        result = super().handle_event(event)
        
        # Envia ações para o servidor
        current_player = self.players[self.current_player_index]
        if hasattr(current_player, 'is_local') and current_player.is_local:
            # Detecta e envia ações
            # (Isso seria implementado detectando mudanças no estado do jogo)
            pass
        
        return result
    
    def update(self, dt):
        """Atualiza o jogo (override)"""
        if self.game_started:
            super().update(dt)
    
    def draw(self):
        """Desenha o jogo (override)"""
        if not self.game_started:
            # Tela de espera
            self.screen.fill(COLORS['BACKGROUND'])
            
            # Título
            draw_text(self.screen, "SALA DE ESPERA", WINDOW_WIDTH // 2, 100,
                     size=48, color=COLORS['WHITE'], center=True)
            
            # Jogadores
            y_offset = 200
            draw_text(self.screen, "Jogadores:", WINDOW_WIDTH // 2 - 200, y_offset,
                     size=32, color=COLORS['WHITE'])
            
            y_offset += 50
            for player_id, info in self.players_info.items():
                color = COLORS['GREEN'] if info['ready'] else COLORS['WHITE']
                status = " (Pronto)" if info['ready'] else ""
                
                text = f"{info['username']}{status}"
                if player_id == self.local_player_id:
                    text += " (Você)"
                
                draw_text(self.screen, text, WINDOW_WIDTH // 2 - 180, y_offset,
                         size=24, color=color)
                y_offset += 40
            
            # Instruções
            if self.local_player_id in self.players_info:
                if not self.players_info[self.local_player_id]['ready']:
                    draw_text(self.screen, "Pressione ENTER quando estiver pronto",
                             WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100,
                             size=24, color=COLORS['YELLOW'], center=True)
            
            draw_text(self.screen, "ESC para sair", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50,
                     size=20, color=COLORS['WHITE'], center=True)
        else:
            super().draw()
    
    def disconnect(self):
        """Desconecta do servidor"""
        self.connected = False
        if self.socket:
            self.socket.close()