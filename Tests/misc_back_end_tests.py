import contextlib
import io
import sys
import os
import cProfile
import pstats
from pstats import SortKey
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../Game')))

from Back_end import *  # noqa

# test speed/see what is slowest
# pr = cProfile.Profile()
# pr.enable()


# pr.disable()
# pr.dump_stats('misc/stats')
# p = pstats.Stats('misc/stats')
# p.strip_dirs().sort_stats(SortKey.TIME).print_stats(20)

#basic test template
game_instance = Game(board_size = (7,7))

game_instance.board = [["*", "*", "*", "*", "*", "*", "*"],
                       ["*", "*", "*", "*", "*", "*", "*"],
                       ["*", "*", "*", "*", "*", "*", "*"],
                       ["*", "*", "*", "*", "*", "*", "*"],
                       ["*", "*", "*", "*", "*", "*", "*"],
                       ["*", "*", "*", "*", "*", "*", "*"],
                       ["*", "*", "*", "*", "*", "*", "*"]]

#do something to board
#assert something about the board
check = True
if not check:
    print("----------------------------------------------------------------------------")
    all_tests = False
    print(game_instance)
    print("message")

all_tests = True

# --------------------------- Testing piece placement: ---------------------------

game_instance = Game(board_size = (7,7), letter_bag = ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
                                                       "X", "X", "X", "X", "X", "X", "X", "X", "X", "X",
                                                       "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"])

test_board = [["*", "b", "*", "d", "*", "*", "*"],
              ["*", "b", "*", "d", "*", "*", "*"],
              ["*", "b", "*", "d", "*", "*", "*"],
              ["*", "b", "*", "d", "*", "*", "*"],
              ["*", "b", "*", "*", "*", "*", "*"],
              ["*", "b", "*", "*", "*", "*", "*"],
              ["*", "b", "*", "*", "*", "*", "*"]]

game_instance.board = test_board

#invalid inputs:
status = game_instance.place_piece(-1,0)
check = status == 3 and game_instance.board == test_board
if not check:
    all_tests = False
    print("----------------------------------------------------------------------------")
    print(game_instance)
    print("Failed to handle placement with illegal rack index")

status = game_instance.place_piece(0,-1)
check = status == 2 and  game_instance.board == test_board
if not check:
    all_tests = False
    print("----------------------------------------------------------------------------")
    print(game_instance)
    print("Failed to handle placement with illegal column index")

status = game_instance.place_piece(0,1)
check = status == 1 and game_instance.board == test_board
if not check:
    all_tests = False
    print("----------------------------------------------------------------------------")
    print(game_instance)
    print("Failed to handle placement in full colum")


#valid input checks
status = game_instance.place_piece(0,0)
check = status == 0 and game_instance.board[0][0] == "X"
if not check:
    all_tests = False
    print("----------------------------------------------------------------------------")
    print(game_instance)
    print("Piece placed incorrectly in the first colum")

status = game_instance.place_piece(0,6)
check = status == 0 and game_instance.board[0][6] == "X"
if not check:
    all_tests = False
    print("----------------------------------------------------------------------------")
    print(game_instance)
    print("Piece placed incorrectly in the last colum")

status = game_instance.place_piece(0,3)
check = status == 0 and [row[3] for row in game_instance.board] == ["d", "d", "d", "d", "X", "*", "*"]
if not check:
    all_tests = False
    print("----------------------------------------------------------------------------")
    print(game_instance)
    print("Piece placed incorrectly in partially full colum")

#final checks:
check = game_instance.board == [["X", "b", "*", "d", "*", "*", "X"],
                                ["*", "b", "*", "d", "*", "*", "*"],
                                ["*", "b", "*", "d", "*", "*", "*"],
                                ["*", "b", "*", "d", "*", "*", "*"],
                                ["*", "b", "*", "X", "*", "*", "*"],
                                ["*", "b", "*", "*", "*", "*", "*"],
                                ["*", "b", "*", "*", "*", "*", "*"]]
if not check:
    all_tests = False
    print("----------------------------------------------------------------------------")
    print(game_instance)
    print("Something went wrong when testing pieces")

