from Barrier import Barrier
import json
import random

class Game:
    separation_line = ("----------------------------------------------")
    
    def __init__(self, player, enemy, board_size, nb_player, walls=None, config="IA_config.json", nb_game="game.json") :
        self.player = player
        self.enemy = enemy
        self.board_size = board_size
        self.nb_player = nb_player
        self.config = config
        self.nb_game = nb_game
        self.walls = walls or []
        self.IA_config = []
        self.file_game = []
        self.positions_barriers = []
        self.barriers = []
        self.key_save = [0]

    def __str__(self):
        return "Good luck " + self.player.name + " & " + self.enemy.name + "!"

    def draw(self):
        for line in range(self.board_size):
            for col in range(self.board_size):
                if (line,col) == self.player.position:
                    print(self.player.name[0].upper(),end=" ")
                elif (line,col) == self.enemy.position:
                    print(self.enemy.name[0].upper(),end=" ")
                elif (line,col) in self.barriers:
                    print(Barrier.icon,end=" ")
                elif (line,col) in self.walls:
                    print(Barrier.icon,end=" ")
                else :
                    print(".",end=" ")
            print()
        print(self.separation_line)

    def add_barrier(self):
        for line in range(self.board_size):
            self.barrier((line, 0))
            self.barrier((line, self.board_size-1))
        for col in range(0,self.board_size):
            self.barrier((0, col))
            self.barrier((self.board_size-1, col))

        for barrier in self.positions_barriers:
            self.barriers.append(barrier.position)

    def barrier(self, position):
        new_barrier = Barrier(position)
        self.positions_barriers.append(new_barrier)

    def is_barried(self, position):
        return position in self.barriers

    def add_wall(self, pos):
        while pos in self.walls or pos==self.player.position or pos==self.enemy.position :
            print("/!\ Location already occupied !")
            pos = self.player.wall_inp()

        if not pos in self.walls and pos!=self.player.position and pos!=self.enemy.position:
            self.walls.append(pos)

    def is_wall(self, pos):
        return pos in self.walls

    def ia_configuration(self):
        try:
            with open(self.config, "r") as config2:
                file_config = json.load(config2)
                for action in file_config:
                    self.IA_config.append(action)
        except :
            print("You are setting up the AI for the 1st time")

    def nb_game_configuration(self):
        try:
            with open(self.nb_game, "r") as nb_total:
                file_game = json.load(nb_total)
                for number in file_game:
                    self.file_game.append(number)
        except :
            print("You are launching the game for the 1st time")

    def pause(self):
        print(self.separation_line)
        print("--------------- COFFEE MOMENT ----------------")
        input(self.player.name + " > Press any key to resume the current game : ")
        print("---------------- PAUSE ENDED -----------------")
        print(self.separation_line)

    def play(self):
        print(self.separation_line)
        print(self)
        finish_game = False

        if self.nb_player == 1 and self.board_size == 12:
            self.ia_configuration()
        self.nb_game_configuration()

        while not finish_game and self.key_save[-1] != 'u':
            if self.player.is_winner() or self.enemy.is_winner() and self.nb_player == 2:
                print(self.separation_line)
                print(self.player)
                print(self.enemy)
                print(self.separation_line)
                self.draw()
                if self.player.position[0] == self.board_size-2:
                    print("---------------- PLAYER 1 WINS ---------------")
                elif self.enemy.position[0] == 1 and self.nb_player == 2:
                    print("---------------- PLAYER 2 WINS ---------------")
                finish_game = True

            elif self.enemy.is_winner() and self.nb_player == 1:
                print(self.separation_line)
                print(self.player)
                print(self.enemy)
                print(self.separation_line)
                self.draw()

                if self.board_size == 12:
                    if self.file_game!= []:
                        self.file_game[-1]+=1

                    elif self.file_game== []:
                        self.file_game.append(0)
                        self.file_game.append(1)

                    with open("game.json", "w") as result:
                        json.dump(self.file_game, result)

                    actions_list = sorted(self.IA_config)
                    with open("IA_config.json", "w") as move:
                        json.dump(actions_list, move)

                print("------------------- IA WINS ------------------")
                finish_game = True

            else:
                self.play_turn()

        if self.nb_player == 1 and self.board_size == 12:
            if self.file_game == []:
                self.file_game.append(1)
                self.file_game.append(0)

            elif self.file_game != [] and self.key_save[-1] != 'u' :
                self.file_game[0]+=1

            with open("game.json", "w") as result:
                json.dump(self.file_game, result)

        print("-------------- THANKS FOR PLAYING ------------")
        print(self.separation_line)
        print("Do you want to replay ?")
        print(self.separation_line)

    def play_turn(self):
        old_player_position = self.player.position
        old_enemy_position = self.enemy.position

        print(self.separation_line)
        print(self.player)
        print(self.enemy)
        print(self.separation_line)
        self.draw()
        self.player.move(self)

        if self.key_save[-1] != 'u':
            self.enemy.move(self)

        if self.enemy.position in self.walls:
            self.enemy.position = old_enemy_position
        if self.enemy.position in self.barriers:
            self.enemy.position = old_enemy_position

        if self.is_barried(self.player.position):
            self.player.position = old_player_position
        if self.is_wall(self.player.position):
            self.player.position = old_player_position

        if self.enemy.position == self.player.position:
            self.enemy.position = old_enemy_position
        if self.player.position == self.enemy.position:
            self.player.position = old_player_position

    def setup_save(self):
        data = [self.player.name,self.player.position, self.enemy.name,self.enemy.position, self.walls, self.player.remaining_try, self.enemy.remaining_try, self.board_size, self.nb_player]
        with open("save.json", "w") as save:
            json.dump(data, save)

    def setup_IA(self):
        if self.nb_player == 1 :
            if self.IA_config== []:
                for line in range(self.board_size):
                    for col in range(self.board_size):
                        self.IA_config.append([line,col,0,0,0,0])

            if self.IA_config!= []:
                ia_line, ia_col = self.enemy.position
                for element in sorted(self.IA_config) :
                    for wall in self.walls :
                        if (ia_line, ia_col) == wall and element[0] == ia_line and element[1]== ia_col :
                            choose = random.randint(2, 3) #Permet à l'IA d'esquiver un mur en face d'elle
                            if choose == 2 :
                                self.enemy.old_actions.append(2)
                                ia_move = list((+1,+1))
                            else :
                                self.enemy.old_actions.append(3)
                                ia_move = list((+1,-1))
                            self.enemy.position = (self.enemy.position[0] + ia_move[0], self.enemy.position[1] + ia_move[1])

                    if self.enemy.old_actions[-1] == 1 and element[0] == ia_line+1 and element[1]== ia_col:
                        self.IA_config.append([ia_line+1, ia_col, element[2]+1, element[3], element[4], element[5]])
                        self.IA_config.remove([ia_line+1, ia_col, element[2], element[3], element[4], element[5]])

                    elif self.enemy.old_actions[-1] == 2 and element[0] == ia_line and element[1]== ia_col-1:
                        self.IA_config.append([ia_line, ia_col-1,element[2], element[3]+1, element[4], element[5]])
                        self.IA_config.remove([ia_line, ia_col-1,element[2], element[3], element[4], element[5]])

                    elif self.enemy.old_actions[-1] == 3 and element[0] == ia_line and element[1]== ia_col+1:
                        self.IA_config.append([ia_line, ia_col+1,element[2], element[3], element[4]+1, element[5]])
                        self.IA_config.remove([ia_line, ia_col+1,element[2], element[3], element[4], element[5]])

                    elif self.enemy.old_actions[-1] == 4 and element[0] == ia_line-1 and element[1]== ia_col : #Eviter de +1 si la la ligne de l'IA = 10 (position de départ)
                        self.IA_config.append([ia_line-1, ia_col, element[2], element[3], element[4], element[5]+1])
                        self.IA_config.remove([ia_line-1, ia_col, element[2], element[3], element[4], element[5]])
