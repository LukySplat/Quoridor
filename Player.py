class Player:
    keyboard = {'s':(1,0),
                'z':(-1,0),
                'd':(0,1),
                'q':(0,-1),
                'w':"wall",
                'u':"save"}

    def __init__(self, name, position, menu=None, remaining_try=None):
        self.name = name
        self.start = position
        self.position = position
        self.menu = menu
        self.remaining_try = remaining_try or 5

    def __str__(self):
        position_line, position_col = self.position
        return self.name + "'s position : line : " + str(position_line) + \
               ", " + "column : " + str(position_col)

    def move(self, game) :
        try:
            key = input(self.name + " > Choose between moving or placing a wall : ")
            if key not in Player.keyboard.keys():
                if key == 'p':
                    game.pause()
                    key = input(self.name + " > Choose between moving or placing a wall : ")
            assert key in Player.keyboard.keys()

        except AssertionError:
            print("Enter a valid action !")
            self.move(game)

        else:
            wall_choice = list(Player.keyboard.keys())[list(Player.keyboard.values()).index("wall")]
            save_choice = list(Player.keyboard.keys())[list(Player.keyboard.values()).index("save")]
            if key == wall_choice:
                if self.remaining_try > 0 :
                    pos = self.wall_inp()
                    game.add_wall(pos)
                    self.limit_wall()
                else:
                    print("/!\ You used all your walls !")
            elif key == save_choice:
                game.setup_save()
                game.key_save.append(key)
            else:
                move = Player.keyboard[key]
                self.position = (self.position[0] + move[0], self.position[1] + move[1])

    def wall_inp(self):
        while 1:
            try:
                line_wall = int(input("Enter the line corresponding to the wall : "))
                col_wall = int(input("Enter the column corresponding to the wall : "))
                assert 1 <= line_wall <= self.menu.board_size-2 and 1 <= col_wall <= self.menu.board_size-2
                return line_wall,col_wall

            except AssertionError:
                print("Enter a valid number !")
            except ValueError:
                print("Enter a valid number !")

    def limit_wall(self):
        self.remaining_try -= 1
        print("Wall(s) remaining for " + self.name + " : ", self.remaining_try)

    def is_winner(self):
        return self.position[0] == self.menu.board_size-2 and self.start[0] != self.position[0] or self.position[0] == 1 and self.start[0] != self.position[0]
