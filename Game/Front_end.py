import pygame #https://www.pygame.org/docs/
import numpy as np
import sys
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
DARK_BROWN = (92, 64, 51)
DARK_GRAY = (83, 83, 83)
LIGHT_GRAY = (105, 105, 105)

# Load tile images
alphabet = list()
tile_images = list()
for letter in string.ascii_lowercase:
    uc_letter = letter.upper()
    alphabet.append(uc_letter)
    file_name = os.path.join(os.path.dirname(__file__), 'misc', 'scrabble_tiles', letter + '.png')
    
    # Check if the file exists
    if not os.path.exists(file_name):
        print(f"Error: File does not exist at path '{file_name}'")
    
    tile_images.append(file_name)
letter_dict = dict(zip(alphabet, tile_images)) # Dictionary mapping letters to their tile_image pathnames

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
    """
    Prints the current board state (used for debugging and proof-of-concept)

    """
    print(np.flip(board, 0))

def print_rack(rack):
    """
    Prints the current rack state (used for debugging and proof-of-concept)

    """
    print(rack)

def draw_board(board):
    """
    Function to draw the board

    """
    for column in range(column_size):
        for row in range(row_size):
            # Draw board
            pygame.draw.rect(screen, DARK_BROWN, (column * square_size, row * square_size + square_size, square_size, square_size))
            # Draw blank slots
            pygame.draw.rect(screen, BLACK, (column * square_size + 10, (row + 1) * square_size + 10, square_size - 20, square_size - 20))
    for column in range(column_size):
        for row in range(row_size):
            if board[row][column] != "*":
                tile_image = load_tile_image(board[row][column])
                screen.blit(tile_image, (column * square_size + 10, height - (row + 1) * square_size + 10))
    pygame.display.update()

