
import random

class Game:
    def __init__(self, board_size = (7,7), rack_size = 7, letter_bag = "", mode = "local_mult"):
        self.board = [["*" for i in range(board_size[0])]for i in range(board_size[1])]
        shuffled_letters = random.shuffle(letter_bag)
        self.letter_bag = shuffled_letters[rack_size:]
        self.rack = shuffled_letters[0:rack_size]
        self.mode = mode

    def place_piece(self, rack_idx, col_idx):
        for row in self.board[::-1]:
            if row[col_idx] == "*":
                row[col_idx] = self.rack[rack_idx]
                self.rack[rack_idx] = self.letter_bag[0]
                self.letter_bag = self.letter_bag[1:0]
                return 0

        return 1


    # def get_col(self, col_idx):
    #     col = []
    #     for row in self.board:
    #         col.append(row[col_idx])
    #     return col




    












