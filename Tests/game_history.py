import sys
import os
import random


sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../Game')))

from Back_end import *  # noqa

mode = input('Enter gamemode (single, local_mult): ')

game_instance = Game(min_word_length=4, mode=mode)

game_state = 0

while game_state == 0:
    rand_rack_index = random.randint(0, game_instance.rack_size - 1)

    available_columns = game_instance.get_available_columns()
    rand_col = random.randint(0, len(available_columns) - 1)

    game_instance.place_piece(rand_rack_index, available_columns[rand_col])

    game_state = game_instance.get_game_state()

# look at game history
for turn in game_instance.game_history:
    if turn.score_gained > 0:
        print(turn)

scores = game_instance.get_scores()

if mode == 'single':
    print(f'Final score: {scores[0]}')
elif mode == 'local_mult':
    print('Final scores: ')
    print(f'   Player 1: {scores[0]}')
    print(f'   Player 2: {scores[1]}')
