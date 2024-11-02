import random
import contextlib
import io
import sys
import os
import math
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../misc')))

from console_text import bcolors  # noqa

# default letters and their value
default_letter_bag = ["A", "A", "A", "A", "A", "A", "A", "A", "A", "B", "B", "C", "C", "D", "D", "D", "D", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "F", "F", "G", "G", "G", "H", "H", "I", "I", "I", "I", "I", "I", "I", "I", "I", "J", "K",
                      "L", "L", "L", "L", "M", "M", "N", "N", "N", "N", "N", "N", "O", "O", "O", "O", "O", "O", "O", "O", "P", "P", "Q", "R", "R", "R", "R", "R", "R", "S", "S", "S", "S", "T", "T", "T", "T", "T", "T", "U", "U", "U", "U", "V", "V", "W", "W", "X", "Y", "Y", "Z"]
default_letter_values = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1,
                         'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
                         'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}
default_len_bonus = {4 : 0, 5 : 5, 6 : 10, 7 : 20, 8 : 30, 9 : 50, 10 : 100}

# get word dictionary
new_path = os.path.join(os.path.dirname(__file__), '..', 'misc', 'Collins Scrabble Words (2019) with definitions.txt')  # noqa
default_word_dictionary = {}
# open the file in read mode
with open(new_path, 'r') as file:
    # read lines from the file into the dictionary
    for line in file.readlines():
        key, value = line.strip().split('	')
        default_word_dictionary[key.strip().upper()] = value.strip()


