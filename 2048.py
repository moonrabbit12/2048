import pygame
import time
import random
import numpy as np
import os

class Cell:
    def __init__(self, val=0):
        self.value = val
        self.merged = False
        self.collided = False 

pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

WHITE = (255, 255, 255)
GRAY = (204, 204, 204)
ORANGE = (255, 133, 51)
BLACK = (0,0,0)
GREEN = (0,200,0)
RED = (200,0,0)
BRIGHT_GREEN = (0,255,0)
BRIGHT_RED = (255,0,0)
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('2048')
clock = pygame.time.Clock() # measure FPS

# make sliding functions        
        
def slideBlocks(direction, grid,score):
    if direction == pygame.K_UP:
        grid,score = slide_up(grid,score)
    elif direction == pygame.K_DOWN:
        grid,score = slide_down(grid,score)
    elif direction == pygame.K_LEFT:
        grid,score = slide_left(grid,score)
    elif direction == pygame.K_RIGHT: 
        grid,score = slide_right(grid,score)
    return grid,score

def slide_up(grid,score):
    for row in range(1,4):
        for col in range(4):
            if grid[row-1][col].value == 0:
                grid[row-1][col].value = grid[row][col].value
                grid[row][col].value = 0
            else:
                if (grid[row-1][col].value == grid[row][col].value 
                    and not grid[row-1][col].merged 
                    and not grid[row][col].merged):
                    grid[row-1][col].value = grid[row-1][col].value + grid[row][col].value
                    grid[row-1][col].merged = True
                    grid[row][col].value = 0
                    score = score + grid[row-1][col].value
    return grid,score

def slide_down(grid,score):
    for row in reversed(range(3)):
        for col in range(4):
            if grid[row+1][col].value == 0:
                grid[row+1][col].value = grid[row][col].value
                grid[row][col].value = 0
            else:
                if (grid[row+1][col].value == grid[row][col].value 
                    and not grid[row+1][col].merged 
                    and not grid[row][col].merged):
                    grid[row+1][col].value = grid[row+1][col].value + grid[row][col].value
                    grid[row+1][col].merged = True
                    grid[row][col].value = 0
                    score = score + grid[row+1][col].value
    return grid,score

def slide_left(grid,score):
    for col in range(1,4):
        for row in range(4):
            if grid[row][col-1].value == 0:
                grid[row][col-1].value = grid[row][col].value
                grid[row][col].value = 0
            else:
                if (grid[row][col-1].value == grid[row][col].value
                   and not grid[row][col-1].merged
                   and not grid[row][col].merged):
                    grid[row][col-1].value = grid[row][col-1].value + grid[row][col].value
                    grid[row][col-1].merged = True
                    grid[row][col].value = 0
                    score = score + grid[row][col-1].value
    return grid,score

def slide_right(grid,score):
    for col in reversed(range(3)):
        for row in range(4):
            if grid[row][col+1].value == 0:
                grid[row][col+1].value = grid[row][col].value
                grid[row][col].value = 0
            else:
                if (grid[row][col+1].value == grid[row][col].value
                   and not grid[row][col+1].merged
                   and not grid[row][col].merged):
                    grid[row][col+1].value = grid[row][col+1].value + grid[row][col].value
                    grid[row][col+1].merged = True
                    grid[row][col].value = 0
                    score = score + grid[row][col+1].value
    return grid,score


def spawn_block(grid):
    if empty_cells_exist(grid):
        empty_cells = []
        for row in range(4):
            for col in range(4):
                if grid[row][col].value == 0:
                    empty_cells.append((row,col))
        chosenCell = random.choice(empty_cells)
        chosenNum = np.random.choice([2,4], p=[0.7,0.3])
        cell = Cell(chosenNum)
        grid[chosenCell[0]][chosenCell[1]] = cell
    return grid
def empty_cells_exist(grid):
    for row in range(4):
        for col in range(4):
            if grid[row][col].value == 0:
                return True
    return False

def initialize_blocks(grid):
    cells = []
    for row in range(4):
        for col in range(4):
            cells.append((row,col))
    chosenCell1 = random.choice(cells)
    cells.remove(chosenCell1) 
    chosenCell2 = random.choice(cells)
    chosenNum1 = np.random.choice([2,4], p=[0.9,0.1])
    chosenNum2 = np.random.choice([2,4], p=[0.7,0.3])
    cell1 = Cell(chosenNum1)
    cell2 = Cell(chosenNum2)
    grid[chosenCell1[0]][chosenCell1[1]] = cell1
    grid[chosenCell2[0]][chosenCell2[1]] = cell2
    return grid


