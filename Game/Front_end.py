import pygame #https://www.pygame.org/docs/
import numpy as np
import sys
import math
import Back_end

# Color definitions
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Create game object and get board info
curr_game = Back_end.Game()
board_list = curr_game.get_board() # gets the current board state, which is a 2D array of strings
board = np.array(board_list)
rack_list = curr_game.get_rack()
rack = np.array(rack_list)
game_over = curr_game.get_game_state()
column_size = 7 #this may be changed
row_size = 7
square_size = 100
width = column_size * square_size #number of columns 
height = (row_size + 1) * square_size #height +1 row for game piece?
size = (width, height) #size of the screen with extra space on top 
turn = curr_game.get_turn()

# Initialize Pygame and display screen
pygame.init()
screen = pygame.display.set_mode(size) #gives the screen size of the game board

def print_board(board):
    print(np.flip(board, 0))

def print_rack(rack):
    print(rack)

def draw_board(board):
    for column in range(column_size):
        for row in range(row_size):
            # Draw board
            pygame.draw.rect(screen, BLUE, (column * square_size, row * square_size + square_size, square_size, square_size))
            # Draw blank slots
            pygame.draw.rect(screen, BLACK, (column * square_size + 10, (row + 1) * square_size + 10, square_size - 20, square_size - 20))
    for column in range(column_size):
        for row in range(row_size):
            if board[row][column] != "*":
                if turn == 0: # Player 1 turn, red
                    pygame.draw.rect(screen, RED, (column * square_size + 10, height - (row + 1) * square_size + 10, square_size - 20, square_size - 20))
                else: # Player 2 turn, yellow
                    pygame.draw.rect(screen, YELLOW, (column * square_size + 10, height - (row + 1) * square_size + 10, square_size - 20, square_size - 20))
    pygame.display.update()

# Draw the board
draw_board(board)
pygame.display.update()
print_board(board)

#check to make sure the game is not over yet 
while (game_over == 0): 
    for event in pygame.event.get(): #any motion
        # Update board and turn number
        board = curr_game.get_board()
        turn = curr_game.get_turn()

        if event.type == pygame.QUIT: #user can exit if needed
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN: #to place pieces
            # Ask for Player 1 input
            if turn == 0:
                # letter_idx = int(input("Player 1, choose a letter index from your rack (0-6): ")) # Will change to select input from list of options
                letter_idx = 0 # REMINDER: Temporary placeholder
                x_pos = event.pos[0]
                column = int(x_pos // square_size)
                curr_game.place_piece(letter_idx, column) ## QUESTION: How will players differentiate their letter tiles from the other player's?
            

            # Ask for Player 2 input
            else:
                # letter_idx = int(input("Player 2, choose a letter index from your rack (0-6): ")) # Will change to select input from list of options
                letter_idx = 0 # REMINDER: Temporary placeholder
                x_pos = event.pos[0]
                column = int(x_pos // square_size)
                curr_game.place_piece(letter_idx, column)

            print_board(board)
            draw_board(board)