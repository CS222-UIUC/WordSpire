import sys
import os

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../Game')))

from Back_end import *  # noqa

game_instance = Game()
print(game_instance)

chosen_rack_index = int(input(
    f'Choose a letter by index (1-{game_instance.rack_size}): ')) - 1
chosen_col = int(input(
    f'Choose a column to drop the selected letter in (1-{game_instance.width}): ')) - 1

game_instance.place_piece(chosen_rack_index, chosen_col)

print(game_instance)
