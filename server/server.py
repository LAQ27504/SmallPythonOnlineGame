import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socket
import threading
# filepath: /home/laq275/LAQ/Classes/SmallPythonOnlineGame/character/Warrior.py
# filepath: /home/laq275/LAQ/Classes/SmallPythonOnlineGame/character/basecharacter.py
from character.basecharacter import BaseCharacter
from character.Warrior import Warrior
from character.Assasin import Assasin


class Player:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.name = None
        self.character = None
        self.ready = False
        self.action = None
        self.target = None

class GameServer:
    def __init__(self, host='192.168.1.8', port=8000):
        self.host = host
        self.port = port
        self.players = []
        self.lock = threading.Lock()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            conn, addr = server_socket.accept()
            player = Player(conn, addr)
            threading.Thread(target=self.handle_client, args=(player,)).start()

    def handle_client(self, player):
        player.conn.sendall(b"Enter your name: ")
        player.name = player.conn.recv(1024).decode().strip()
        with self.lock:
            self.players.append(player)
            print(f"{player.name} has joined the game.")
            if len(self.players) == 3:
                self.start_game()

    def start_game(self):
        threads = []
        for player in self.players:
            thread = threading.Thread(target=self.choose_character, args=(player,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.play_game()


    def choose_character(self, player):
        text = f"Players: {[p.name for p in self.players]}\n".encode()
        player.conn.sendall(text)
        choice1 = player.conn.recv(1024)
        if choice1:
            choice1 = choice1.decode().strip()
        print(player.name, choice1)
        player.conn.sendall(b"Choose your character (1: BaseCharacter, 2: Warrior, 3: Assasin): ")
        choice = player.conn.recv(1024).decode().strip()
        print(player.name, choice)
        if choice == '1':
            player.character = BaseCharacter(player.name)
        elif choice == '2':
            player.character = Warrior(player.name)
        elif choice == '3':
            player.character = Assasin(player.name)
        player.ready = True

    def play_game(self):
        while len([p for p in self.players if p.character.health > 0]) > 1:
            threads = []
            for player in self.players:
                if player.character.health > 0:
                    thread = threading.Thread(target=self.take_turn, args=(player,))
                    threads.append(thread)
                    thread.start()
                else: 
                    player.conn.sendall(b"You are dead. You will spectate the game.\n")
            for thread in threads:
                thread.join()

            self.calculate_damage()
            for player in self.players:
                if player.character.health > 0:
                    thread = threading.Thread(target=self.show_status, args=(player,))
                    threads.append(thread)
                    thread.start()
                else: 
                    player.conn.sendall(b"You are dead. You will spectate the game.\n")
            for thread in threads:
                thread.join()

        self.declare_winner()

    def take_turn(self, player):
        player.character.change_mana(5)
        player.conn.sendall(b"Choose your action (1: Attack, 2: Parry): ")
        action = player.conn.recv(1024).decode().strip()
        player.conn.sendall(b"Choose your target (Enter player name): ")
        target_name = player.conn.recv(1024).decode().strip()
        if not target_name:
            target = None
        else:
            target = next((p for p in self.players if p.name == target_name), None)
        print(player.name, action, target)
        player.action = action
        player.target = target
        if player.action == '2':
            player.character.change_parry(True) 
    def calculate_damage(self):
        for player in self.players:
            if player.action == '1' and player.target:
                player.character.attack(player.target.character)
        for player in self.players:
            if player.action == '2':
                player.character.parry()
             # Simplified for example
        

    def show_status(self, player):
        status = "\n".join([f"{p.name}: Health={p.character.health}, Mana={p.character.mana}" for p in self.players])
        actions = "\n".join([f"{p.name} chose action {p.action} targeting {p.target.name if p.target else 'None'}" for p in self.players])
        player.conn.sendall(f"Actions:\n{actions}\n\nStatus:\n{status}\n".encode())
        a = player.conn.recv(1024).decode().strip()
    def declare_winner(self):
        winner = next((p for p in self.players if p.character.health > 0), None)
        if winner:
            for player in self.players:
                if player == winner:
                    player.conn.sendall(b"You are the last player standing. You win!\n")
                else:
                    player.conn.sendall(f"The game is over. The winner is {winner.name}.\n".encode())
        self.reset_game()

    def reset_game(self):
        for player in self.players:
            player.conn.close()
        self.players = []

if __name__ == "__main__":
    server = GameServer()
    server.start_server()