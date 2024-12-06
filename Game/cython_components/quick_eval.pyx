# min_max_bot.pyx
# cython: language_level=3

import random
import math
import copy
import sys
from typing import List, Dict, Tuple
from libc.limits cimport INT_MAX

cdef class min_max_bot:
    cdef int max_depth
    cdef int height
    cdef int width
    cdef int min_word_length
    cdef Dict[str, int] score_dict
    cdef Dict[str, int] word_dict

    def __init__(self, int max_depth, int height, int width, int min_word_length, Dict[str, int] score_dict, Dict[str, int] word_dict):
        self.max_depth = max_depth
        self.height = height
        self.width = width
        self.min_word_length = min_word_length
        self.score_dict = score_dict
        self.word_dict = word_dict

    def get_best_move(self, List[List[str]] board, List[str] rack, List[str] bag):
        cdef int depth = min(self.max_depth, len(rack))
        val, move = self.simple_alphabeta(board, rack, 0, depth, -INT_MAX, INT_MAX, True)
        return move

    cdef simple_alphabeta(self, List[List[str]] board, List[str] rack, int score, int depth, int a, int b, bint maximizer):
        if depth == 0:
            return (score, (-1, -1))

        cdef List[int] available_columns = self.get_available_columns(board)

        if not available_columns:
            return (score, (-1, -1))

        cdef List[Tuple[Tuple[int, int], 
                        List[List[str]], 
                        List[str], 
                        int]] moves = self.order_moves(board, rack, available_columns)
        best_move = (-1, -1)

        cdef int value
        if maximizer:
            value = -INT_MAX
            for move, new_board, new_rack, gained_score in moves:
                curr_val, curr_move = self.simple_alphabeta(new_board, new_rack, score + gained_score, depth - 1, a, b, False)
                if curr_val > value:
                    value = curr_val
                    best_move = move
                if value >= b:
                    break
                a = max(a, value)

            return (value, best_move)
        else:
            value = INT_MAX
            for move, new_board, new_rack, gained_score in moves:
                curr_val, curr_move = self.simple_alphabeta(new_board, new_rack, score - gained_score, depth - 1, a, b, True)
                if curr_val < value:
                    value = curr_val
                    best_move = move
                if value <= a:
                    break
                b = min(b, value)

            return (value, best_move)

    cdef order_moves(self, List[List[str]] board, List[str] rack, List[int] available_columns):
        cdef List[Tuple[Tuple[int, int], List[List[str]], List[str], int]] moves = []
        cdef int idx
        for col in available_columns:
            for idx, letter in enumerate(rack):
                new_board, gained_score = self.update_board(board, letter, col)
                moves.append(((idx, col), new_board, rack[:idx] + rack[idx+1:], gained_score))
        moves.sort(reverse=True, key=lambda i: (i[3], random.random()))
        return moves

    cdef get_available_columns(self, List[List[str]] board):
        cdef List[int] available_columns = []
        for i in range(self.width):
            if board[-1][i] == '*':
                available_columns.append(i)
        return available_columns

    cdef update_board(self, List[List[str]] board, str letter, int col_idx):
        cdef List[List[str]] board_copy = copy.deepcopy(board)

        for row_idx, row in enumerate(board_copy):
            if row[col_idx] == "*":
                row[col_idx] = letter
                return (board_copy, self.get_score(board_copy, row_idx, col_idx))

        raise Exception("Illegal move, column full.")

    cdef score_list(self, List[str] letters, int key_idx, int min_len):
        """
        Scores all valid words in a single row/list of characters

            letters (list): list of uppercase letters in a row
            key_idx (int): index of letter required to be in word
            min_len (int): minimum length words to score

        Return:
            score (int): number of points for all found words
        """

        # initialize basic variables
        cdef int score = 0
        cdef int max_idx = len(letters)
        cdef str ltrs_string = "".join(letters)
        cdef int min_end = 0
        cdef str potential_word = ""

        for start in range(key_idx + 1):   # loop over possible start indices
            # loop over possible end indices
            min_end = max(start + min_len - 1, key_idx)
            potential_word = ltrs_string[start:min_end]
            for end in range(min_end + 1, max_idx + 1):
                potential_word += ltrs_string[end - 1]

                # forward
                if potential_word in self.word_dict:
                    # score per letter in word
                    for letter in potential_word:
                        score += self.score_dict[letter]

                # backward
                potential_word = potential_word[::-1]
                if potential_word in self.word_dict:
                    # score per letter in word
                    for letter in potential_word:
                        score += self.score_dict[letter]

        return score

    cdef get_score(self, List[List[str]] board, int row_idx, int col_idx):
        """
        Scores a move that places a tile

            row_idx (int): an int between 0 and board_height giving the row of the tile for which we want to find words 
            col_idx (int): an int between 0 and board_width giving the col of the tile for which we want to find words 

        Return:
            score (int): the score for the current move
        """

        cdef str origin = board[row_idx][col_idx]
        if origin == "*":
            return 0

        cdef int score = 0

        cdef int i

        # horizontal words
        cdef int start_offset = col_idx
        for i in range(1, start_offset + 1):
            if board[row_idx][col_idx - i] == "*":
                start_offset = i - 1
                break

        cdef int end_offset = self.width - col_idx
        for i in range(1, end_offset):
            if board[row_idx][col_idx + i] == "*":
                end_offset = i - 1
                break

        cdef List[str] row = board[row_idx][col_idx - start_offset: col_idx + end_offset]
        score += self.score_list(row, start_offset, self.min_word_length)

        # vertical words
        start_offset = row_idx
        for i in range(1, start_offset + 1):
            if board[row_idx - i][col_idx] == "*":
                start_offset = i - 1
                break

        end_offset = self.height - row_idx
        for i in range(1, end_offset):
            if board[row_idx + i][col_idx] == "*":
                end_offset = i - 1
                break

        cdef List[str] col = []
        for i in range(-start_offset, end_offset):
            col.append(board[row_idx + i][col_idx])
        score += self.score_list(col, start_offset, self.min_word_length)

        # up-right words
        start_offset = min(row_idx, col_idx)
        for i in range(1, start_offset + 1):
            if board[row_idx - i][col_idx - i] == "*":
                start_offset = i - 1
                break

        end_offset = min(self.height - row_idx, self.width - col_idx)
        for i in range(1, end_offset):
            if board[row_idx + i][col_idx + i] == "*":
                end_offset = i - 1
                break

        cdef List[str] main_diagonal = []
        for i in range(-start_offset, end_offset):
            main_diagonal.append(board[row_idx + i][col_idx + i])
        score += self.score_list(main_diagonal, start_offset, self.min_word_length)

        # up-left words
        start_offset = min(row_idx, self.width - col_idx - 1)
        for i in range(1, start_offset + 1):
            if board[row_idx - i][col_idx + i] == "*":
                start_offset = i - 1
                break

        end_offset = min(self.height - row_idx, col_idx + 1)
        for i in range(1, end_offset):
            if board[row_idx + i][col_idx - i] == "*":
                end_offset = i - 1
                break

        cdef List[str] anti_diagonal = []
        for i in range(-start_offset, end_offset):
            anti_diagonal.append(board[row_idx + i][col_idx - i])
        score += self.score_list(anti_diagonal, start_offset, self.min_word_length)

        return score
