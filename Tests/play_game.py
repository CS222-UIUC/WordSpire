import sys
import os

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../Game')))

from Back_end import *  # noqa

game_instance = Game()
print(game_instance)

game_state = 0

while game_state == 0:
    chosen_rack_index = int(input(
        f'Choose a letter by index (1-{game_instance.rack_size}): ')) - 1
    chosen_col = int(input(
        f'Choose a column to drop the selected letter in (1-{game_instance.width}): ')) - 1

    game_instance.place_piece(chosen_rack_index, chosen_col)

    print(game_instance)

    game_state = game_instance.get_game_state()

if game_state == 1:
    print('Player 1 wins.')
elif game_state == 2:
    print('Player 2 wins.')
else:
    print('Tie game.')