#player switching
check = game_instance.get_turn() == 1
if not check:
    all_tests = False
    print("----------------------------------------------------------------------------")
    print(game_instance)
    print("Something went wrong with switching player")

#removing from bag
check = len(game_instance.letter_bag) == 20
if not check:
    all_tests = False
    print("----------------------------------------------------------------------------")
    print(game_instance)
    print("Something went wrong with the letterbag")

# ------------------------------- Testing status: -------------------------------

game_instance = Game(board_size = (7,7))

test_board = [["a", "b", "c", "d", "e", "f", "g"],
              ["a", "b", "c", "d", "e", "f", "g"],
              ["a", "b", "c", "d", "e", "f", "g"],
              ["a", "b", "c", "d", "e", "f", "g"],
              ["a", "b", "c", "d", "e", "f", "g"],
              ["a", "b", "c", "d", "e", "f", "g"],
              ["a", "b", "d", "d", "e", "f", "*"]]

game_instance.board = test_board

#make player 1 winning
game_instance.p1_score = 1

#finding empty column
check = game_instance.get_game_state() == 0
if not check:
    print("----------------------------------------------------------------------------")
    all_tests = False
    print(game_instance)
    print("Game ended too early")

check = game_instance.get_available_columns() == [6]
if not check:
    print("----------------------------------------------------------------------------")
    all_tests = False
    print(game_instance)
    print(f"Found inccorrect empty columns: {game_instance.get_available_columns()}")

#simulate an empty rack
game_instance.rack_size = 0
check = game_instance.get_game_state() == 1
if not check:
    print("----------------------------------------------------------------------------")
    all_tests = False
    print(game_instance)
    if game_instance.get_game_state() == 0:
        print("Game didn't end when rack is empty")
    else:
        print("Incorrect winner on empty rack case")

#restore rack
game_instance.rack_size = 7
#fill last comlumn
game_instance.place_piece(0,6)
#make player 2 winning
game_instance.p2_score = 2

check = game_instance.get_game_state() == 2
if not check:
    print("----------------------------------------------------------------------------")
    all_tests = False
    print(game_instance)
    if game_instance.get_game_state() == 0:
        print("Game didn't end when rack is empty")
    else:
        print("Incorrect winner on full board case")

#make tie
game_instance.p2_score = 1
check = game_instance.get_game_state() == 3
if not check:
    print("----------------------------------------------------------------------------")
    all_tests = False
    print(game_instance)
    print("Players didn't tie correctly")


# ------------------------------- Testing scoring: -------------------------------

custom_dict = dict()
custom_dict["LEVEL"] = "?"
custom_dict["TESTS"] = "?"
custom_dict["TEST"] = "?"
custom_dict["SET"] = "?"
custom_dict["AMAZING"] = "?"

game_instance = Game(board_size = (7,7), word_dictionary = custom_dict)

test_board = [["T", "*", "*", "*", "T", "*", "G"],
              ["L", "E", "V", "E", "L", "*", "N"],
              ["*", "*", "S", "*", "*", "*", "I"],
              ["*", "T", "*", "T", "*", "*", "Z"],
              ["S", "E", "*", "S", "*", "*", "A"],
              ["*", "S", "T", "E", "S", "T", "M"],
              ["*", "T", "*", "T", "*", "*", "A"]]

expected_outputs = defaultdict(lambda : defaultdict(lambda : []))

#first column
expected_outputs [0][0] = [("TEST", 4, "?", ((0, 0), (3, 3)))]
expected_outputs [0][1] = [("LEVEL", 8, "?", ((0, 1), (4, 1))), ("LEVEL", 8, "?", ((4, 1), (0, 1)))]
expected_outputs [0][4] = [("TESTS", 5, "?", ((4, 0), (0, 4)))]

#second column
expected_outputs [1][1] = [("LEVEL", 8, "?", ((0, 1), (4, 1))), ("LEVEL", 8, "?", ((4, 1), (0, 1))), ("TEST", 4, "?", ((0, 0), (3, 3)))]
expected_outputs [1][3] = [("TEST", 4, "?", ((4, 0), (1, 3))), ("TESTS", 5, "?", ((4, 0), (0, 4))), ("TEST", 4, "?", ((1, 3), (1, 6)))]
expected_outputs [1][4] = expected_outputs [1][5] = expected_outputs [1][6] =[("TEST", 4, "?", ((1, 3), (1, 6)))]


