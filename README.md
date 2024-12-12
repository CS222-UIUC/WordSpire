Wordspire: A mix between Connect-4 and Scrabble
====

## Overview:

Wordspire is a mix between Connect-4 and Scrabble that plays on a 7x7 board with a 7-letter rack. Each turn a player chooses a tile from the rack and places it in one of the columns on the board, forming words and getting points for each new word. Wordspire has 3 game modes: singleplayer, local multiplayer, and vs. Bot. Inspired by simple word games, such as Wordle, we aimed to develop a new word game that is easy to learn and fun to play.


## Technical Architecture:

Wordspire is comprised of 2 main components, the frontend which accepts player inputs and the backend which handles the game logic and contains the bot. These components 

![Technical Architecture Diagram](https://github.com/user-attachments/assets/b7d78acf-98cc-4065-a469-ed46484f5f12)

#### Front end:

The frontend implements python through the pygame library using it for graphics and user interaction. 
Our program initializes game assets such as:
Image tiles for letters, Sound effects, Leaderboard files
It creates an interactive game board with components such as:
Buttons, Menus, Sound effects
The front-end also implements user inputs via mouse clicks and keyboard actions and updates them on the screen. 
 The front end works with the backend to implement core functionalities such as:
Retrieving the current board and rack
Maintaining the game state
Calculating scores
Tracking player moves

#### Back end:

The back end is designed to support the implementation of our game and its various game modes, including:
Enforcing rules
Scoring moves
Providing feedback on played tiles 

More specifically, the back end is simply written as a Python class which can be initialized with certain game rules and in a specific gamemode. These features are then easily accessed by the front end through a variety of functions such as place_piece, get_best_move, etc.

The back end class also host the bot, which uses Cython for a performance speed up over Python and is similarly implemented as a class with accessor functions. 

The words and their definition come from the 2019 Scrabble Collins Dictionary word list.


## How to Play Wordspire:

Press 'R' to view the current player's rack 
Press 'B' or 'ESC' to view the board from the rack menu
Press 'L' to view the leaderboard for the current gamemode
Press 'P' to pause the game
Press 'W' to view all current words made by each player    
Click on tiles when viewing the board to see if any words were generated at said tile

## Authors/Contributors: 
- *Phillip Nakamura*: Backend
- *Ben Pazner*: Backend
- *Jasmine Patel*: Frontend
- *Aidan Tijerina-Albury*: Frontend



