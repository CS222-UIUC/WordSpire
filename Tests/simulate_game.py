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
mode = input('Enter gamemode (single, local_mult, vs_bot): ')

depth = 7
if (mode == "vs_bot"):
    depth = int(input('Enter bot depth: '))
    bot_turn = int(input('Enter 0 if bot goes first, 1 if second: '))

# player 1 wins, losses, ties
results = [0.0, 0.0, 0.0]

for i in tqdm(range(num_games)):
    if (i % 100 == 0):
        print(i)
    game_instance = Game(min_word_length=4, mode=mode, bot_depth=depth)

    if (print_enable):
        print(game_instance)

    game_state = 0

    while game_state == 0:
        if (mode == "vs_bot" and game_instance.get_turn() == bot_turn):
            best_move = game_instance.get_best_move()
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
        if mode == 'single':
            print('Game over.')
        elif game_state == 1:
            print('Player 1 wins.')
        elif game_state == 2:
            print('Player 2 wins.')
        else:
            print('Tie game.')
    
    results[game_state - 1] += 1

print(f"\nResults: {results}\n")
print("Win rates:")
if (mode == 'local_mult'):
    print(f"   Player 1: {100 * results[0] / num_games}%")
    print(f"   Player 2: {100 * results[1] / num_games}%")
elif (mode == 'vs_bot'):
    print(f"   Bot: {100 * results[bot_turn] / num_games}%")
    print(f"   Random: {100 * results[1 - bot_turn] / num_games}%")
print(f"   Ties: {100 * results[2] / num_games}%")


# pr.disable()
# pr.dump_stats('misc/stats_post_change')
# p = pstats.Stats('misc/stats_pre_change')
# p.strip_dirs().sort_stats(SortKey.TIME).print_stats(20)
# p = pstats.Stats('misc/stats_post_change')
# p.strip_dirs().sort_stats(SortKey.TIME).print_stats(20)
