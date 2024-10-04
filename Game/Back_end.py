
import random

class Game:
  def __init__(self, board_size = (7,7), rack_size = 7, letter_bag = "", mode = "local_mult"):
    self.board = [["*" for i in range(board_size[0])]for i in range(board_size[1])]
    shuffled_letters = random.shuffle(letter_bag)
    self.letter_bag = shuffled_letters[rack_size:]
    self.rack = shuffled_letters[0:rack_size]
    self.mode = mode


    












