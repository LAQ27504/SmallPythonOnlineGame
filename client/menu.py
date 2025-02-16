import os 
import time

class Menu():
    def __init__(self):
        pass
    def clear_terminal(self):
    # Check the operating system
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # macOS/Linux/Unix
            os.system('clear')
    def start_menu(self):
        self.clear_terminal()
        print("-------------------------")
        print("Start the game [Enter]")
        input()
        print("Enter the connection:")
        connection = input()
        connection = connection.split("/")
        name = input("Enter your name: ")
        return (connection, name)
    
    def start_menu_restart(self):
        self.clear_terminal()
        print("-------------------------")
        print("Start the game [Enter]")
        print()
        print("Re-enter the connection:")
        connection = input()
        connection = connection.split("/")
        name = input("Enter your name: ")
        return (connection, name)

    def wait_menu(self, player_list : list):
        self.clear_terminal()
        print("-------------------------")
        print("Waiting room")
        if len(player_list) > 0:
            for player in player_list:
                print(f"Player {player} has joined")
        pass
    