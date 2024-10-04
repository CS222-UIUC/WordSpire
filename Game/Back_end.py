
import random

default_letter_bag = ["A","A","A","A","A","A","A","A","A","B","B","C","C","D","D","D","D","E","E","E","E","E","E","E","E","E","E","E","E","F","F","G","G","G","H","H","I","I","I","I","I","I","I","I","I","J","K","L","L","L","L","M","M","N","N","N","N","N","N","O","O","O","O","O","O","O","O","P","P","Q","R","R","R","R","R","R","S","S","S","S","T","T","T","T","T","T","U","U","U","U","V","V","W","W","X","Y","Y","Z"]
default_letter_values = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 
                         'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 
                         'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}

class Game:
    def __init__(self, board_size = (7,7), rack_size = 7, letter_bag = default_letter_bag, letter_values = default_letter_values, mode = "local_mult"):        
        self.board = [["*" for i in range(board_size[0])]for i in range(board_size[1])]
        shuffled_letters = random.shuffle(letter_bag)
        self.letter_bag = shuffled_letters[rack_size:]
        self.rack = shuffled_letters[0:rack_size]
        self.mode = mode
        self.p1_score = 0
        self.p2_score = 0
        self.turn = True

    def get_board(self):
        return self.board
    
    def get_rack(self):
        return self.rack
    
    def get_scores(self):
        return (self.p1_score, self.p2_score)
        
    def get_turn(self):
        return int(self.turn)

    def place_piece(self, rack_idx, col_idx):
        for row in self.board[::-1]:
            if row[col_idx] == "*":
                row[col_idx] = self.rack[rack_idx]
                self.rack[rack_idx] = self.letter_bag[0]
                self.letter_bag = self.letter_bag[1:]
                self.turn = not self.turn
                return 0

        return 1


    # def get_col(self, col_idx):
    #     col = []
    #     for row in self.board:
    #         col.append(row[col_idx])
    #     return col




    












