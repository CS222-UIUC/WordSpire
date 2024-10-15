import pygame #https://www.pygame.org/docs/
import numpy as np
import sys
import math
import string
import os
import Back_end

# Color definitions
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Load tile images
alphabet = list()
tile_images = list()
for letter in string.ascii_lowercase:
    uc_letter = letter.upper()
    alphabet.append(uc_letter)
    file_name = os.path.join(os.path.dirname(__file__), '..', 'misc', 'scrabble_tiles', letter + '.png')
    # Debugging: Print the file name being generated
    print(f"Constructed file path for letter '{letter}': {file_name}")
    
    # Check if the file exists
    if not os.path.exists(file_name):
        print(f"Error: File does not exist at path '{file_name}'")
    else:
        print(f"File exists: {file_name}")
    
    tile_images.append(file_name)
letter_dict = dict(zip(alphabet, tile_images))

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
                tile_image = load_tile_image(board[row][column])
                screen.blit(tile_image, (column * square_size + 10, height - (row + 1) * square_size + 10))
    pygame.display.update()

def display_start_menu():
    # Cover game screen to dispay the menu
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("WordSpire", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (width / 2, height / 2 - 50)
    screen.blit(text, textRect)

    # Create Start button
    button_font = pygame.font.Font('freesansbold.ttf', 28)
    button_text = button_font.render("Start", True, BLACK)
    button_rect = pygame.Rect(width / 2 - 60, height / 2 + 20, 120, 50)
    pygame.draw.rect(screen, GREEN, button_rect)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

    pygame.display.update()
    return button_rect

def display_rack(curr_rack):
    # TO BE FINISHED
    # Currently places a tile in the center of the starting screen

    first_letter = curr_rack[0]
    
    # Get the image path for the letter, handle if not found
    image_path = letter_dict.get(first_letter)
    if image_path is None:
        print(f"Error: No image found for letter '{first_letter}'")
        return

    # Try to load and display the image if the path is valid
    try:
        first_letter_tile = pygame.image.load(image_path)  # Directly load the image using pygame.image.load()
        first_letter_tile = pygame.transform.scale(first_letter_tile, (80, 80))
        screen.blit(first_letter_tile, (width / 2 - 40, height / 2 - 40))
        pygame.display.update()
    except pygame.error as e:
        print(f"Failed to load image for letter '{first_letter}': {e}")

def load_tile_image(curr_letter):
    curr_letter = curr_letter.upper()
    image_path = letter_dict.get(curr_letter)
    if image_path is None:
        print(f"Error: No image found for letter '{curr_letter}'")
        return

    # Try to load and display the image if the path is valid
    try:
        curr_letter_tile = pygame.image.load(image_path)  # Directly load the image using pygame.image.load()
        curr_letter_tile = pygame.transform.scale(curr_letter_tile, (80, 80))
        return curr_letter_tile
    except pygame.error as e:
        print(f"Failed to load image for letter '{curr_letter}': {e}")

# Draw the board
pygame.display.update()
print_board(board)
start_button_rect = display_start_menu()

game_started = False

#check to make sure the game is not over yet 
while (game_over == 0): 
    screen.fill(BLACK)
    for event in pygame.event.get(): #any motion
        # Update board and turn number
        board = curr_game.get_board()
        turn = curr_game.get_turn()

        if event.type == pygame.QUIT: #user can exit if needed
            sys.exit()
        if not game_started:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button_rect.collidepoint(mouse_pos):
                    game_started = True
                    screen.fill(BLACK)
                    draw_board(board)
                    continue
                continue
        if event.type == pygame.MOUSEBUTTONDOWN: #to place pieces
            board = curr_game.get_board()
            turn = curr_game.get_turn()
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
            if game_started:
                draw_board(board)