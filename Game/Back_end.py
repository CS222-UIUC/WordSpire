import random
import contextlib
import io
import os

# default letters and their value
default_letter_bag = ["A", "A", "A", "A", "A", "A", "A", "A", "A", "B", "B", "C", "C", "D", "D", "D", "D", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "F", "F", "G", "G", "G", "H", "H", "I", "I", "I", "I", "I", "I", "I", "I", "I", "J", "K",
                      "L", "L", "L", "L", "M", "M", "N", "N", "N", "N", "N", "N", "O", "O", "O", "O", "O", "O", "O", "O", "P", "P", "Q", "R", "R", "R", "R", "R", "R", "S", "S", "S", "S", "T", "T", "T", "T", "T", "T", "U", "U", "U", "U", "V", "V", "W", "W", "X", "Y", "Y", "Z"]
default_letter_values = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1,
                         'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
                         'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}

# get word dictionary
new_path = os.path.join(os.path.dirname(__file__), '..', 'misc', 'Collins Scrabble Words (2019) with definitions.txt')
default_word_dictionary = {}
# open the file in read mode
with open(new_path, 'r') as file:
    # read lines from the file into the dictionary
    for line in file.readlines():
        key, value = line.strip().split('	')
        default_word_dictionary[key.strip()] = value.strip()


class Game:
    # all arguments have a defualt value but can be overwritten
    def __init__(self, board_size: tuple[int, int] = (7, 7), rack_size: int = 7,
                 letter_bag: list[str] = default_letter_bag, letter_values: dict[str, int] = default_letter_values,
                 word_dictionary: dict[str, str] = default_word_dictionary, mode: str = "local_mult", min_word_length: int = 4):
        """
        Innitialization function
        Note: all arguments have a defualt value but can be overwritten

        Args:
            board_size (tuple[2]): 1D tupple of length 2 containing width and height respectively
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

        Note: Scoring not yet implemented
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
                self.rack[rack_idx] = self.letter_bag[-1]
                self.letter_bag.pop()

                # score
                if self.turn:
                    self.p2_score += self.score_loc(row_idx, col_idx)
                else:
                    self.p1_score += self.score_loc(row_idx, col_idx)

                # change_turn
                if self.mode == "local_mult" or self.mode == "online_mult":
                    self.turn = not self.turn

                return 0  # returns 0 as succeeded

        return 1  # returns 1 error code for column full

    def score_list(self, letters: list, key_idx: int, min_len: int):
        score = 0
        max_idx = len(letters)

        for length in range(min_len, max_idx + 1):
            for start in range(max(key_idx - length + 1, 0), min(key_idx, max_idx - length) + 1):
                potential_word = "".join(letters[start: start + length])

                # forward
                if not '*' in potential_word and potential_word in self.dict:
                    for letter in potential_word:
                        score += self.score_dict[letter]

                # backward
                potential_word = potential_word[::-1]
                if not '*' in potential_word and potential_word in self.dict:
                    for letter in potential_word:
                        score += self.score_dict[letter]

        return score

    def score_loc(self, row_idx: int, col_idx: int):
        score = 0

        # horizontal words
        row = self.board[row_idx]
        score += self.score_list(row, col_idx, self.min_word_length)

        # vertical words
        row = [i[col_idx] for i in self.board]
        score += self.score_list(row, row_idx, self.min_word_length)

        # up-right words
        main_diagonal = [self.board[row_idx + i][col_idx + i] for i in range(
            max(0 - row_idx, 0 - col_idx), min(self.height - row_idx, self.width - col_idx))]
        score += self.score_list(main_diagonal,
                                 min(row_idx, col_idx), self.min_word_length)

        # up-left words
        anti_diagonal = [self.board[row_idx + i][col_idx - i] for i in range(max(
            0 - row_idx, col_idx - self.width + 1), min(self.height - row_idx, col_idx + 1))]
        score += self.score_list(anti_diagonal, min(row_idx,
                                 self.height - col_idx - 1), self.min_word_length)

        return score

    def get_game_state(self):
        """
        Function to determine the current state of the game

        Return:
            (int): 0 if game is not over, 1 if player 1 wins, 2 if player 2 wins, 3 if tie
        """

        # check for available columns
        for col in range(self.width):
            if self.board[-1][col] == '*' and self.letter_bag:
                return 0

        # determine game result
        if self.p1_score > self.p2_score:
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
        res += f'\n\nPlayer 1 Score: {self.p1_score}\n'
        res += f'Player 2 Score: {self.p2_score}\n\n'

        # print current player's turn
        res += f'Player {self.turn + 1}\'s Turn\n\n'

        return res

    # unused:
    # def get_col(self, col_idx):
    #     col = []
    #     for row in self.board:
    #         col.append(row[col_idx])
    #     return col
