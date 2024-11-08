def search_list(self, letters: list, key_idx: int, min_len: int):
    """
    Scores all valid words in a single row/list of characters

        letters (list): list of upercase letters in a row
        key_idx: (int): index of letter required to be in word
        min_len (int): minimum length words to score

    Return:
        score (int): number of points for all found words
    """

    # initialize basic variables
    score = 0
    max_idx = len(letters)
    ltrs_string = "".join(letters)

    for start in range(key_idx + 1):   # loop over possible start indices
        # loop over possible end indices
        for end in range(max(start + min_len, key_idx + 1), max_idx + 1):
            potential_word = ltrs_string[start:end]

            # forward
            if potential_word in self.dict:
                # score per letter in word
                for letter in potential_word:
                    score += self.score_dict[letter]

            # backward
            potential_word = potential_word[::-1]
            if potential_word in self.dict:
                # score per letter in word
                for letter in potential_word:
                    score += self.score_dict[letter]

    return score


def get_words(self, row_idx: int, col_idx: int):
    """
    Scores a move that places a tile

        row_idx (int): an int between 0 and board_height giving the row of the tile for which we want to find words 
        col_idx (int): an int between 0 and board_width giving the col of the tile for which we want to find words 

    Return:
        words (list((string, string))): list of words and their definitions as tuple pairs
    """

    origin = self.board[row_idx][col_idx]
    if origin == "*":
        return 0

    score = 0

    # horizontal words
    start_offset = col_idx
    for i in range(1, start_offset + 1):
        if self.board[row_idx][col_idx - i] == "*":
            start_offset = i - 1
            break

    end_offset = self.width - col_idx
    for i in range(1, end_offset):
        if self.board[row_idx][col_idx + i] == "*":
            end_offset = i - 1
            break

    row = self.board[row_idx][col_idx - start_offset: col_idx + end_offset]
    score += self.search_list(row, start_offset, self.min_word_length)

    # vertical words
    start_offset = row_idx
    for i in range(1, start_offset + 1):
        if self.board[row_idx - i][col_idx] == "*":
            start_offset = i - 1
            break

    end_offset = self.height - row_idx
    for i in range(1, end_offset):
        if self.board[row_idx + i][col_idx] == "*":
            end_offset = i - 1
            break

    col = [self.board[row_idx + row][col_idx]
           for row in range(-start_offset, end_offset)]
    score += self.search_list(col, start_offset, self.min_word_length)

    # up-right words
    start_offset = min(row_idx, col_idx)
    for i in range(1, start_offset + 1):
        if self.board[row_idx - i][col_idx - i] == "*":
            start_offset = i - 1
            break

    end_offset = min(self.height - row_idx, self.width - col_idx)
    for i in range(1, end_offset):
        if self.board[row_idx + i][col_idx + i] == "*":
            end_offset = i - 1
            break

    main_diagonal = [self.board[row_idx + i][col_idx + i]
                     for i in range(-start_offset, end_offset)]
    score += self.search_list(main_diagonal,
                              start_offset, self.min_word_length)

    # up-left words
    start_offset = min(row_idx, self.width - col_idx - 1)
    for i in range(1, start_offset + 1):
        if self.board[row_idx - i][col_idx + i] == "*":
            start_offset = i - 1
            break

    end_offset = min(self.height - row_idx, col_idx + 1)
    for i in range(1, end_offset):
        if self.board[row_idx + i][col_idx - i] == "*":
            end_offset = i - 1
            break

    anti_diagonal = [self.board[row_idx + i][col_idx - i]
                     for i in range(-start_offset, end_offset)]
    score += self.search_list(anti_diagonal,
                              start_offset, self.min_word_length)

    return score
