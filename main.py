import pygame as pg
import asyncio
from bananagrams.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, LETTERCOLOR
from bananagrams.board import Board
from bananagrams.game import Game
from solver import SolveState

try:
    import aio.gthread as threading
except:
    ...

from threading import Thread

pg.init()
def new_screen():
    WIN = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Banagrams!')
    return WIN

async def main():
    import random
    random.seed(None)
    FPS = 60
    clock = pg.time.Clock()
    clock.tick(FPS)
    run = True
    win = new_screen()
    Thread(target=game_loop, args = [win]).start()
    t = 0
    while run:
        pg.display.update()
        await asyncio.sleep(0)
        pass

    pg.quit()
    pass


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = (x - 16 * SQUARE_SIZE) // SQUARE_SIZE
    return row, col



def game_loop(win):
    game = Game(win)

    FPS = 60
    run = True
    clock = pg.time.Clock()
    # clock.tick(FPS)
    user_text = ''
    r_row = 0
    r_col = 0
    game_over = False
    direction = "RIGHT"
    active = False
    selected_tile = False


    AI_PLAY = pg.USEREVENT + 1

    AI_PLAY2 = pg.USEREVENT + 2

    pg.time.delay(1500)
    game.ai_inital_play()
    game.update(user_text)
    pg.time.delay(500)

    # pg.time.set_timer(AI_PLAY2, 150, 0)

    pg.time.set_timer(AI_PLAY, 4500)


    while not aio.exit:
        clock.tick(FPS)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                run = False

            if game_over == False:
                # if event.type ==AI_PLAY2:
                #     game.ai_inital_play()
                #     # game.update(user_text)

                if event.type == AI_PLAY:

                    if game.ai_normal_play() == True:
                        game.game_over = True
                        game_over = True

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:

                        print("Peel!")
                        # game.peel()
                        game.human_peel()
                        #game.player2_peel()

                    elif event.key == pg.K_SPACE:
                        print("Space")
                        game.game_over = True
                        game_over = True

                        # run = False

                    elif event.key == pg.K_2 and r_row == 15:
                        print("Dump!")
                        game.human_dump(r_row, r_col)

                    elif event.key == pg.K_BACKSPACE and active == True:
                        user_text = user_text[:-1]
                        print("Backspace")
                        print(user_text)
                    elif event.key == pg.K_RETURN and active == True:
                        active = False
                        game.place_word(user_text, r_row, r_col, direction)
                        direction = "RIGHT"
                        user_text=''
                    elif event.key == pg.K_DOWN and active == True:
                        direction = "DOWN"
                    elif active == True:
                        user_text += event.unicode
                        print(user_text)

                if event.type == pg.MOUSEBUTTONDOWN:

                    pos = pg.mouse.get_pos()
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
        yield aio


asyncio.run(main())
