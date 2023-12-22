import pygame
from game_bananagrams.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, LETTERCOLOR
from game_bananagrams.board import Board
from game_bananagrams.game import Game
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

    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    user_text = ''
    r_row = 0
    r_col = 0
    game_over = False
    direction = "RIGHT"
    active = False
    selected_tile = False

    AI_PLAY = pygame.USEREVENT + 1

    AI_PLAY2 = pygame.USEREVENT + 2

    pygame.time.set_timer(AI_PLAY2, 1500, 1)

    pygame.time.set_timer(AI_PLAY, 4500)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
            if game_over == False:

                if event.type ==AI_PLAY2:
                    game.ai_inital_play()
                    game.update(user_text)

                if event.type == AI_PLAY:
                    if game.ai_normal_play() == True:
                        game.game_over = True
                        game_over = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:

                        print("Peel!")
                        # game.peel()
                        game.human_peel()
                        #game.player2_peel()

                    elif event.key == pygame.K_SPACE:
                        print("Space")
                        game.game_over = True
                        game_over = True

                        # run = False

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
                                # game.select(row, col)
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