def draw_blocks(grid,CELL_MARGIN,CELL_WIDTH,CELL_HEIGHT):
    colors = {
        2: (242, 242, 242),
        4: (204, 204, 204),
        8: (255, 209, 179),
        16: (255, 148, 77),
        32: (230, 92, 0),
        64: (255, 102, 102),
        128: (255, 255, 102),
        256: (230, 230, 0),
        512: (179, 179, 0),
        1024: (154, 229, 154),
        2048: (73, 208, 73)
    }
    for row in range(4):
        for col in range(4):
            if grid[row][col].value != 0:
                if grid[row][col].value <= 2048:
                    color = colors[grid[row][col].value]
                else:
                    color = (128, 204, 255)
                pygame.draw.rect(gameDisplay, color, 
                                 [(CELL_MARGIN+CELL_WIDTH) * col + CELL_MARGIN,
                                (CELL_MARGIN+CELL_HEIGHT) * row + CELL_MARGIN,
                                CELL_WIDTH,
                                CELL_HEIGHT])
                smallText = pygame.font.Font("freesansbold.ttf",40)
                textSurf, textRect = text_objects(str(grid[row][col].value),smallText,grid[row][col].value)
                x = (CELL_MARGIN+CELL_WIDTH) * col + CELL_MARGIN
                y = (CELL_MARGIN+CELL_HEIGHT) * row + CELL_MARGIN
                textRect.center = (x+(CELL_WIDTH/2),y+(CELL_HEIGHT/2))
                gameDisplay.blit(textSurf,textRect)
            else:
                pygame.draw.rect(gameDisplay, GRAY, 
                                 [(CELL_MARGIN+CELL_WIDTH) * col + CELL_MARGIN,
                                (CELL_MARGIN+CELL_HEIGHT) * row + CELL_MARGIN,
                                CELL_WIDTH,
                                CELL_HEIGHT])


def game_loop():
    
    gameExit = False
    
    CELL_WIDTH  = 120
    CELL_HEIGHT = 120
    CELL_MARGIN = 10
    
    high_score = 0
    score = 0

    filename = "high_score.txt"
    if not os.path.isfile(filename):
	    # File does not exist, create it and write a default high score
	    with open(filename, "w") as f:
	        f.write("0")
	    print("High score file created.")
	    
    with open(filename, "r+") as f:
        high_score = int(f.read())
        
    
    # make 4-by-4 grid (2D integer array)
    grid = []
    for row in range(4):
        grid.append([])
        for col in range(4):
            cell = Cell()
            grid[row].append(cell)
    
    direction = None
    
    grid = initialize_blocks(grid)
    
    # actually draw the game initially
    
    gameDisplay.fill(WHITE)
    
    for row in range(4):
        for col in range(4):
            pygame.draw.rect(gameDisplay, GRAY,
                            [(CELL_MARGIN+CELL_WIDTH) * col + CELL_MARGIN,
                                (CELL_MARGIN+CELL_HEIGHT) * row + CELL_MARGIN,
                                CELL_WIDTH,
                                CELL_HEIGHT])
    
    draw_blocks(grid,CELL_MARGIN,CELL_WIDTH,CELL_HEIGHT)
    pygame.display.update()
    
    # the actual gameplay starts from down here
    
    counter = 0
    
    while not gameExit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_DOWN 
                    or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    direction = event.key
                    break
                    # TODO: check if breaking is the way to process one command at a time
        
        if (direction == pygame.K_UP or direction == pygame.K_DOWN 
                    or direction == pygame.K_LEFT or direction == pygame.K_RIGHT):
            counter = counter + 1
            for slide in range(3):
                grid,score = slideBlocks(direction,grid,score)
            direction = None
            # reset all the collided flags
            for row in range(4):
                for col in range(4):
                    grid[row][col].collided = False
                    grid[row][col].merged = False
        
            grid = spawn_block(grid)
            
                
        
        draw_blocks(grid,CELL_MARGIN,CELL_WIDTH,CELL_HEIGHT)
        display_score(score,high_score)
        if gameOver(grid,score,high_score):
            prompt_game_over()
        pygame.display.update()
        clock.tick(60)



