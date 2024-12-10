import pygame #https://www.pygame.org/docs/
import numpy as np
import sys
import string
import os
import time
import Back_end

# Color definitions
BLUE = (65, 105, 225)
ROYAL_BLUE = (36, 114, 240)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DUSTY_RED = (185, 72, 78)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GRAY = (83, 83, 83)
DARKER_GRAY = (40, 40, 40)
LIGHT_GRAY = (105, 105, 105)
PURPLE = (91, 17, 102)
YELLOW = (254, 221, 86)
OFF_WHITE = (237, 237, 237)
BEIGE = (234, 220, 201)
MAROON = (101, 0, 6)
MAHOGANY = (46, 25, 20)

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

# Load audio files
tile_drop_sound = os.path.join(os.path.dirname(__file__), 'misc', 'sounds', 'click.mp3')
winner_sound = os.path.join(os.path.dirname(__file__), 'misc', 'sounds', 'winner.mp3')
score_point_sound = os.path.join(os.path.dirname(__file__), 'misc', 'sounds', 'score.mp3')
button_press_sound = os.path.join(os.path.dirname(__file__), 'misc', 'sounds', 'button_press.mp3')
error_sound = os.path.join(os.path.dirname(__file__), 'misc', 'sounds', 'error.mp3')

single_leaderboard_path = os.path.join(os.path.dirname(__file__), 'singleplayer_leaderboard.txt')
multi_leaderboard_path = os.path.join(os.path.dirname(__file__), 'multiplayer_leaderboard.txt')

# Get board info
column_size = 7
row_size = 7
square_size = 100
width = column_size * square_size #number of columns 
height = (row_size + 1) * square_size #height +1 row for game piece?
size = (width, height) #size of the screen with extra space on top 

scr_color = DARKER_GRAY
txt_color = WHITE
bttn_color = GREEN
bttn_txt_color = BLACK
board_color = MAHOGANY

# Initialize Pygame and display screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(size) # Gives the screen size of the game board
pygame.display.set_caption('WordSpire') # Set name of the window
image_path = letter_dict.get('W')
icon = pygame.image.load(image_path)
pygame.display.set_icon(icon)

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
    screen.fill(scr_color)
    for column in range(column_size):
        for row in range(row_size):
            # Draw board
            pygame.draw.rect(screen, MAHOGANY, (column * square_size, row * square_size + square_size, square_size, square_size))
            # Draw blank slots
            pygame.draw.rect(screen, MAROON, (column * square_size + 10, (row + 1) * square_size + 10, square_size - 20, square_size - 20))
    for column in range(column_size):
        for row in range(row_size):
            if board[row][column] != "*":
                tile_image = load_tile_image(board[row][column])
                screen.blit(tile_image, (column * square_size + 10, height - (row + 1) * square_size + 10))
    pygame.display.update()

def add_to_leaderboard(name, new_score):
    leaderboard_path = ""
    leaderboard_path = single_leaderboard_path if num_players == 1 else multi_leaderboard_path
    lines = []
    new_entry = False
    with open(leaderboard_path, "r") as f:
        old = f.read() # read everything in the file
        lines = old.split("\n")
        if len(lines) == 1 and lines[0] == "":
            lines = [f"{name}: {new_score}"]
            new_entry = True
        else:
            for i in range(10):
                if i < len(lines):
                    if lines[i] != "":
                        curr_score = int(lines[i].split(":")[1][1:])
                        if new_score > curr_score:
                            lines.insert(i, f"{name}: {new_score}")
                            new_entry = True
                            break
                    else:
                        lines.insert(i, f"{name}: {new_score}")
                        new_entry = True
                        break
                else:
                    lines.append(f"{name}: {new_score}")
                    new_entry = True
                    break
            while len(lines) > 10:
                lines.pop()
    file = open(leaderboard_path, "w")
    for i in range(len(lines)):
        if i < len(lines) - 1:
            file.write(lines[i] + '\n')
        else:
            file.write(lines[i])
    file.close()
    return new_entry

def get_leaderboard_data():
    leaderboard_path = ""
    leaderboard_path = single_leaderboard_path if num_players == 1 else multi_leaderboard_path
    leaderboard_data = []
    with open(leaderboard_path, "r") as f:
        data = f.read()
        lines = data.split("\n")
        for line in lines:
            if line != "":
                line_data = line.split(":")
                name = line_data[0]
                score = line_data[1][1:]
                leaderboard_data.append((name, score))
    return leaderboard_data

def display_pop_up(dimensions, text_list, buttons_list):
    """
    Displays a pop-up menu on the screen with the given dimensions and text and buttons to include

        dimensions (tuple[int, int]): the width and height of the menu as a tuple
        text_list (list): list containing tuples of information about all text boxes to include
        buttons_list (list): list containing tuples of information about all buttons to create
    
    Return:
        buttons (list): list of pygame.rect.Rect that represent the text buttons
    """
    menu_width = dimensions[0]
    menu_height = dimensions[1]
    menu_x = (width - menu_width) / 2
    menu_y = (height - menu_height) / 2
    popup_menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
    pygame.draw.rect(screen, DARK_GRAY, popup_menu_rect, width=0, border_radius=10)

    for text_tuple in text_list:
        message = text_tuple[0]
        color = text_tuple[1]
        center_coords = text_tuple[2]
        y_offset = text_tuple[3]
        spacing = text_tuple[4]
        font_size = text_tuple[5]

        font = pygame.font.Font('freesansbold.ttf', font_size)  # Adjust font size if needed
        words = message.split()
        lines = []
        current_line = ""

        if y_offset == 0:
            word_text = font.render(message, True, color)
            word_text_rect = word_text.get_rect(center=center_coords)
            screen.blit(word_text, word_text_rect)
        
        else:
            lines_words = message.split()
            lines = []
            current_line = ""
            # Improved word wrapping that avoids splitting words in the middle
            for word in lines_words:
                # Check if adding the word to the current line would exceed the width
                if font.size(current_line + word + spacing)[0] <= (menu_width - 40):  # 40px padding
                    current_line += word + spacing  # Add the word with a space
                else:
                    # Append the current line to lines and start a new line with the word
                    lines.append(current_line.strip())
                    current_line = word + spacing
            # Append any remaining text in the last line
            if current_line:
                lines.append(current_line.strip())
            # Render each line of text with left alignment
            start_y = menu_y + y_offset  # Adjusted starting Y position
            for i, line in enumerate(lines):
                message_text = font.render(line, True, color)
                message_text_rect = message_text.get_rect(center=(menu_x + menu_width / 2, start_y + i * 30))  # 20px padding from the left
                screen.blit(message_text, message_text_rect)

    buttons = []

    for button_tuple in buttons_list:
        center = button_tuple[0]
        text = button_tuple[1]
        font_size = button_tuple[2]
        text_color = button_tuple[3]
        button_color = button_tuple[4]
        size = button_tuple[5]
        button = create_text_button(center, text, font_size=font_size, text_color=text_color, button_color=button_color, size=size)
        buttons.append(button)

    return buttons

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

