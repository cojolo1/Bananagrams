import pygame
from bananagrams.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, LETTERCOLOR
from bananagrams.board import Board
from bananagrams.game import Game
from solver import SolveState
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Banagrams!')
pygame.init()
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = (x - 16 * SQUARE_SIZE) // SQUARE_SIZE
    return row, col

def main():
    """Runs the game loop"""
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)


    user_text = ''
    r_row = 0
    r_col = 0
    total_moves = 0
    game_over = False
    direction = "RIGHT"
    active = False
    selected_tile = False

    #The different user-defined events that we will used to allow the
    #AI to make moves and display the approtiate text
    AI_PLAY = pygame.USEREVENT + 1
    AI_PLAY2 = pygame.USEREVENT + 2
    PEEL_DISPLAY_OFF = pygame.USEREVENT + 3
    DUMP_DISPLAY_OFF = pygame.USEREVENT + 4

    #Sets the frequency and occurences for the different moves the AI player will make
    pygame.time.set_timer(AI_PLAY2, 1500, 1)
    pygame.time.set_timer(AI_PLAY, 6000)

    while run:
        clock.tick(FPS)

        #Determines if a player/AI has "Peeled"
        if game.is_peel:
            print("Setting Peel Timer")
            pygame.time.set_timer(PEEL_DISPLAY_OFF, 700, 1)
            game.is_peel = False
            game.is_peel_text = True

        # Determines if a player/AI has "Dumped"
        if game.is_dump:
            print("Setting Dump Timer")
            pygame.time.set_timer(DUMP_DISPLAY_OFF, 700, 1)
            game.is_dump = False
            game.is_dump_text = True


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if game_over == False:

                #Removes the peel text display after 0.7 seconds
                if event.type == PEEL_DISPLAY_OFF:
                    print("Peel Display Off Event")
                    print("is_peel_text", game.is_peel_text)
                    game.is_peel_text = False

                # Removes the dump text display after 0.7 seconds
                if event.type == DUMP_DISPLAY_OFF:
                    print("Dump Display Off Event")
                    print("is_dump_text", game.is_dump_text)
                    game.is_dump_text = False

                #Calls the AI's initial play
                if event.type ==AI_PLAY2:
                    total_moves += 1
                    game.ai_inital_play()
                    game.update(user_text)

                #Calls all the AI's plays after initial play
                if event.type == AI_PLAY:
                    total_moves +=1
                    if game.ai_normal_play() == True:
                        print("The most troublesome letter in this game was", game.find_ultimate_troublesome_word())
                        print("The total moves this game: ", total_moves )
                        game.game_over = True
                        game_over = True

                #Controls all the events associated with a keydown
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        print("Peel!")
                        game.human_peel()

                    elif event.key == pygame.K_SPACE:
                        print("Space")
                        game.game_over = True
                        game_over = True

                    elif event.key == pygame.K_2 and r_row == 15:
                        print("Dump!")
                        game.human_dump(r_row, r_col)

                    elif event.key == pygame.K_BACKSPACE and active == True:
                        user_text = user_text[:-1]
                        print("Backspace")
                        print(user_text)
                    elif event.key == pygame.K_RETURN and active == True:
                        active = False
                        game.place_word(user_text, r_row, r_col, direction)
                        direction = "RIGHT"
                        user_text=''
                    elif event.key == pygame.K_DOWN and active == True:
                        direction = "DOWN"
                    elif active == True:
                        user_text += event.unicode
                        print(user_text)

                #Controls all the events associated with a mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    print("You selected row: ", row)
                    print("You selected column: ", col)
                    if event.button == 1:
                        gameboard = game.player2_get_board()

                        if row < 15 and row >= 0 and col < 15 and col >= 0:
                            if gameboard[row][col] != None:
                                selected_tile = True
                                print("You selected a non-empty tile")
                                print("Row", row)
                                print("Col", col)
                                game.select(row, col)
                            else:
                                print("you selected an empty tile")
                                if selected_tile:
                                    game.select(row,col)
                                    selected_tile = False
                                else:
                                    user_text = ''
                                    active = True
                                    r_row = row
                                    r_col = col
                        elif row == 15:
                            r_row = row
                            r_col = col

        game.update(user_text)

    pygame.quit()

main()