def display_start_menu():
    """
    Function to display the start menu

    Return:
        start_button_rect (pygame.rect.Rect): pygame object representing the "Start" text button box
    """
    
    # Create title text
    font = pygame.font.Font('freesansbold.ttf', 48)
    text = font.render("WordSpire", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (width / 2, height / 2 - 50)
    screen.blit(text, textRect)

    # Create Start button
    start_button_center = (width / 2 - 60, height / 2 + 20)
    start_button_rect = create_text_button(start_button_center, message = "Start")

    pygame.display.update()
    return start_button_rect

def display_rack(curr_rack, selected=False):
    """
    Function to display rack screen, including player turn, rack tiles, two buttons, and scores

        curr_rack (list): Array of strings representing the rack
        selected (bool): Boolean stating whether a tile has been selected (Default is False)

    Return:
        rack_menu_buttons (list): Array of pygame.rect.Rect objects for text buttons and
                                  tuples containing (image button, rack index)
    """
    # Returns a list of buttons starting with 'View Board', then 'Select Tile', then the letter tiles

    # Display player turn
    font = pygame.font.Font('freesansbold.ttf', 48)
    if curr_game.get_turn():
        text = font.render("Player 2's Turn", True, WHITE)
    else:
        text = font.render("Player 1's Turn", True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, 200)
    screen.blit(text, text_rect)

    # Display player score
    font = pygame.font.Font('freesansbold.ttf', 24)
    p1_score, p2_score = curr_game.get_scores()
    p1_msg = "Player 1 Score: " + str(p1_score)
    p2_msg = "Player 2 Score: " + str(p2_score)
    p1_text = font.render(p1_msg, True, WHITE)
    p2_text = font.render(p2_msg, True, WHITE)
    p1_rect = p1_text.get_rect()
    p2_rect = p2_text.get_rect()
    p1_rect.center = (width / 4 - 50, height - 30)
    p2_rect.center = (3 * width / 4 + 50, height - 30)
    screen.blit(p1_text, p1_rect)
    screen.blit(p2_text, p2_rect)

    rack_menu_buttons = []

    # Display a button that allows you to go back to board
    view_board_button_center = (width / 2 - 60, height / 2 + 200)
    view_board_button_rect = create_text_button(view_board_button_center, "View Board", 16)
    rack_menu_buttons.append(view_board_button_rect)

    # Display a 'Select Tile' button
    if not selected:
        place_button_center = (width / 2 - 60, height / 2 + 120)
        place_button_rect = create_text_button(place_button_center, "Select Tile", 16, DARK_GRAY, LIGHT_GRAY)
        rack_menu_buttons.append(place_button_rect)
    else:
        place_button_center = (width / 2 - 60, height / 2 + 120)
        place_button_rect = create_text_button(place_button_center, "Select Tile", 16)
        rack_menu_buttons.append(place_button_rect)

    # Load and display images for tiles
    for i, letter in enumerate(curr_rack):
        tile_image = load_tile_image(letter)
        tile_rect = tile_image.get_rect(topleft=(i * 100 + 10, height / 2 - 40))  # Adjust position as needed
        screen.blit(tile_image, tile_rect)
        rack_menu_buttons.append((tile_rect, i))  # Store the rect with the index

    pygame.display.update()
    return rack_menu_buttons

def load_tile_image(curr_letter):
    """
    Function to load a tile image path

        curr_letter (string): Letter for the tile image to load
    """
    # Get image path
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

def display_pause_menu():
    """
    Function to display the pause menu

    Return:
        resume_button_rect (pygame.rect.Rect): pygame object representing the "Resume" text button box
        options_button_rect (pygame.rect.Rect): pygame object representing the "Options" text button box
    """
    # Display Pause Menu
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("Game Paused", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (width / 2, height / 2 - 100)
    screen.blit(text, textRect)

    # Create Resume button
    resume_button_center = (width / 2 - 60, height / 2)
    resume_button_rect = create_text_button(resume_button_center, "Resume", 26)

    # Create Options button
    options_button_center = (width / 2 - 60, height / 2 + 70)
    options_button_rect = create_text_button(options_button_center, "Options", 26)

    pygame.display.update()
    return resume_button_rect, options_button_rect

def create_text_button(location, message="", font_size=28, text_color=BLACK, button_color=GREEN, size=(120, 50)):
    """
    Function that creates and returns a text button object

        location (tuple[int, int]): x and y location for the center of the button, defined from top left corner
        message (string): string message to be displayed inside the button
        font_size (int): 
        text_color (tuple[int, int, int]): takes a pre-determined color for the button's text
        button_color (tuple[int, int, int]): takes a pre-determined color for the button itself

    Return:
        button_rect (pygame.rect.Rect): pygame object representing the text button created
    """
    # Define center for the button
    x = location[0]
    y = location[1]

    # Create button object
    button_font = pygame.font.Font('freesansbold.ttf', font_size)
    button_text = button_font.render(message, True, text_color)
    button_rect = pygame.Rect(x, y, size[0], size[1])
    pygame.draw.rect(screen, button_color, button_rect, width=0, border_radius=10)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    return button_rect

def display_error_message(message):
    """
    Function to display a pop-up box that will tell the player the error message for their disallowed
    or undefined behavior

        message (str): string representation of error message to display

    Return:
        x_button_rect (pygame.rect.Rect): pygame object representing the "X" text button box to exit pop-up
    """

    # Define the dimensions for the error menu pop-up
    menu_width = width * 0.6  # Adjusted width for longer messages
    menu_height = height * 0.4  # Adjusted height
    menu_x = (width - menu_width) / 2
    menu_y = (height - menu_height) / 2
    error_menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)

    # Draw the error menu with rounded corners
    pygame.draw.rect(screen, DARK_GRAY, error_menu_rect, width=0, border_radius=10)

    # Display the error message with word wrapping
    font = pygame.font.Font('freesansbold.ttf', 24)  # Adjust font size if needed
    words = message.split()
    lines = []
    current_line = ""

    # Word wrapping logic
    for word in words:
        # Check if adding the next word exceeds the menu width
        if font.size(current_line + word)[0] < (menu_width - 40):  # 40px padding
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())

    # Render each line of text, starting lower in the pop-up
    start_y = menu_y + 120  # Adjusted starting Y position (increased to be lower)
    for i, line in enumerate(lines):
        error_text = font.render(line, True, WHITE)
        error_text_rect = error_text.get_rect(center=(menu_x + menu_width / 2, start_y + i * 30))  # 30px line spacing
        screen.blit(error_text, error_text_rect)

    # Create a close button ("X") in the top right of the pop-up
    close_button_center = (menu_x + menu_width / 2 + 150, menu_y + 10)
    x_button_rect = create_text_button(close_button_center, "X", font_size=24, text_color=WHITE, button_color=RED, size=(50, 50))

    # Update the display to show the pop-up and the close button
    pygame.display.update()

    return x_button_rect