def display_rack(curr_rack, selected_idx):
    """
    Function to display rack screen, including player turn, rack tiles, two buttons, and scores

        curr_rack (list): Array of strings representing the rack
        selected (bool): Boolean stating whether a tile has been selected (Default is False)

    Return:
        rack_menu_buttons (list): Array of pygame.rect.Rect objects for text buttons and
                                  tuples containing (image button, rack index)
    """
    screen.fill(scr_color)
    curr_rack = curr_game.get_rack()
    # Display player turn
    font = pygame.font.Font('freesansbold.ttf', 48)
    if curr_game.get_turn():
        text = font.render("Player 2's Turn", True, txt_color)
    else:
        text = font.render("Player 1's Turn", True, txt_color)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, 200)
    screen.blit(text, text_rect)

    # Display player score
    font = pygame.font.Font('freesansbold.ttf', 24)
    p1_score, p2_score = curr_game.get_scores()
    p1_msg = "Player 1 Score: " + str(p1_score)
    p2_msg = "Player 2 Score: " + str(p2_score)
    if p1_points_gained > 0:
        p1_pts_gained_txt = font.render(f"+{p1_points_gained}", True, BLUE)
        p1_pts_rect = p1_pts_gained_txt.get_rect()
        p1_pts_rect.center = (width / 4 + 33, height - 60)
        screen.blit(p1_pts_gained_txt, p1_pts_rect)
    if p2_points_gained > 0:
        p2_pts_gained_txt = font.render(f"+{p2_points_gained}", True, DUSTY_RED)
        p2_pts_rect = p2_pts_gained_txt.get_rect()
        p2_pts_rect.center = (3 * width / 4 + 133, height - 60)
        screen.blit(p2_pts_gained_txt, p2_pts_rect)
    p1_text = font.render(p1_msg, True, txt_color)
    p2_text = font.render(p2_msg, True, txt_color)
    p1_rect = p1_text.get_rect()
    p2_rect = p2_text.get_rect()
    p1_rect.center = (width / 4 - 50, height - 30)
    p2_rect.center = (3 * width / 4 + 50, height - 30)
    screen.blit(p1_text, p1_rect)
    screen.blit(p2_text, p2_rect)

    rack_menu_buttons = []

    # Display a button that allows you to go back to board
    view_board_button_center = (width / 2 - 60, height / 2 + 200)
    view_board_button_rect = create_text_button(view_board_button_center, "View Board", 16, text_color = bttn_txt_color, button_color = bttn_color)
    rack_menu_buttons.append(view_board_button_rect)

    # Display a 'Select Tile' button
    place_button_center = (width / 2 - 60, height / 2 + 120)
    if selected_idx < 0:
        selected_msg = "No tile selected"
        place_button_rect = create_text_button(place_button_center, "Select Tile", 16, DARK_GRAY, LIGHT_GRAY)
        rack_menu_buttons.append(place_button_rect)
    else:
        selected_msg = "Selected tile: " + str(curr_rack[selected_idx])
        place_button_rect = create_text_button(place_button_center, "Select Tile", 16, text_color = bttn_txt_color, button_color = bttn_color)
        rack_menu_buttons.append(place_button_rect)

    selected_text = font.render(selected_msg, True, txt_color)
    selected_rect = selected_text.get_rect()
    selected_rect.center = (width / 2, height / 2 + 80)
    screen.blit(selected_text, selected_rect)

    rack_background_rect = pygame.Rect(0, height / 2 - 70, width, 120)
    pygame.draw.rect(screen, MAHOGANY, rack_background_rect)
    shadow_rect = pygame.Rect(0, height / 2 + 30, width, 6)
    pygame.draw.rect(screen, BLACK, shadow_rect)
    shadow_2_rect = pygame.Rect(0, height / 2 + 47, width, 3)
    pygame.draw.rect(screen, BLACK, shadow_2_rect)

    # Load and display images for tiles
    for i, letter in enumerate(curr_rack):
        y_pos = height / 2 - 60
        if i == selected_idx:
            y_pos -= 40
        tile_image = load_tile_image(letter)
        tile_rect = tile_image.get_rect(topleft=(i * 100 + 10, y_pos))  # Adjust position as needed
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
    screen.fill(scr_color)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("Game Paused", True, txt_color)
    textRect = text.get_rect()
    textRect.center = (width / 2, height / 2 - 100)
    screen.blit(text, textRect)

    # Create Resume button
    resume_button_center = (width / 2 - 60, height / 2)
    resume_button_rect = create_text_button(resume_button_center, "Resume", 26, text_color = bttn_txt_color, button_color = bttn_color)

    # Create Options button
    options_button_center = (width / 2 - 60, height / 2 + 70)
    options_button_rect = create_text_button(options_button_center, "Options", 26, text_color = bttn_txt_color, button_color = bttn_color)

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

        message (string): string representation of error message to display

    Return:
        x_button_rect (pygame.rect.Rect): pygame object representing the "X" text button box to exit pop-up
    """

    # Define the dimensions for the error menu pop-up
    menu_width = width * 0.6  # Adjusted width for longer messages
    menu_height = height * 0.4  # Adjusted height
    menu_x = (width - menu_width) / 2
    menu_y = (height - menu_height) / 2
    dimensions = (menu_width, menu_height)
    y_offset = 120
    text_tuple = (message, WHITE, (0, 0), y_offset, ' ', 24)
    text_list = [text_tuple]

    # Create a close button ("X") in the top right of the pop-up
    close_button_center = (menu_x + menu_width / 2 + 150, menu_y + 10)
    close_button_tuple = (close_button_center, "X", 24, WHITE, RED, (50, 50))
    buttons_list = [close_button_tuple]

    buttons = display_pop_up(dimensions, text_list, buttons_list)

    # Update the display to show the pop-up and the close button
    pygame.display.update()

    return buttons[0]

def display_tile_definitions(col_idx, row_idx, word_idx = 0):
    """
    Function to display the term(s) and definition(s), if any, for the given tile

        row (int): index from 0-6 representing the row from left to right
        column (int): index from 0-6 representing 

    Return:
        buttons (List): List containing an x_button_rect if there's no word or one word
                        and a left_button_rect and right_button_rect, as well as the word_idx
    """

    tile_info = curr_game.get_words(col_idx, row_idx)
    num_words = len(tile_info)

    menu_width = width * 0.6  # Adjusted width for longer messages
    menu_height = height * 0.6  # Adjusted height
    menu_x = (width - menu_width) / 2
    menu_y = (height - menu_height) / 2
    dimensions = (menu_width, menu_height)

    close_button_center = (menu_x + menu_width / 2 + 150, menu_y + 10)
    close_button_tuple = (close_button_center, "X", 24, WHITE, RED, (50, 50))
    buttons_list = [close_button_tuple]

    # Create pop-up of words with definitions over the current screen
    words = []
    scores = []
    definitions = []
    text_list = []
    for entry in tile_info:
        words.append(entry[0])
        scores.append(entry[1])
        definitions.append(entry[2])
    if num_words == 0:
        box_message = "No words made at this tile"
        box_text_tuple = (box_message, LIGHT_GRAY, (width / 2, height / 2), 0, ' ', 24)
        text_list.append(box_text_tuple)
    else:
        word_text = f"{words[word_idx]} ({str(scores[word_idx])} points)"
        word_text_tuple = (word_text, WHITE, (menu_x + 200, menu_y + 100), 0, ' ', 24)
        text_list.append(word_text_tuple)

        definition_text = definitions[word_idx]
        definition_text_tuple = (definition_text, WHITE, (0, 0), 140, ' ', 24)
        text_list.append(definition_text_tuple)
        
        if num_words > 1:
            left_button_color = GREEN if word_idx > 0 else LIGHT_GRAY
            left_text_color = BLACK if word_idx > 0 else DARK_GRAY
            right_button_color = GREEN if word_idx < num_words - 1 else LIGHT_GRAY
            right_text_color = BLACK if word_idx < num_words - 1 else DARK_GRAY
            left_button_center = (menu_x + 10, menu_y + menu_height - 60)
            right_button_center = (menu_x + menu_width / 2 + 150, menu_y + menu_height - 60)
            left_button_tuple = (left_button_center, "<", 24, left_text_color, left_button_color, (50, 50))
            buttons_list.append(left_button_tuple)
            right_button_tuple = (right_button_center, ">", 24, right_text_color, right_button_color, (50, 50))
            buttons_list.append(right_button_tuple)
    buttons = display_pop_up(dimensions, text_list, buttons_list)
    if num_words > 1:
        buttons.append(num_words)
    pygame.display.update()
    return buttons

def display_game_over(game_state, sound_played, leaderboard_updated):
    """
    Game over function; displays the winning player, a game over message, and an option to restart or quit

        game_state (int): current state of the game; 0 if game is not over, 1 if player 1 wins, 2 if player 2 wins, 3 if tie
        sound_played (bool): Whether the end-of-game sound has played already
        leaderboard_updated (bool): Tells whether the leaderboard has been updated this game

    Return:
        restart_button_rect (pygame.rect.Rect): pygame object representing the "Restart" text button box
        quit_button_rect (pygame.rect.Rect): pygame object representing the "Quit" text button box
    """
    if game_state == 0:
        return 0
    
    screen.fill(scr_color)

    font = pygame.font.Font('freesansbold.ttf', 48)
    text = font.render("Game Over", True, txt_color)
    textRect = text.get_rect()
    textRect.center = (width / 2, height / 2 - 50)
    screen.blit(text, textRect)

    if leaderboard_updated:
        font = pygame.font.Font('freesansbold.ttf', 20)
        color = LIGHT_GRAY if mode == "dark" else WHITE
        text = font.render("Leaderboard has been updated!", True, color)
        textRect = text.get_rect()
        textRect.center = (width / 2, height - 25)
        screen.blit(text, textRect)

    winning_player = str(game_state)
    winning_text = "Player " + winning_player + " won!"
    if game_state == 1:
        color = BLUE
        if not sound_played:
            sound = pygame.mixer.Sound(winner_sound)
            sound.play()
    elif game_state == 2:
        color = DUSTY_RED
        if not sound_played:
            sound = pygame.mixer.Sound(winner_sound)
            sound.play()
    else:
        color = GREEN
        winning_text = "It's a tie!"
    font = pygame.font.Font('freesansbold.ttf', 50)
    text = font.render(winning_text, True, color)
    textRect = text.get_rect()
    textRect.center = (width / 2, 75)
    screen.blit(text, textRect)

    restart_button_center = (width / 2 - 60, height / 2 + 20)
    restart_button_rect = create_text_button(restart_button_center, message = "Restart", text_color = bttn_txt_color, button_color = bttn_color)

    quit_button_center = (width / 2 - 60, height / 2 + 100)
    quit_button_rect = create_text_button(quit_button_center, message = "Quit", text_color = bttn_txt_color, button_color = bttn_color)

    pygame.display.update()

    return restart_button_rect, quit_button_rect

def display_mode_selection():
    """
    Function to display the mode selection screen, including light/dark theme selection and number of players

    Return:
        dark_button_rect (pygame.rect.Rect): pygame object representing the "Dark Mode" text button box
        light_button_rect (pygame.rect.Rect): pygame object representing the "Light Mode" text button box
        one_player_button_rect (pygame.rect.Rect): pygame object representing the "1 Player" text button box
        two_players_button_rect (pygame.rect.Rect): pygame object representing the "2 Players" text button box
        ok_button_rect (pygame.rect.Rect): pygame object representing the "Okay" text button box to confirm selections
    """    
    screen.fill(scr_color)

    # Create Select Mode text
    font = pygame.font.Font('freesansbold.ttf', 36)
    mode_text = font.render("Select Mode:", True, txt_color)
    mode_textRect = mode_text.get_rect()
    mode_textRect.center = (width / 2, height / 5 - 60)
    screen.blit(mode_text, mode_textRect)
    # Create mode selection buttons (light and dark) 
    dark_button_center = (width / 3 - 90, height / 5)
    light_button_center = (width * 2 / 3 - 90, height / 5)
    dark_button_rect = create_text_button(dark_button_center, message = "Dark Mode", text_color = WHITE, button_color = PURPLE, size = (180, 50))
    light_button_rect = create_text_button(light_button_center, message = "Light Mode", text_color = WHITE, button_color = YELLOW, size = (180, 50))
    # Create Number of Players text
    font = pygame.font.Font('freesansbold.ttf', 36)
    players_text = font.render("Number of Players:", True, txt_color)
    players_textRect = players_text.get_rect()
    players_textRect.center = (width / 2, height / 2 - 60)
    screen.blit(players_text, players_textRect)
    # Create player number buttons
    one_player_center = (width / 3 - 90, height / 2)
    two_players_center = (width * 2 / 3 - 90, height / 2)
    one_player_button_rect = create_text_button(one_player_center, message = "1 Player", text_color = bttn_txt_color, button_color = bttn_color, size = (180, 50))
    two_players_button_rect = create_text_button(two_players_center, message = "2 Players", text_color = bttn_txt_color, button_color = bttn_color, size = (180, 50))
    outline_color = WHITE if mode == "dark" else DARK_GRAY
    if num_players == 1:
        one_p_outline = pygame.Rect(one_player_center[0] - 5, one_player_center[1] - 5, 190, 60)
        pygame.draw.rect(screen, outline_color, one_p_outline, width = 2, border_radius = 15)
    elif num_players == 2:
        two_p_outline = pygame.Rect(two_players_center[0] - 5, two_players_center[1] - 5, 190, 60)
        pygame.draw.rect(screen, outline_color, two_p_outline, width = 2, border_radius = 15)
    # Create button to confirm selections
    ok_button_center = (width / 2 - 60, height * 3 / 4)
    ok_bttn_color = bttn_color if num_players > 0 else LIGHT_GRAY
    ok_txt_color = bttn_txt_color if num_players > 0 else DARK_GRAY
    ok_button_rect = create_text_button(ok_button_center, message = "Okay", text_color = ok_txt_color, button_color = ok_bttn_color)
    pygame.display.update()

    return dark_button_rect, light_button_rect, one_player_button_rect, two_players_button_rect, ok_button_rect # return all buttons

def display_found_words(page):
    """
    Function to display all words found by each player one one page each
    
        page (int): an integer representing the page number (0 or 1)
    
    Return:
        buttons (list): a list containing the x_button_rect, left_button_rect, and right_button_rect
    """
    menu_width = width * 0.6  # Adjusted width for longer messages
    menu_height = height * 0.6  # Adjusted height
    menu_x = (width - menu_width) / 2
    menu_y = (height - menu_height) / 2
    dimensions = (menu_width, menu_height)

    close_button_center = (menu_x + menu_width / 2 + 150, menu_y + 10)
    close_button_tuple = (close_button_center, "X", 24, WHITE, RED, (50, 50))
    buttons_list = [close_button_tuple]
    
    text_list = []
    if page == 0:
        title_tuple = ("Player 1 Words", BLUE, (width / 2, menu_y + 100), 0, ' ', 32)
        text_list.append(title_tuple)
        p1_words = words_made.get(1)
        p1_words_str = ""
        for i in range(len(p1_words)):
            p1_words_str += p1_words[i]
            if i < len(p1_words) - 1:
                p1_words_str += " "
        if p1_words_str != "":
            p1_words_tuple = (p1_words_str, WHITE, (0, 0), 140, '   ', 24)
            text_list.append(p1_words_tuple)
        else:
            message_tuple = ("No words found", LIGHT_GRAY, (width / 2, height / 2), 0, ' ', 24)
            text_list.append(message_tuple)
        left_text_color = DARK_GRAY
        left_button_color = LIGHT_GRAY
        right_text_color = BLACK
        right_button_color = GREEN

    if page == 1:
        title = "Bot Words" if vs_bot else "Player 2 Words"
        title_tuple = (title, DUSTY_RED, (width / 2, menu_y + 100), 0, ' ', 32)
        text_list.append(title_tuple)
        p2_words = words_made.get(2)
        p2_words_str = ""
        for i in range(len(p2_words)):
            p2_words_str += p2_words[i]
            if i < len(p2_words) - 1:
                p2_words_str += " "
        if p2_words_str != "":
            p2_words_tuple = (p2_words_str, WHITE, (0, 0), 140, '   ', 24)
            text_list.append(p2_words_tuple)
        else:
            message_tuple = ("No words found", LIGHT_GRAY, (width / 2, height / 2), 0, ' ', 24)
            text_list.append(message_tuple)
        left_text_color = BLACK
        left_button_color = GREEN
        right_text_color = DARK_GRAY
        right_button_color = LIGHT_GRAY

    left_button_center = (menu_x + 10, menu_y + menu_height - 60)
    right_button_center = (menu_x + menu_width / 2 + 150, menu_y + menu_height - 60)
    left_button_tuple = (left_button_center, "<", 24, left_text_color, left_button_color, (50, 50))
    buttons_list.append(left_button_tuple)
    right_button_tuple = (right_button_center, ">", 24, right_text_color, right_button_color, (50, 50))
    buttons_list.append(right_button_tuple)
    buttons = display_pop_up(dimensions, text_list, buttons_list)
    pygame.display.update()

    return buttons

def display_bot_menu(bot_moved, rack_idx=-1, col_idx=-1):
    menu_width = width * 0.6  # Adjusted width for longer messages
    menu_height = height * 0.4  # Adjusted height
    menu_y = (height - menu_height) / 2
    dimensions = (menu_width, menu_height)
    if not bot_moved:
        text_tuple = ("Bot thinking...", WHITE, (width / 2, menu_y + 150), 0, ' ', 24)
        text_list = [text_tuple]
        display_pop_up(dimensions, text_list, [])
    else:
        rack = curr_game.get_rack()
        message = f"Selected Tile: {rack[rack_idx]}"
        text_tuple = (message, WHITE, (width / 2, menu_y + 120), 0, ' ', 24)
        text_list = [text_tuple]
        display_pop_up(dimensions, text_list, [])
        pygame.display.update()
        message = f"Selected Column: {col_idx + 1}"
        text_tuple = (message, WHITE, (width / 2, menu_y + 200), 0, ' ', 24)
        text_list.append(text_tuple)
        time.sleep(2)
        display_pop_up(dimensions, text_list, [])
    pygame.display.update()
        
def ask_for_name(text_entry, entering_text):
    """
    Function to display the menu that asks the player for their name, including a text box with a cursor

        text_entry (string): Current string input to display in the text box
        entering_text (bool): True if the player has clicked the text box, False otherwise
    
    Return:
        text_box_rext (pygame.rect.Rect): 
        enter_button_rect (pygame.rect.Rect):
    """
    # Create gray background
    bg_width = 500
    bg_height = 150
    bg_x = (width - bg_width) / 2
    bg_y = (height - bg_height) / 2 - 25
    bg_rect = pygame.Rect(bg_x, bg_y, bg_width, bg_height)
    pygame.draw.rect(screen, DARK_GRAY, bg_rect, border_radius=6)

    # Create text asking for name
    msg_text = ""
    if num_players == 1:
        msg_text = "Input player name"
    else:
        player_num = player_idx + 1
        msg_text = f"Input Player {player_num} name"
    font = pygame.font.Font(None, 36)
    msg_x = bg_x + 20
    msg_y = bg_y + 30
    msg_surface = font.render(msg_text, True, WHITE)
    screen.blit(msg_surface, (msg_x, msg_y))

    # Dimensions and positions
    box_width = 380
    box_height = 40
    box_x = (width - box_width) / 2 - 40
    box_y = (height - box_height) / 2
    text_box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(screen, WHITE, text_box_rect, border_top_left_radius=5, border_bottom_left_radius=5)

    # Display the text that is being typed
    font = pygame.font.Font(None, 24)
    text_color = BLACK if entering_text else LIGHT_GRAY
    text_displayed = text_entry if entering_text else "Enter name here"
    text_surface = font.render(text_displayed, True, text_color)
    text_x = box_x + 10  # Padding from the left of the text box
    text_y = box_y + (box_height - text_surface.get_height()) / 2
    screen.blit(text_surface, (text_x, text_y))

    # Blinking cursor
    if entering_text:
        cursor_color = BLACK if pygame.time.get_ticks() // 500 % 2 == 0 else WHITE
        cursor_x = box_x + 10 + pygame.font.Font(None, 24).size(text_entry)[0]  # Cursor after the text
        cursor_y = box_y + 10
        pygame.draw.line(screen, cursor_color, (cursor_x, cursor_y), (cursor_x, cursor_y + box_height - 20), 2)
    else:
        cursor_x = box_x + 10 + pygame.font.Font(None, 24).size(text_entry)[0]  # Cursor after the text
        cursor_y = box_y + 10
        pygame.draw.line(screen, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + box_height - 20), 2)

    # Character count
    max_chars = 25
    curr_num_chars = len(text_entry)
    count_text = f"{curr_num_chars}/{max_chars}"
    font = pygame.font.Font(None, 24)
    count_render = font.render(count_text, True, BLACK)
    count_x = box_x + box_width - 40
    count_y = box_y + (box_height - count_render.get_height()) / 2
    screen.blit(count_render, (count_x, count_y))

    button_width = 80
    button_height = box_height
    button_x = box_x + box_width
    button_y = box_y
    enter_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, bttn_color, enter_button_rect, border_top_right_radius=5, border_bottom_right_radius=5)
    button_font = pygame.font.Font(None, 28)
    button_text = button_font.render("Enter", True, bttn_txt_color)
    button_text_x = button_x + (button_width - button_text.get_width()) / 2
    button_text_y = button_y + (button_height - button_text.get_height()) / 2
    screen.blit(button_text, (button_text_x, button_text_y))

    pygame.display.update()

    return text_box_rect, enter_button_rect

def display_leaderboard(title="Leaderboard"):
    """
    Displays a leaderboard on the screen with player names and scores.

        title (string): Title of the leaderboard (default is "Leaderboard").
    
    Return:
        close_button_rect (pygame.rect.Rect): pygame object representing the "X" text button box
    """

    leaderboard_data = get_leaderboard_data()

    # Define dimensions and positions
    leaderboard_width = 500
    leaderboard_height = 400  # Increased to accommodate 10 spots
    leaderboard_x = (screen.get_width() - leaderboard_width) // 2
    leaderboard_y = (screen.get_height() - leaderboard_height) // 2
    padding = 20

    # Background rectangle
    leaderboard_rect = pygame.Rect(leaderboard_x, leaderboard_y, leaderboard_width, leaderboard_height)
    pygame.draw.rect(screen, DARK_GRAY, leaderboard_rect, border_radius=10)

    # Title text
    font = pygame.font.Font(None, 38)
    title_text = font.render(title, True, WHITE)
    title_rect = title_text.get_rect(center=(leaderboard_x + leaderboard_width // 2, leaderboard_y + 2 * padding))
    screen.blit(title_text, title_rect)

    # Sort leaderboard data by score in descending order and pad to 10 entries
    padded_data = leaderboard_data + [("", "")] * (10 - len(leaderboard_data))

    # Render player names and scores
    font = pygame.font.Font(None, 28)
    for idx, (player, score) in enumerate(padded_data[:10]):
        text = f"{idx + 1}. {player}:  {score}" if player else f"{idx + 1}."
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(topleft=(leaderboard_x + padding + 5, leaderboard_y + 80 + idx * 30))
        screen.blit(text_surface, text_rect)

    # Display a "Close" button
    button_x = leaderboard_x + leaderboard_width - 60
    button_y = leaderboard_y + 10
    close_button_center = (button_x, button_y)
    close_button_rect = create_text_button(close_button_center, "X", 24, WHITE, RED, (50, 50))

    pygame.display.update()

    # Return the rectangle for the Close button to handle interaction
    return close_button_rect

# Create game object
curr_game = Back_end.Game()
board = curr_game.get_board() 
rack = curr_game.get_rack()
game_over = curr_game.get_game_state()
turn = curr_game.get_turn()

# Draw the board
pygame.display.update()
screen.fill(DARKER_GRAY)
start_button_rect = display_start_menu()

# Boolean flags
game_started = False
game_initiated = False
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
showing_player_words = False
col_idx = -1
row_idx = -1
word_idx = 0
scores = curr_game.get_scores()
end_screen_displayed = False
mode = "dark"
num_players = 0
vs_bot = False
curr_name = ""
displaying_name_menu = False
entering_name = False
player_idx = 0
displaying_end_menu = False
names = []
new_leaderboard = False
displaying_leaderboard = False

# Score and word information
turn_info = None
p1_points_gained = 0
p2_points_gained = 0
words_made = {1 : [], 2 : []}

# Check to make sure the game is not over yet 
while True:
    game_over = curr_game.get_game_state()
    board = curr_game.get_board()
    turn = curr_game.get_turn()
    scores = curr_game.get_scores()
    if game_over and not displaying_end_menu:
        displaying_name_menu = True
        text_box_rect, enter_button_rect = ask_for_name(curr_name, entering_name)
    if vs_bot and turn == 1:
        if not game_over:
            display_bot_menu(False)
            bot_move = curr_game.get_best_move()
            rack_idx = bot_move[0]
            col_idx = bot_move[1]
            display_bot_menu(True, rack_idx=rack_idx, col_idx=col_idx)
            curr_game.place_piece(rack_idx, col_idx)
            new_scores = curr_game.get_scores()
            turn_object = curr_game.game_history[-1]
            p2_points_gained = turn_object.score_gained
            p1_points_gained = 0
            curr_player = 2
            curr_words = words_made[curr_player]
            if len(turn_object.words_formed) > 0:
                for word in turn_object.words_formed:
                    curr_words.append(word[0])
            words_made[curr_player] = curr_words
            board = curr_game.get_board()
            time.sleep(2)
            draw_board(board)
            if scores[1] != new_scores[1]:
                sound = pygame.mixer.Sound(score_point_sound)
                sound.play()
            continue
    for event in pygame.event.get(): # any motion/action in pygame
        # Update board and turn number
        if event.type == pygame.QUIT: #user can exit if needed
            sys.exit()
        if not game_initiated: # Display starting menu
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if start_button_rect.collidepoint(mouse_pos):
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    game_initiated = True
                    continue
                continue
        if game_initiated and not game_started: # Display mode selection menu
            dark_button_rect, light_button_rect, one_player_button_rect, two_players_button_rect, ok_button_rect = display_mode_selection()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if dark_button_rect.collidepoint(mouse_pos) and mode != "dark": # "Dark Mode" button pressed
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    scr_color = DARKER_GRAY
                    txt_color = WHITE
                    bttn_color = GREEN
                    bttn_txt_color = BLACK
                    board_color = MAHOGANY
                    mode = "dark"
                    display_mode_selection()
                elif light_button_rect.collidepoint(mouse_pos) and mode != "light": # "Light Mode" button pressed
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    scr_color = BEIGE
                    txt_color = BLACK
                    bttn_color = ROYAL_BLUE
                    bttn_txt_color = WHITE
                    board_color = MAHOGANY
                    mode = "light"
                    display_mode_selection()
                elif ok_button_rect.collidepoint(mouse_pos) and num_players > 0: # "Okay" button pressed
                    game_started = True
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    draw_board(board)
                elif one_player_button_rect.collidepoint(mouse_pos) and num_players != 1: # "1 Player" button pressed
                    # Create game object
                    curr_game = Back_end.Game(mode="vs_bot", bot_depth=3)
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    num_players = 1
                    vs_bot = True
                elif two_players_button_rect.collidepoint(mouse_pos) and num_players != 2:
                    curr_game = Back_end.Game()
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    num_players = 2
                    vs_bot = False
                board = curr_game.get_board()
                rack = curr_game.get_rack()
                game_over = curr_game.get_game_state()
                turn = curr_game.get_turn()
                continue
            continue
        if displaying_name_menu and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if text_box_rect.collidepoint(mouse_pos):
                entering_name = True
            elif enter_button_rect.collidepoint(mouse_pos):
                if curr_name == "":
                    continue
                entering_name = False
                names.append(curr_name)
                curr_name = ""
                if num_players == 2:
                    player_idx += 1
                    if player_idx > 1:
                        for i in range(len(names)):
                            name = names[i]
                            score = scores[i]
                            added_score = add_to_leaderboard(name, score)
                            if added_score:
                                new_leaderboard = True
                        restart_button_rect, quit_button_rect = display_game_over(curr_game.get_game_state(), False, new_leaderboard)
                        displaying_name_menu = False
                        displaying_end_menu = True
                else:
                    name = names[0]
                    score = scores[0]
                    added_score = add_to_leaderboard(name, score)
                    if added_score:
                        new_leaderboard = True
                    restart_button_rect, quit_button_rect = display_game_over(curr_game.get_game_state(), False, new_leaderboard)
                    displaying_name_menu = False
                    displaying_end_menu = True
            else:
                entering_name = False
            continue
        if entering_name and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                curr_name = curr_name[:-1]
            elif event.key == pygame.K_COLON:
                continue
            elif event.key == pygame.K_RETURN:
                if curr_name == "":
                    continue
                entering_name = False
                names.append(curr_name)
                curr_name = ""
                if num_players == 2:
                    player_idx += 1
                    if player_idx > 1:
                        for i in range(len(names)):
                            name = names[i]
                            score = scores[i]
                            added_score = add_to_leaderboard(name, score)
                            if added_score:
                                new_leaderboard = True
                        restart_button_rect, quit_button_rect = display_game_over(curr_game.get_game_state(), False, new_leaderboard)
                        displaying_name_menu = False
                        displaying_end_menu = True
                else:
                    restart_button_rect, quit_button_rect = display_game_over(curr_game.get_game_state(), False, new_leaderboard)
                    displaying_name_menu = False
                    displaying_end_menu = True
            elif len(curr_name) < 25:
                curr_name += event.unicode
            continue
        if displaying_leaderboard:
            x_button_rect = display_leaderboard(title=title)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if x_button_rect.collidepoint(mouse_pos):
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    displaying_leaderboard = False
                    if game_over:
                        restart_button_rect, quit_button_rect = display_game_over(game_over, True, False)
                    else:
                        draw_board(board)
            continue
        if game_over and not displaying_name_menu:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if restart_button_rect.collidepoint(mouse_pos):
                    sound = pygame.mixer.Sound(button_press_sound)
                    curr_game = Back_end.Game()
                    # Update boolean flags
                    game_started = False
                    game_initiated = False
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
                    showing_player_words = False
                    col_idx = -1
                    row_idx = -1
                    word_idx = 0
                    scores = curr_game.get_scores()
                    end_screen_displayed = False
                    mode = "dark"
                    num_players = 0
                    vs_bot = False
                    curr_name = ""
                    displaying_name_menu = False
                    entering_name = False
                    player_idx = 0
                    displaying_end_menu = False
                    names = []
                    new_leaderboard = False
                    displaying_leaderboard = False
                elif quit_button_rect.collidepoint(mouse_pos):
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    sys.exit()
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
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    word_idx = 0
                    displaying_words = False
                    displaying_words_menu = False
                    draw_board(board)
                    continue
                if len(buttons) > 1:
                    if left_button_rect.collidepoint(mouse_pos):
                        if word_idx > 0:
                            sound = pygame.mixer.Sound(button_press_sound)
                            sound.play()
                            word_idx -= 1
                            buttons = display_tile_definitions(col_idx, row_idx, word_idx)
                    if right_button_rect.collidepoint(mouse_pos):
                        if word_idx < num_words - 1:
                            sound = pygame.mixer.Sound(button_press_sound)
                            sound.play()
                            word_idx += 1
                            buttons = display_tile_definitions(col_idx, row_idx, word_idx)
                    continue
            continue
        if error_message != "":
            if not error_message_drawn:
                x_button_rect = display_error_message(error_message)
            error_message_drawn = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if x_button_rect.collidepoint(mouse_pos):
                    if game_started:
                        draw_board(board)
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    error_message = ""
                    error_message_drawn = False
                    continue
            else:
                continue
        if game_started and not showing_rack and event.type == pygame.KEYDOWN and not paused:
            if not game_over:
                if event.key == pygame.K_p:
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    paused = True
                    resume_button_rect, options_button_rect = display_pause_menu()
                elif event.key == pygame.K_r:
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    showing_rack = True
                    rack = curr_game.get_rack()
                    if selected_idx != -1:
                        tmp_selected_idx = selected_idx
                        tmp_selected = True
                    rack_menu_buttons = display_rack(rack, selected_idx)
                    view_board_button_rect = rack_menu_buttons[0]
                    select_button_rect = rack_menu_buttons[1]
            if event.key == pygame.K_w and not displaying_leaderboard:
                sound = pygame.mixer.Sound(button_press_sound)
                sound.play()
                showing_player_words = True
                page = 0
                found_words_buttons = display_found_words(page)
                x_button_rect = found_words_buttons[0]
                left_button_rect = found_words_buttons[1]
                right_button_rect = found_words_buttons[2]
            elif event.key == pygame.K_l and not showing_player_words:
                sound = pygame.mixer.Sound(button_press_sound)
                sound.play()
                displaying_leaderboard = True
                title = "Singleplayer Leaderboard" if num_players == 1 else "Multiplayer Leaderboard"
                x_button_rect = display_leaderboard(title=title)
        if paused:  # Display pause menu
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if resume_button_rect.collidepoint(mouse_pos):
                        sound = pygame.mixer.Sound(button_press_sound)
                        sound.play()
                        paused = False
                        draw_board(board)
                        continue
                    elif options_button_rect.collidepoint(mouse_pos):
                        sound = pygame.mixer.Sound(button_press_sound)
                        sound.play()
                        # Do nothing for now when player presses the 'Options' button
                        pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    paused = False
                    draw_board(board)
                    continue
            continue
        if showing_player_words:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if x_button_rect.collidepoint(mouse_pos):
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    showing_player_words = False
                    draw_board(board)
                elif left_button_rect.collidepoint(mouse_pos):
                    if page > 0:
                        page -= 1
                        sound = pygame.mixer.Sound(button_press_sound)
                        sound.play()
                        found_words_buttons = display_found_words(page)
                        x_button_rect = found_words_buttons[0]
                        left_button_rect = found_words_buttons[1]
                        right_button_rect = found_words_buttons[2]
                elif right_button_rect.collidepoint(mouse_pos):
                    if page < 1:
                        page += 1
                        sound = pygame.mixer.Sound(button_press_sound)
                        sound.play()
                        found_words_buttons = display_found_words(page)
                        x_button_rect = found_words_buttons[0]
                        left_button_rect = found_words_buttons[1]
                        right_button_rect = found_words_buttons[2]
                continue

        if showing_rack:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for i in range(2, len(rack_menu_buttons)):  # Start from index 2 to skip 'View Board' and 'Select Tile'
                    tile_button_rect, rack_idx = rack_menu_buttons[i]
                    if tile_button_rect.collidepoint(mouse_pos):
                        if tmp_selected and rack_idx == tmp_selected_idx:
                            tmp_selected = False
                            tmp_selected_idx = -1
                        else:
                            tmp_selected = True
                            tmp_selected_idx = rack_idx
                        sound = pygame.mixer.Sound(tile_drop_sound)
                        sound.play()
                        rack_menu_buttons = display_rack(rack, tmp_selected_idx)
                        continue
                if view_board_button_rect.collidepoint(mouse_pos):
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    showing_rack = False
                    draw_board(board)
                    selected_idx = tmp_selected_idx = -1
                    selected = tmp_selected = False
                    continue
                elif tmp_selected and select_button_rect.collidepoint(mouse_pos):
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    selected = tmp_selected
                    selected_idx = tmp_selected_idx
                    tmp_selected = False
                    tmp_selected_idx = -1
                    showing_rack = False
                    draw_board(board)
                    pygame.draw.rect(screen, scr_color, (0, 0, width, square_size))
                    rack = curr_game.get_rack()
                    pos_x = event.pos[0]
                    tile_image = load_tile_image(rack[selected_idx])
                    tile_rect = tile_image.get_rect(center=(pos_x, square_size / 2))  # Adjust position as needed
                    screen.blit(tile_image, tile_rect)
                    pygame.display.update()
                    continue
                else:
                    selected_idx = -1
                    continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    showing_rack = False
                    draw_board(board)
                    tmp_selected = False
                    continue
                elif tmp_selected and event.key == pygame.K_RETURN:
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    selected = tmp_selected
                    selected_idx = tmp_selected_idx
                    tmp_selected = False
                    tmp_selected_idx = -1
                    showing_rack = False
                    draw_board(board)
        if not displaying_words and not showing_rack and game_started:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board = curr_game.get_board()
                turn = curr_game.get_turn()
                if selected:
                    pygame.draw.rect(screen, scr_color, (0, 0, width, square_size))
                    x_pos = event.pos[0]
                    column = int(x_pos // square_size)
                    placed_piece = curr_game.place_piece(selected_idx, column)
                    # Update turn_info
                    turn_object = curr_game.game_history[-1]
                    curr_player = 1
                    if curr_game.get_turn() == 1:
                        p1_points_gained = turn_object.score_gained
                        p2_points_gained = 0
                    else:
                        p2_points_gained = turn_object.score_gained
                        p1_points_gained = 0
                        curr_player = 2
                    curr_words = words_made[curr_player]
                    if len(turn_object.words_formed) > 0:
                        for word in turn_object.words_formed:
                            curr_words.append(word[0])
                    words_made[curr_player] = curr_words
                    if placed_piece == 1:
                        sound = pygame.mixer.Sound(error_sound)
                        sound.play()
                        error_message = "Column is full! Please place tile in a different column."
                        display_error_message(error_message)
                    selected_idx = -1
                    selected = False
                    if game_started:
                        draw_board(board)
                    sound = pygame.mixer.Sound(tile_drop_sound)
                    sound.play()
                    new_scores = curr_game.get_scores()
                    if new_scores[0] != scores[0] or new_scores[1] != scores[1]:
                        sound = pygame.mixer.Sound(score_point_sound)
                        sound.play()
                        scores = new_scores
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
                    sound = pygame.mixer.Sound(button_press_sound)
                    sound.play()
                    x_button_rect = display_tile_definitions(col_idx, row_idx)
            if event.type == pygame.MOUSEMOTION and selected_idx != -1:
                pygame.draw.rect(screen, scr_color, (0, 0, width, square_size))
                rack = curr_game.get_rack()
                pos_x = event.pos[0]
                tile_image = load_tile_image(rack[selected_idx])
                tile_rect = tile_image.get_rect(center=(pos_x, square_size / 2))  # Adjust position as needed
                screen.blit(tile_image, tile_rect)
                pygame.display.update()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    selected = False
                    selected_idx = -1
                    pygame.draw.rect(screen, scr_color, (0, 0, width, square_size))
                    pygame.display.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            for col_idx in range(7):
                for _ in range(7):
                    curr_game.place_piece(0, col_idx)
            board = curr_game.get_board()
            draw_board(board)