from Player import Player
from IA import Ia
from Game import Game
import json

class Menu:
    separation_line = ("==============================================")

    def __init__(self, save_file="save.json", game=None):
        self.save_file = save_file
        self.game = game
        self.board_size = 12

    def setup_menu(self):
        menu = 1
        print("############################################## \n"
              "#           QUORIDOR BY PETRALE LUCA         # \n"
              "#                 FINAL VERSION              # \n"
              "##############################################")        
        while menu:
            print("1. Launch the game")
            print("2. Resume the game")
            print("3. Change the number of square")
            print("4. Leave the game")
            print(self.separation_line)
            self.board_size = 12 #Reinitialise si le joueur lance plusieurs jeux à la fois et qu'il change de cases
            player_input = input("What is your choice (1-4) : ")

            if player_input == "1":
                self.setup_game()
                self.game.play()

            elif player_input == "2":
                self.display_save()
                self.game.play()

            elif player_input == "3":
                self.change_board_size()
                self.setup_game()
                self.game.play()

            elif player_input == "4":
                print(self.separation_line)
                print("--------------- SEE YOU SOON ! ---------------")
                print(self.separation_line)
                menu = 0

    def add_player(self):
        while 1:
            try:
                print(self.separation_line)
                choose_nb_player = input("Choose the number of players (1-2) : ")
                assert choose_nb_player in ["1","2"]
                nb_player = int(choose_nb_player)
                return nb_player
            except AssertionError:
                print("Enter a valid number !")

    def player_username(self):
        while 1 :
            player_username = input("What's your name : ")
            if len(player_username) != 0 :
                return player_username

    def change_board_size(self):
        while 1:
            try:
                choose_board_size = input("How many squares do you want for the game (10/12/14) : ")
                assert choose_board_size in ["10","12","14"]
                self.board_size = int(choose_board_size)+2
                return self.board_size
            except AssertionError:
                print("Enter a valid number !")

    def setup_game(self):
        nb_player = self.add_player()
        player = self.player_username()
        position=(1, (self.board_size//2))
        player = Player(player, position, menu)
        enemy_position = (self.board_size-2,self.board_size//2)

        if nb_player == 1:
            enemy = Ia("IA", enemy_position)

        else:
            enemy = self.player_username()
            enemy = Player(enemy, enemy_position, menu)

        game = Game(player, enemy, self.board_size, nb_player)
        game.add_barrier()
        self.game = game

    def display_save(self):
        try:
            with open(self.save_file, "r") as save:
                file = json.load(save)

                player_name = file[0]
                player_position_tmp = file[1]
                player_position_line = player_position_tmp[0]
                player_position_col = player_position_tmp[1]
                player_position = (player_position_line,player_position_col)

                enemy_name = file[2]
                enemy_position_tmp = file[3]
                enemy_position_line = enemy_position_tmp[0]
                enemy_position_col = enemy_position_tmp[1]
                enemy_position = (enemy_position_line, enemy_position_col)

                walls = []
                for wall_line, wall_col in file[4]:
                    walls.append((wall_line,wall_col))

                player_remaining_try = file[5]
                enemy_remaining_try = file[6]

                board_size = file[7]

                nb_player = file[8]
                player = Player(player_name, player_position, menu, player_remaining_try)
                if nb_player == 1 :
                    enemy = Ia(enemy_name, enemy_position, enemy_remaining_try)
                else:
                    enemy = Player(enemy_name, enemy_position, menu, enemy_remaining_try)

                game = Game(player, enemy, board_size, nb_player, walls)
                game.add_barrier()
                self.game = game

        except FileNotFoundError:
            print("No backup file exists !")
            self.setup_menu()

if __name__ == "__main__" :
    menu =  Menu()
    menu.setup_menu()
