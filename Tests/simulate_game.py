import sys
import os
import random


sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../Game')))

from Back_end import *  # noqa

game_instance = Game(min_word_length = 4)
print(game_instance)

game_state = 0

while game_state == 0:
    rand_rack_index = random.randint(0, game_instance.rack_size - 1)

    available_columns = game_instance.get_available_columns()
    rand_col = random.randint(0, len(available_columns) - 1)

    game_instance.place_piece(rand_rack_index, available_columns[rand_col])

    print(game_instance)

    game_state = game_instance.get_game_state()

if game_state == 1:
    print('Player 1 wins.')
elif game_state == 2:
    print('Player 2 wins.')
else:
    print('Tie game.')
