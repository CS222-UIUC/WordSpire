import sys
import os
import random
import cProfile
import pstats
from tqdm import tqdm
from pstats import SortKey


sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../Game')))

from Back_end import *  # noqa

# # test speed/see what is slowest
# pr = cProfile.Profile()
# pr.enable()

num_games = int(input('Enter number of games to simulate: '))
print_enable = int(input('Enable printing (0, 1): '))

depth_1 = int(input('Enter bot_1 depth (-1 for random): '))
depth_2 = int(input('Enter bot_2 depth (-1 for random): '))

mode = "vs_bot"
    
# player 1 wins, losses, ties
results = [0.0, 0.0, 0.0]

for i in tqdm(range(num_games)):
    game_instance = Game(min_word_length=4, mode=mode)

    if (print_enable):
        print(game_instance)

    game_state = 0

    while game_state == 0:
        if (game_instance.get_turn() == 0 and depth_1 != -1):
            best_move = game_instance.get_best_move(depth_1)
            game_instance.place_piece(*best_move)
        elif (game_instance.get_turn() == 1 and depth_2 != -1):
            best_move = game_instance.get_best_move(depth_2)
            game_instance.place_piece(*best_move)
        else:
            rand_rack_index = random.randint(0, game_instance.rack_size - 1)

            available_columns = game_instance.get_available_columns()
            rand_col = random.randint(0, len(available_columns) - 1)

            game_instance.place_piece(rand_rack_index, available_columns[rand_col])

        if (print_enable):
            print(game_instance)

        game_state = game_instance.get_game_state()

    if (print_enable):
        if game_state == 1:
            print('Player 1 wins.')
        elif game_state == 2:
            print('Player 2 wins.')
        else:
            print('Tie game.')
    
    results[game_state - 1] += 1

print(f"\nResults: {results}\n")
print("Win rates:")
print(f"   Bot 1 (Depth {depth_1}): {100 * results[0] / num_games}%")
print(f"   Bot 2 (Depth {depth_2}): {100 * results[1] / num_games}%")
print(f"   Ties: {100 * results[2] / num_games}%")


# pr.disable()
# pr.dump_stats('misc/stats_post_change')
# p = pstats.Stats('misc/stats_pre_change')
# p.strip_dirs().sort_stats(SortKey.TIME).print_stats(20)
# p = pstats.Stats('misc/stats_post_change')
# p.strip_dirs().sort_stats(SortKey.TIME).print_stats(20)