def display_tile_definitions(col_idx, row_idx, word_idx = 0):
    """
    Function to display the term(s) and definition(s), if any, for the given tile

        row (int): index from 0-6 representing the row from left to right
        column (int): index from 0-6 representing 

    Return:
        buttons (List): List containing an x_button_rect if there's no word or one word
                        and a left_button_rect and right_button_rect, as well as the word_idx
    """

    buttons = []
    tile_info = curr_game.get_words(col_idx, row_idx)
    num_words = len(tile_info)

    menu_width = width * 0.6  # Adjusted width for longer messages
    menu_height = height * 0.6  # Adjusted height
    menu_x = (width - menu_width) / 2
    menu_y = (height - menu_height) / 2
    words_menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)

    pygame.draw.rect(screen, DARK_GRAY, words_menu_rect, width=0, border_radius=10)

    close_button_center = (menu_x + menu_width / 2 + 150, menu_y + 10)
    x_button_rect = create_text_button(close_button_center, "X", font_size=24, text_color=WHITE, button_color=RED, size=(50, 50))
    buttons.append(x_button_rect)

    # Create pop-up of words with definitions over the current screen
    words = []
    scores = []
    definitions = []
    for entry in tile_info:
        words.append(entry[0])
        scores.append(entry[1])
        definitions.append(entry[2])
    if num_words == 0:
        box_message = "No words made at this tile"
        font = pygame.font.Font('freesansbold.ttf', 24)
        words_text = font.render(box_message, True, LIGHT_GRAY)
        words_text_rect = words_text.get_rect(center=words_menu_rect.center)
        screen.blit(words_text, words_text_rect)
    else:
        # Display the error message with word wrapping
        word_text = words[word_idx]
        word_text = word_text + " (" + str(scores[word_idx]) + " points)"
        definition_text = definitions[word_idx]
        font = pygame.font.Font('freesansbold.ttf', 24)  # Adjust font size if needed
        lines_words = definition_text.split()
        lines = []
        current_line = ""
        font = pygame.font.Font('freesansbold.ttf', 24)
        word_text = font.render(word_text, True, WHITE)
        word_text_rect = word_text.get_rect(center=(menu_x + 200, menu_y + 100))
        screen.blit(word_text, word_text_rect)
        lines = []
        current_line = ""
        # Improved word wrapping that avoids splitting words in the middle
        for word in lines_words:
            # Check if adding the word to the current line would exceed the width
            if font.size(current_line + word + " ")[0] <= (menu_width - 40):  # 40px padding
                current_line += word + " "  # Add the word with a space
            else:
                # Append the current line to lines and start a new line with the word
                lines.append(current_line.strip())
                current_line = word + " "
        # Append any remaining text in the last line
        if current_line:
            lines.append(current_line.strip())
        # Render each line of text with left alignment
        start_y = menu_y + 140  # Adjusted starting Y position
        for i, line in enumerate(lines):
            def_text = font.render(line, True, WHITE)
            def_text_rect = def_text.get_rect(center=(menu_x + menu_width / 2, start_y + i * 30))  # 20px padding from the left
            screen.blit(def_text, def_text_rect)
        if num_words > 1:
            left_button_color = LIGHT_GRAY
            left_text_color = DARK_GRAY
            right_button_color = LIGHT_GRAY
            right_text_color = DARK_GRAY
            if word_idx > 0:
                left_button_color = GREEN
                left_text_color = BLACK
            if word_idx < num_words - 1:
                right_button_color = GREEN
                right_text_color = BLACK
            left_button_center = (menu_x + 10, menu_y + menu_height - 60)
            right_button_center = (menu_x + menu_width / 2 + 150, menu_y + menu_height - 60)
            left_button_rect = create_text_button(left_button_center, "<", text_color=left_text_color, button_color=left_button_color, size=(50, 50))
            right_button_rect = create_text_button(right_button_center, ">", text_color=right_text_color, button_color=right_button_color, size=(50, 50))
            buttons.append(left_button_rect)
            buttons.append(right_button_rect)
            buttons.append(num_words)
    pygame.display.update()
    return buttons

