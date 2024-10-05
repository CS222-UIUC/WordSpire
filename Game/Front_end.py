import pygame #https://www.pygame.org/docs/
import sys

def draw_board(board):
    pass

pygame.init()
Column_size = 7 #this may be changed
Row_size = 7
Square_size = 100
width = Column_size * Square_size #number of columns 
height = (Row_size + 1) * Square_size #height +1 row for game piece?

size = (width, height) #size of the screen with extra space on top 

screen = pygame.display.setmode(size) #gives the screen size of the game board 

#check to make sure the game is not over yet 
for event in pygame.event.get(): #any motion
    if event.type == pygame.QUIT: #user can exit if needed
        sys.exit() 
    if event.type == pygame.MOUSEBUTTONDOWN: #to place pieces
        print("hello")