#third column
expected_outputs [2][1] = [("LEVEL", 8, "?", ((0, 1), (4, 1))), ("LEVEL", 8, "?", ((4, 1), (0, 1)))]
expected_outputs [2][2] = [("TEST", 4, "?", ((4, 0), (1, 3))), ("TESTS", 5, "?", ((4, 0), (0, 4))), ("TEST", 4, "?", ((0, 0), (3, 3)))]
expected_outputs [2][5] = [("TEST", 4, "?", ((2, 5), (5, 5)))]

#fourth column
expected_outputs [3][1] = [("LEVEL", 8, "?", ((0, 1), (4, 1))), ("LEVEL", 8, "?", ((4, 1), (0, 1))), ("TEST", 4, "?", ((4, 0), (1, 3))), ("TESTS", 5, "?", ((4, 0), (0, 4)))]
expected_outputs [3][3] = [("TEST", 4, "?", ((0, 0), (3, 3))), ("TEST", 4, "?", ((3, 6), (3, 3)))]
expected_outputs [3][4] = expected_outputs [3][6] = [("TEST", 4, "?", ((3, 6), (3, 3)))]
expected_outputs [3][5] = [("TEST", 4, "?", ((3, 6), (3, 3))), ("TEST", 4, "?", ((2, 5), (5, 5)))]


#fifth column
expected_outputs [4][0] = [("TEST", 4, "?", ((4, 0), (1, 3))), ("TESTS", 5, "?", ((4, 0), (0, 4)))]
expected_outputs [4][1] = [("LEVEL", 8, "?", ((0, 1), (4, 1))), ("LEVEL", 8, "?", ((4, 1), (0, 1)))]
expected_outputs [4][5] = [("TEST", 4, "?", ((2, 5), (5, 5)))]

#sixth column
expected_outputs [5][5] = [("TEST", 4, "?", ((2, 5), (5, 5)))]

#seventh column (amazing)
expected_outputs [6] = defaultdict(lambda : [("AMAZING", 19, "?", ((6, 6), (6, 0)))])


game_instance.board = test_board
printed = False

#check each square on grid against expected output
for x in range(7):
    for y in range(7):
        word_list = game_instance.get_words(x,y)
        check = set(word_list) == set(expected_outputs[x][y])
        if not check:
            all_tests = False

            if not printed:
                printed = True
                print(game_instance)
            
            print(f"Something went wrong when finding words at location ({x}, {y}):")
            print("Expected:")
            print(expected_outputs[x][y])
            print("Got:")
            print(word_list)
            print()
        #important = input()
            
#testing different min word lengths
game_instance.min_word_length = 3
word_list = game_instance.get_words(4,0)
check = set(word_list) == set([("SET", 3, "?", ((2, 2), (4, 0))), ("TEST", 4, "?", ((4, 0), (1, 3))), ("TESTS", 5, "?", ((4, 0), (0, 4)))])
if not check:
    all_tests = False
    print(game_instance)
    print(f"Min length 3 failes")
    print("Expected:")
    print([("SET", 3, "?", ((2, 2), (4, 0))), ("TEST", 4, "?", ((4, 0), (1, 3))), ("TESTS", 5, "?", ((4, 0), (0, 4)))])
    print("Got:")
    print(word_list)
    print()

game_instance.min_word_length = 5
word_list = game_instance.get_words(4,0)
check = set(word_list) == set([("TESTS", 5, "?", ((4, 0), (0, 4)))])
if not check:
    all_tests = False
    print(game_instance)
    print(f"Min length 5 failes")
    print("Expected:")
    print([("TESTS", 5, "?", ((4, 0), (0, 4)))])
    print("Got:")
    print(word_list)
    print()

# -------------------------------------- end --------------------------------------
if all_tests:
    print("All tests passed!!")
else:
    print(("----------------------------------------------------------------------------"))

