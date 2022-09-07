import random

class Ia:
    keyboard = {"up" : (-1,0),
                "right" : (0,1),
                "left" : (0,-1),
                "down" : (1,0)}

    def __init__(self, name, position, remaining_try=None) :
        self.name = name
        self.position = position
        self.remaining_try = remaining_try or 5
        self.old_actions = []
        self.old_enemy_position = []
        
    def __str__(self):
        ia_line, ia_col = self.position
        return self.name + "'s position : line : " + str(ia_line) + \
               ", " + "column : " + str(ia_col)

    def random_choice(self):
        ia_move = self.keyboard[random.choice(list(self.keyboard.keys()))]
        if ia_move == (-1,0) :
            self.old_actions.append(1)
        elif ia_move == (0,1) :
            self.old_actions.append(2)
        elif ia_move == (0,-1) :
            self.old_actions.append(3)
        elif ia_move == (1,0) :
            self.old_actions.append(4)
        return ia_move

    def move(self, game):
        if game.IA_config == [] or game.board_size != 12  :
            ia_move = self.random_choice()
            self.position = (self.position[0] + ia_move[0], self.position[1] + ia_move[1])
            game.setup_IA()

        elif game.IA_config != [] and game.board_size == 12:
            move_or_wall = random.choice([1,1,1,1,2]) #80% de move et 20% de chance pour un mur
            if move_or_wall == 2 :
                if self.remaining_try > 0:
                    player_line, player_col = game.player.position
                    pos = (player_line+1, player_col)
                    while pos in game.walls or pos==game.player.position or pos==game.enemy.position or pos in game.barriers:
                        pos = (random.randint(1, game.board_size-2), random.randint(1, game.board_size-2))

                    game.add_wall(pos)
                    self.ia_limit_wall(pos)

                else :
                    move_or_wall = 1

            if move_or_wall == 1:
                ia_line, ia_col = self.position
                for element in sorted(game.IA_config):
                    if element[0] == ia_line and element[1] == ia_col :
                        if not self.position in self.old_enemy_position :
                            if element[2] != 0 or element[3] != 0 or element[4] != 0 or element[5] != 0 :
                                choice1 = [1]*element[2]
                                choice2 = [2]*element[3]
                                choice3 = [3]*element[4]
                                choice4 = [4]*element[5]
                                choice1.extend(choice2)
                                choice1.extend(choice3)
                                choice1.extend(choice4)
                                choose = random.choice(choice1)
                                if choose == 1 :
                                    self.old_actions.append(1)
                                    ia_move = list((-1,0))
                                elif choose == 2 :
                                    self.old_actions.append(2)
                                    ia_move = list((0,1))
                                elif choose == 3 :
                                    self.old_actions.append(3)
                                    ia_move = list((0,-1))
                                elif choose == 4 :
                                    self.old_actions.append(4)
                                    ia_move = list((1,0))
                            else:
                                ia_move = self.random_choice()
                        else:
                            ia_move = self.random_choice()

                self.old_enemy_position.append(self.position)
                self.position = (self.position[0] + ia_move[0], self.position[1] + ia_move[1])
                game.setup_IA()

    def ia_limit_wall(self, pos):
        self.remaining_try -= 1
        print(self.name + " put up a wall in", pos)
        print("Wall(s) remaining for " + self.name + " : ", self.remaining_try)

    def is_winner(self):
        return self.position[0] == 1
