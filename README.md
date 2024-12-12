Wordspire: A mix between Connect-4 and Scrabble
====

## Overview:

Wordspire is a mix between Connect-4 and Scrabble that plays on a 7x7 board with a 7-letter rack. Each turn a player chooses a tile from the rack and places it in one of the columns on the board, forming words and getting points for each new word. Wordspire has 3 game modes: singleplayer, local multiplayer, and vs. Bot. Inspired by simple word games, such as Wordle, we aimed to develop a new word game that is easy to learn and fun to play.

<img width="49.5%" alt="Screenshot 2024-12-12 at 12 45 31 PM" src="https://github.com/user-attachments/assets/17967666-342c-4068-ab22-5c5608ef9af0" />
<img width="49.5%" alt="Screenshot 2024-12-12 at 12 42 03 PM" src="https://github.com/user-attachments/assets/e77fbadd-4563-4779-9871-15dc35fb8e8a" />


## Technical Architecture:

Wordspire is comprised of 2 main components, the frontend which accepts player inputs and the backend which handles the game logic and contains the bot. 

To communicate between components, the backend is a Python class, which can be initialized with certain game rules and in a specific game mode. These features are then easily accessed by the front end through a variety of functions such as place_piece, get_best_move, etc. The backend class also hosts the bot, which uses Cython for a performance speed up over Python and is similarly implemented as a class with accessor functions. 


![Technical Architecture Diagram](https://github.com/user-attachments/assets/b7d78acf-98cc-4065-a469-ed46484f5f12)

#### Frontend:

The frontend is implemented in Python through the pygame library, which is used to handle graphics and user interaction. Using game assets including image tiles, sound effects, and a leaderboard file the frontend also creates an interactive game board, which players can play with via mouse clicks and keyboard actions, also handled by the frontend. Finally, the frontend holds an instance of the backend class and calls functions on the backend to implement core functionalities as discussed below.

#### Backend:

The back end is designed to support the implementation of our game and its various game modes, including maintaining the current board and rack, calculating scores, tracking player moves, enforcing rules, and providing feedback on played tiles such as definitions and earned points. The words and their definition come from the 2019 Scrabble Collins Dictionary word list. Finally, the backend also implements the bot logic as a separate class, which uses a min-max algorithm with alpha-beta pruning. Due to the randomness of potential newly drawn times, the bot only considers the tiles currently on the rack, leading to a max depth of 7, which can be computed in roughly 1-2 seconds. 

## How to Play Wordspire:



Press 'R' to view the current player's rack

Press 'B' or 'ESC' to view the board from the rack menu

Press 'L' to view the leaderboard for the current gamemode

Press 'P' to pause the game

Press 'W' to view all current words made by each player  

Click on tiles when viewing the board to see if any words were generated at said tile

These rules can also be easily visualized at any time in-game by clicking on the blue "*i*" button.

<img width="95%" alt="Screenshot 2024-12-12 at 12 50 47 PM" src="https://github.com/user-attachments/assets/de980d57-5305-45f2-a300-0dfda2dfc3a5" />

## Authors/Contributors: 
- *Phillip Nakamura*: Backend
- *Ben Pazner*: Backend
- *Jasmine Patel*: Frontend
- *Aidan Tijerina-Albury*: Frontend