def display_game_over(game_state):
    """
    Game over function; displays the winning player, a game over message, and an option to restart or quit

        game_state (int): current state of the game; 0 if game is not over, 1 if player 1 wins, 2 if player 2 wins, 3 if tie

    Return:
        restart_button_rect (pygame.rect.Rect): pygame object representing the "Restart" text button box
        quit_button_rect (pygame.rect.Rect): pygame object representing the "Quit" text button box
    """
    if game_state == 0:
        return 0
    
    font = pygame.font.Font('freesansbold.ttf', 48)
    text = font.render("Game Over", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (width / 2, height / 2 - 50)
    screen.blit(text, textRect)

    winning_player = str(game_state)
    winning_text = "Player " + winning_player + " won!"
    if game_state == 1:
        color = BLUE
    elif game_state == 2:
        color = RED
    else:
        color = GREEN
        winning_text = "It's a tie!"
    font = pygame.font.Font('freesansbold.ttf', 50)
    text = font.render(winning_text, True, color)
    textRect = text.get_rect()
    textRect.center = (width / 2, 75)
    screen.blit(text, textRect)

    restart_button_center = (width / 2 - 60, height / 2 + 20)
    restart_button_rect = create_text_button(restart_button_center, message = "Restart")

    quit_button_center = (width / 2 - 60, height / 2 + 100)
    quit_button_rect = create_text_button(quit_button_center, message = "Quit")

    pygame.display.update()

    return restart_button_rect, quit_button_rect


# Draw the board
pygame.display.update()
print_board(board)
start_button_rect = display_start_menu()

game_started = False
paused = False
showing_rack = False
selected = False
selected_idx = -1
tmp_selected = False
tmp_selected_idx = -1
error_message = ""
error_message_drawn = False
displaying_words = False
displaying_words_menu = False
col_idx = -1
row_idx = -1
word_idx = 0

#check to make sure the game is not over yet 
while True:
    game_over = curr_game.get_game_state()
    board = curr_game.get_board()
    turn = curr_game.get_turn()
    for event in pygame.event.get(): #any motion
        # Update board and turn number
        if event.type == pygame.QUIT: #user can exit if needed
            sys.exit()
        if not game_started:  # Display starting menu
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if start_button_rect.collidepoint(mouse_pos):
                    game_started = True
                    screen.fill(BLACK)
                    draw_board(board)
                    continue
                continue
        if game_over > 0:
            restart_button_rect, quit_button_rect = display_game_over(game_over)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if restart_button_rect.collidepoint(mouse_pos):
                    curr_game = Back_end.Game()
                    board_list = curr_game.get_board() # gets the current board state, which is a 2D array of strings
                    board = np.array(board_list)
                    rack_list = curr_game.get_rack()
                    rack = np.array(rack_list)
                    game_over = curr_game.get_game_state()
                    turn = curr_game.get_turn()
                    game_started = False
                    screen.fill(BLACK)
                    start_button_rect = display_start_menu()
                elif quit_button_rect.collidepoint(mouse_pos):
                    sys.exit()
                else:
                    continue
        if displaying_words:
            if not displaying_words_menu:
                draw_board(board)
                buttons = display_tile_definitions(col_idx, row_idx, word_idx)
                x_button_rect = buttons[0]
                if len(buttons) > 1:
                    left_button_rect = buttons[1]
                    right_button_rect = buttons[2]
                    num_words = buttons[3]
            displaying_words_menu = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if x_button_rect.collidepoint(mouse_pos):
                    word_idx = 0
                    displaying_words = False
                    displaying_words_menu = False
                    draw_board(board)
                    continue
                if len(buttons) > 1:
                    if left_button_rect.collidepoint(mouse_pos):
                        if word_idx > 0:
                            word_idx -= 1
                            buttons = display_tile_definitions(col_idx, row_idx, word_idx)
                    if right_button_rect.collidepoint(mouse_pos):
                        if word_idx < num_words - 1:
                            word_idx += 1
                            buttons = display_tile_definitions(col_idx, row_idx, word_idx)
                    continue
            else:
                continue
        if error_message != "":
            if not error_message_drawn:
                draw_board(board)
                x_button_rect = display_error_message(error_message)
            error_message_drawn = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if x_button_rect.collidepoint(mouse_pos):
                    error_message = ""
                    error_message_drawn = False
                    draw_board(board)
                    continue
            else:
                continue
        if game_started and event.type == pygame.KEYDOWN:  # Go into pause menu
            if event.key == pygame.K_p:
                screen.fill(BLACK)
                paused = True
                resume_button_rect, options_button_rect = display_pause_menu()
            elif event.key == pygame.K_r:
                screen.fill(BLACK)
                showing_rack = True
                rack = curr_game.get_rack()
                rack_menu_buttons = display_rack(rack, selected)
                view_board_button_rect = rack_menu_buttons[0]
                select_button_rect = rack_menu_buttons[1]
        if paused:  # Display pause menu
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if resume_button_rect.collidepoint(mouse_pos):
                        paused = False
                        draw_board(board)
                        continue
                    elif options_button_rect.collidepoint(mouse_pos):
                        # Do nothing for now when player presses the 'Options' button
                        pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                    draw_board(board)
                    continue
        if showing_rack:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    for i in range(2, len(rack_menu_buttons)):  # Start from index 2 to skip 'View Board' and 'Select Tile'
                        tile_button_rect, rack_idx = rack_menu_buttons[i]
                        if tile_button_rect.collidepoint(mouse_pos):
                            tmp_selected = True
                            tmp_selected_idx = rack_idx
                            rack_menu_buttons = display_rack(rack, tmp_selected)
                            continue
                    if view_board_button_rect.collidepoint(mouse_pos):
                        showing_rack = False
                        draw_board(board)
                        continue
                    elif tmp_selected and select_button_rect.collidepoint(mouse_pos):
                        selected = tmp_selected
                        selected_idx = tmp_selected_idx
                        tmp_selected = False
                        tmp_selected_idx = -1
                        showing_rack = False
                        draw_board(board)
                        continue
                    else:
                        selected_idx = -1
                        continue
        if not displaying_words and not paused and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board = curr_game.get_board()
                turn = curr_game.get_turn()
                if selected:
                    # Ask for Player 1 input
                    if turn == 0:
                        x_pos = event.pos[0]
                        column = int(x_pos // square_size)
                        placed_piece = curr_game.place_piece(selected_idx, column)
                        if placed_piece == 1:
                            error_message = "Column is full! Please place tile in a different column."
                            display_error_message(error_message)

                    # Ask for Player 2 input
                    else:
                        x_pos = event.pos[0]
                        column = int(x_pos // square_size)
                        placed_piece = curr_game.place_piece(selected_idx, column)
                        if placed_piece == 1:
                            error_message = "Column is full! Please place tile in a different column."
                            display_error_message(error_message)
                    selected_idx = -1
                    selected = False
                    print_board(board)
                    if game_started:
                        draw_board(board)
                else:
                    x_pos = event.pos[0]
                    y_pos = event.pos[1]
                    col_idx = int(x_pos // square_size)
                    row_idx = int(y_pos // square_size)
                    row_idx -= 1
                    if row_idx >= 0:
                        displaying_words = True
                    else:
                        continue
                    row_idx = 6 - row_idx
                    x_button_rect = display_tile_definitions(col_idx, row_idx)