def gameOver(grid,score,high_score):
    if not empty_cells_exist(grid) and not adjacent_tiles_with_same_val_exist(grid):
        if score > high_score:
            with open("high_score.txt", "w") as f:
                f.write(str(score))
        prompt_game_over()
        

def prompt_game_over():
    message_display("Game Over")
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text,largeText)
    TextRect.center = ((DISPLAY_WIDTH/2),(DISPLAY_HEIGHT/2))
    gameDisplay.blit(TextSurf,TextRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()
def adjacent_tiles_with_same_val_exist(grid):
    for row in range(4):
        for col in range(4):
            if row==0 and col==0:
                if (grid[row][col].value == grid[row][col+1].value
                   or grid[row][col].value == grid[row+1][col].value):
                    return True
            elif row==0 and col > 0 and col < 3:
                if (grid[row][col].value == grid[row][col-1].value
                   or grid[row][col].value == grid[row][col+1].value
                   or grid[row][col].value == grid[row+1][col].value):
                    return True
            elif row==0 and col==3:
                if (grid[row][col].value == grid[row][col-1].value
                   or grid[row][col].value == grid[row+1][col].value):
                    return True
            elif row > 0 and row < 3 and col==0:
                if (grid[row][col].value == grid[row][col+1].value
                   or grid[row][col].value == grid[row-1][col].value
                   or grid[row][col].value == grid[row+1][col].value):
                    return True
            elif row > 0 and row < 3 and col > 0 and col < 3:
                if (grid[row][col].value == grid[row][col-1].value
                   or grid[row][col].value == grid[row][col+1].value
                   or grid[row][col].value == grid[row-1][col].value
                   or grid[row][col].value == grid[row+1][col].value):
                    return True
            elif row > 0 and row < 3 and col==3:
                if (grid[row][col].value == grid[row][col-1].value
                   or grid[row][col].value == grid[row-1][col].value
                   or grid[row][col].value == grid[row+1][col].value):
                    return True
            elif row==3 and col==0:
                if (grid[row][col].value == grid[row][col+1].value
                   or grid[row][col].value == grid[row-1][col].value):
                    return True
            elif row==3 and col > 0 and col < 3:
                if (grid[row][col].value == grid[row][col-1].value
                   or grid[row][col].value == grid[row][col+1].value
                   or grid[row][col].value == grid[row-1][col].value):
                    return True
            elif row==3 and col==3:
                if (grid[row][col].value == grid[row][col-1].value
                   or grid[row][col].value == grid[row-1][col].value):
                    return True
    return False






def display_score(score,high_score):
    pygame.draw.rect(gameDisplay, WHITE, 
                     (DISPLAY_WIDTH-200,0,200,20))
    smallText = pygame.font.Font("freesansbold.ttf",15)
    textSurf, textRect = text_objects("Score: "+str(score),smallText)
    x = DISPLAY_WIDTH-200
    y = 0
    textRect.center = (x+(200/2),y+(20/2))
    gameDisplay.blit(textSurf,textRect)
    
    pygame.draw.rect(gameDisplay, WHITE, 
                     (DISPLAY_WIDTH-200,30,200,20))
    smallText = pygame.font.Font("freesansbold.ttf",15)
    textSurf, textRect = text_objects("High Score: "+str(high_score),smallText)
    x = DISPLAY_WIDTH-200
    y = 30
    textRect.center = (x+(200/2),y+(20/2))
    gameDisplay.blit(textSurf,textRect)



def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(WHITE)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("2048",largeText,0)
        TextRect.center = ((DISPLAY_WIDTH/2),(DISPLAY_HEIGHT/2))
        gameDisplay.blit(TextSurf,TextRect)
        
        button("Play!",150,450,100,50,GREEN,BRIGHT_GREEN,"play")
        button("Quit!",550,450,100,50,RED,BRIGHT_RED,"quit")
             
        pygame.display.update()
        clock.tick(15)

def button(msg,x,y,w,h,i_col,a_col,action=None):    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, a_col, (x,y,w,h))
        if click[0] == 1 and action != None:
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gameDisplay, i_col, (x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg,smallText)
    textRect.center = (x+(w/2),y+(h/2))
    gameDisplay.blit(textSurf,textRect)

    pygame.display.update()
    
def text_objects(text,font,value=0):
    if value < 8:
        textSurface = font.render(text, True, BLACK)
    else:
        textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()



game_intro()
pygame.quit()
quit()