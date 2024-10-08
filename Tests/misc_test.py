from PyDictionary import PyDictionary
import contextlib
import io
import sys
import os
import cProfile
import pstats
from pstats import SortKey

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../Game')))

from Back_end import *  # noqa

game_instance = Game()

# test speed/see what is slowest
# pr = cProfile.Profile()
# pr.enable()

print(game_instance)
game_instance.score_loc(4, 3)


# pr.disable()
# pr.dump_stats('misc/stats')
# p = pstats.Stats('misc/stats')
# p.strip_dirs().sort_stats(SortKey.TIME).print_stats(20)