class Game:
    # all arguments have a default value but can be overwritten
    def __init__(self, board_size: tuple[int, int] = (7, 7), rack_size: int = 7,
                 letter_bag: list[str] = default_letter_bag, letter_values: dict[str, int] = default_letter_values,
                 word_dictionary: dict[str, str] = default_word_dictionary, mode: str = "local_mult", min_word_length: int = 4,
                 num_multipliers = 5, len_bonus = default_len_bonus):
        """
        Innitialization function
        Note: all arguments have a defualt value but can be overwritten

        Args:
            board_size (tuple[2]): 1D tuple of length 2 containing width and height respectively
            rack_size  (int): number of letters player can choose from on the letter rack
            letter_bag (list): list of starting letters
            letter_values (dict): a dictionary mapping all letters to their point value
            mode (str): describes how the game should run ["single","local_mult","online_mult","vs_bot"]

        Return:
            Void
        """

        # create board with list comprehension
        self.width = board_size[1]
        self.height = board_size[0]
        self.board = [["*" for i in range(self.width)]
                      for z in range(self.height)]
        
        self.bonus_squares = defaultdict(lambda : 1)
        for i in range(num_multipliers):
            self.bonus_squares[(random.randint(0, self.height - 1), random.randint(0, self.width - 1))] += 1
        self.len_bonus = defaultdict(lambda : 100, len_bonus)

        # create random letter rack and shuffle letter bag
        shuffled_letters = letter_bag
        random.shuffle(shuffled_letters)
        self.rack_size = rack_size
        self.letter_bag = shuffled_letters[self.rack_size:]
        self.rack = shuffled_letters[0:self.rack_size]

        # other misc info
        self.mode = mode
        self.min_word_length = min_word_length
        self.p1_score = 0
        self.p2_score = 0
        self.turn = False
        self.dict = word_dictionary
        self.score_dict = letter_values

        # game history (list of turns)
        self.game_history = []

    def get_board(self):
        """
        Board getter function

        Return:
            board (2D-list): 2D array of strings representing the board
        """
        return self.board

    def get_rack(self):
        """
        Rack getter function

        Return:
            rack (list): list of strings representing current letters on the rack
        """
        return self.rack

    def get_scores(self):
        """
        Score getter function

        Return:
            score (tuple[2]): tuple of length 2 containing score of player 1 and player 2 respectively
        """
        return (self.p1_score, self.p2_score)

    def get_turn(self):
        """
        Turn getter function

        Return:
            turn (int): 0 if player 1, 1 if player 2, in single player always 0
        """
        return int(self.turn)

    def place_piece(self, rack_idx: int, col_idx: int):
        """
        Function to place a new tile from the tiles on the letter rack

            rack_idx (int): an int between 0 and rack_size
            col_idx (int): an int between 0 and board_width

        Return:
            status_code (int): 0 if successful, 1 if column is full, 2 if outside board, 3 if outside rack 
        """

        # ensure valid input values
        if col_idx >= self.width or col_idx < 0:
            return 2
        if rack_idx >= self.rack_size or rack_idx < 0:
            return 3

        # main placement loop
        for row_idx, row in enumerate(self.board):

            # find lowest empty point in col
            if row[col_idx] == "*":

                # place the piece
                row[col_idx] = self.rack[rack_idx]

                # refill letter rack
                if self.letter_bag:
                    self.rack[rack_idx] = self.letter_bag[-1]
                    self.letter_bag.pop()
                # if no letters left in letter bag
                else:
                    self.rack.pop(rack_idx)
                    self.rack_size -= 1

                # score
                score_gained = 0
                words = self.get_words(col_idx, row_idx)
                if self.turn:
                    for word in words:
                        score_gained += word[1]
                        self.p2_score += word[1]

                else:
                    for word in words:
                        score_gained += word[1]
                        self.p1_score += word[1]

                # add turn to game history
                turn = Turn(self.board, self.turn,
                            row[col_idx], col_idx, score_gained, words)
                self.game_history.append(turn)

                # change_turn
                if self.mode == "local_mult" or self.mode == "online_mult":
                    self.turn = not self.turn

                return 0  # returns 0 as succeeded

        return 1  # returns 1 error code for column full

    def search_list(self, letters: list, key_idx: int, min_len: int, start_pos: tuple[int, int], end_pos: tuple[int, int], bonus):
        """
        Finds all valid words and their definitions in a single row/list of characters

            letters (list): list of upercase letters in a row
            key_idx: (int): index of letter required to be in word
            min_len (int):  minimum length words to score
            start_pos (tuple(int,int)):
            end_pos (tuple(int,int)):

        Return:
            words (list((string, int, string, ((int, int), (int, int))))): list of words, score, their definitions, and location on the board
        """

        # initialize basic variables
        words = []
        max_idx = len(letters)
        ltrs_string = "".join(letters)

        col_dir = int(math.copysign(
            1, end_pos[0] - start_pos[0])) if end_pos[0] - start_pos[0] != 0 else 0
        row_dir = int(math.copysign(
            1, end_pos[1] - start_pos[1])) if end_pos[1] - start_pos[1] != 0 else 0

        for start in range(key_idx + 1):   # loop over possible start indices
            # loop over possible end indices
            for end in range(max(start + min_len, key_idx + 1), max_idx + 1):
                potential_word = ltrs_string[start:end]

                # forward
                if potential_word in self.dict:
                    word_start = (
                        start_pos[0] + col_dir * start, start_pos[1] + row_dir * start)
                    word_end = (start_pos[0] + col_dir * (end - 1),
                                start_pos[1] + row_dir * (end - 1))
                    score = 0
                    for letter in potential_word:
                        score += self.score_dict[letter]
                    score *= bonus
                    score += self.len_bonus[abs(end - start)]
                    
                    words.append(
                        (potential_word, score, self.dict[potential_word], (word_start, word_end)))

                # backward
                potential_word = potential_word[::-1]
                if potential_word in self.dict:
                    word_start = (
                        start_pos[0] + col_dir * (end - 1), start_pos[1] + row_dir * (end - 1))
                    word_end = (start_pos[0] + col_dir *
                                start, start_pos[1] + row_dir * start)
                    score = 0
                    for letter in potential_word:
                        score += self.score_dict[letter]
                    score *= bonus
                    score += self.len_bonus[abs(end - start)]

                    words.append(
                        (potential_word, score, self.dict[potential_word], (word_start, word_end)))

        return words

    def get_words(self, col_idx: int, row_idx: int):
        """
        Scores a move that places a tile

            col_idx (int): an int between 0 and board_width giving the col of the tile for which we want to find words 
            row_idx (int): an int between 0 and board_height giving the row of the tile for which we want to find words 

        Return:
            words (list((string, int, string, ((int, int), (int, int))))): list of words, score, their definitions, and location on the board
        """

        origin = self.board[row_idx][col_idx]
        if origin == "*":
            return []

        bonus = self.bonus_squares[(row_idx, col_idx)]
        words = []

        # horizontal words
        start_offset = col_idx
        for i in range(1, start_offset + 1):
            if self.board[row_idx][col_idx - i] == "*":
                start_offset = i - 1
                break

        end_offset = self.width - col_idx - 1
        for i in range(1, end_offset + 1):
            if self.board[row_idx][col_idx + i] == "*":
                end_offset = i - 1
                break

        row = self.board[row_idx][col_idx -
                                  start_offset: col_idx + end_offset + 1]
        start_pos = (col_idx - start_offset, row_idx)
        end_pos = (col_idx + end_offset - 1, row_idx)
        words.extend(self.search_list(row, start_offset,
                     self.min_word_length, start_pos, end_pos, bonus))

        # vertical words
        start_offset = row_idx
        for i in range(1, start_offset + 1):
            if self.board[row_idx - i][col_idx] == "*":
                start_offset = i - 1
                break

        end_offset = self.height - row_idx - 1
        for i in range(1, end_offset + 1):
            if self.board[row_idx + i][col_idx] == "*":
                end_offset = i - 1
                break

        col = [self.board[row_idx + row][col_idx]
               for row in range(-start_offset, end_offset + 1)]
        start_pos = (col_idx, row_idx - start_offset)
        end_pos = (col_idx, row_idx + end_offset - 1)
        words.extend(self.search_list(col, start_offset,
                     self.min_word_length, start_pos, end_pos, bonus))

        # up-right words
        start_offset = min(row_idx, col_idx)
        for i in range(1, start_offset + 1):
            if self.board[row_idx - i][col_idx - i] == "*":
                start_offset = i - 1
                break

        end_offset = min(self.height - row_idx - 1, self.width - col_idx - 1)
        for i in range(1, end_offset + 1):
            if self.board[row_idx + i][col_idx + i] == "*":
                end_offset = i - 1
                break

        main_diagonal = [self.board[row_idx + i][col_idx + i]
                         for i in range(-start_offset, end_offset + 1)]
        start_pos = (col_idx - start_offset, row_idx - start_offset)
        end_pos = (col_idx + end_offset - 1, row_idx + end_offset - 1)
        words.extend(self.search_list(main_diagonal, start_offset,
                     self.min_word_length, start_pos, end_pos, bonus))

        # up-left words
        start_offset = min(row_idx, self.width - col_idx - 1)
        for i in range(1, start_offset + 1):
            if self.board[row_idx - i][col_idx + i] == "*":
                start_offset = i - 1
                break

        end_offset = min(self.height - row_idx - 1, col_idx)
        for i in range(1, end_offset + 1):
            if self.board[row_idx + i][col_idx - i] == "*":
                end_offset = i - 1
                break

        anti_diagonal = [self.board[row_idx + i][col_idx - i]
                         for i in range(-start_offset, end_offset + 1)]
        start_pos = (col_idx + start_offset, row_idx - start_offset)
        end_pos = (col_idx - end_offset + 1, row_idx + end_offset - 1)
        words.extend(self.search_list(anti_diagonal, start_offset,
                     self.min_word_length, start_pos, end_pos, bonus))

        return words

    def get_game_state(self):
        """
        Function to determine the current state of the game

        Note:
            If the gamemode is single-player, return 1 when the game is over.

        Return:
            (int): 0 if game is not over, 1 if player 1 wins, 2 if player 2 wins, 3 if tie
        """

        # check for remaingin tiles in tile rack
        if self.rack_size != 0:
            # check for available columns
            for col in range(self.width):
                if self.board[-1][col] == '*' and self.letter_bag:
                    return 0

        # determine game result
        if self.p1_score > self.p2_score or self.mode == 'single':
            return 1
        elif self.p2_score > self.p1_score:
            return 2

        return 3

    def get_available_columns(self):
        """
        Function to aquire available columns for dropping letters

        Return:
            available_columns (List[int]): list of available columns (0-indexed)
        """

        available_columns = []
        for i in range(self.width):
            if self.board[-1][i] == '*':
                available_columns.append(i)

        return available_columns

    def __str__(self):
        """
        Function to define string representation of Game object

        The string representation displays the current board, 
        letter rack, player scores, and turn

        Note:
            Currently defined for multiplayer mode

        Return:
            res (string): String representation of the attributes stated above
        """
        # print board
        row_str = '+'
        for i in range(self.width):
            row_str += '-----+'

        res = 'Board:\n\n' + row_str + '\n'
        for i in range(self.height - 1, -1, -1):
            for j in range(self.width):
                if self.board[i][j] == "*" and self.bonus_squares[(i,j)] > 1:
                    res += f'|  {self.bonus_squares[(i,j)]}  '
                else:
                    res += f'|  {self.board[i][j]}  '
            res += f'|\n{row_str}\n'

        # print column labels
        res += '   '
        for i in range(self.width):
            res += f'{i + 1}     '

        # print letter rack
        res += f'\n\nLetter Rack:     {self.rack}\n'

        # print letter rack indicies
        res += 'Rack Indicies:     '
        for i in range(self.rack_size):
            res += f'{i + 1}    '

        # print scores
        if self.mode == 'single':
            res += f'\n\nScore: {self.p1_score}\n'
        elif self.mode == 'local_mult':
            res += f'\n\nPlayer 1 Score: {self.p1_score}\n'
            res += f'Player 2 Score: {self.p2_score}\n\n'

        # print current player's turn
        if self.mode == 'local_mult':
            res += f'Player {self.turn + 1}\'s Turn\n\n'

        return res


class Turn:
    def __init__(self, board: list[list[int]], turn: int, letter: str, letter_col: int,
                 score_gained: int, words_formed: list[tuple[str, int, str, tuple[tuple[int, int], tuple[int, int]]]]):
        """
        Innitialization function

        Args:
            board (list): the game's board after this turn
            turn (int): 0 if player 1's turn, 1 if player 2's turn
            letter (str): player's chosen letter
            letter_col (tuple): column of placed letter, 0-indexed
            score_gained (int): player's increase in score from this turn
            words_formed (list): list of words formed and related info

        Return:
            Void
        """

        # board attributes
        self.height = len(board)
        self.width = len(board[0])

        # store turn attributes
        self.board = [[item for item in board[i]] for i in range(self.height)]
        self.turn = turn
        self.letter = letter
        self.letter_col = letter_col
        self.score_gained = score_gained
        self.words_formed = words_formed

        # create board with highlighted words
        color = bcolors.OKBLUE
        if turn:
            color = bcolors.OKGREEN

        for word in words_formed:
            start_pos = word[3][0]
            end_pos = word[3][1]
            col_dir = int(math.copysign(
                1, end_pos[0] - start_pos[0])) if end_pos[0] - start_pos[0] != 0 else 0
            row_dir = int(math.copysign(
                1, end_pos[1] - start_pos[1])) if end_pos[1] - start_pos[1] != 0 else 0
            for i in range(len(word[0])):
                row, col = start_pos[1] + i * \
                    row_dir, start_pos[0] + i * col_dir
                self.board[row][col] = f'{
                    color}{self.board[row][col]}{bcolors.ENDC}'

    def __str__(self):
        """
        Function to define string representation of Turn object

        The string representation states whose turn it is, the placed letter,
        the column of the letter, the change in score, and the words formed

        The board after this turn was played is also shown

        Return:
            res (string): String representation of the attributes stated above
        """

        # print board
        row_str = '+'
        for i in range(self.width):
            row_str += '-----+'

        res = 'Board:\n\n' + row_str + '\n'
        for i in range(self.height - 1, -1, -1):
            for j in range(self.width):
                res += f'|  {self.board[i][j]}  '
            res += f'|\n{row_str}\n'

        # print column labels
        res += '   '
        for i in range(self.width):
            res += f'{i + 1}     '

        # print turn information
        res += f"""\n\nPlayer {self.turn + 1} placed the letter \'{
            self.letter}\' in column {self.letter_col + 1}.\n\n"""

        if self.words_formed:
            res += f"""Player {self.turn + 1} gained {
                self.score_gained} score through the following words:\n"""
            for word in self.words_formed:
                res += f'   {word[0]} (+{word[1]})\n'

        return res + '\n'
