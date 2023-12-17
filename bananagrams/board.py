import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, LETTERCOLOR
from .piece import Piece
import random
class Board:
    def __init__(self, win):
        self.board = []
        self.tiles = []

        self.secret_tiles = []

        self.player1_hand_letter = []
        self.player1_hand = []
        self.win = win

        self.player2_board = []
        self.player2_hand = []

        self.draw_squares(self.win)
        self.create_tiles()
        self.create_secret_tiles()
        self.deal_inital()
        self.create_board()
        self.draw(self.win)



    def get_tiles(self):
        return self.tiles

    def get_board(self):
        return self.board

    def draw_squares(self, win):
        win.fill(BLACK)

        for row in range(15):
            for col in range(15):
                pygame.draw.rect(win, LETTERCOLOR, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

        for row in range(15):
            for col in range(15):
                pygame.draw.rect(win, LETTERCOLOR, (row * SQUARE_SIZE + SQUARE_SIZE * 16, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)



    def move(self, piece, row, col):

        self.player2_board[piece.row][piece.col], self.player2_board[row][col] = self.player2_board[row][col], self.player2_board[piece.row][piece.col]
        piece.player2_move(row, col)

        if piece.row < 15:
            self.player2_hand[self.player2_hand.index(piece)] = 0
            # self.player2_hand.remove(piece)



    def ai_move(self, piece, row, col, index_of_tile_in_player_hand):
        self.player1_hand[self.player1_hand.index(piece)] = 0
        self.board[row][col] = piece
        self.board[piece.row][piece.col] = None
        piece.move(row, col)


    def move_by_click(self, piece, row, col):
        self.player2_board[piece.row][piece.col], self.player2_board[row][col] = self.player2_board[row][col], self.player2_board[piece.row][piece.col]
        piece.player2_move(row, col)


    def create_secret_tiles(self):
        tiles = []
        for j in range(2):
            tiles.append(Piece('J'))
        for k in range(2):
            tiles.append(Piece('K'))
        for q in range(2):
            tiles.append(Piece('Q'))
        for x in range(2):
            tiles.append(Piece('X'))
        for z in range(2):
            tiles.append(Piece('Z'))
        for e in range(18):
            tiles.append(Piece('E'))
        for k in range(13):
            tiles.append(Piece('A'))
        for i in range(12):
            tiles.append(Piece('I'))
        for o in range(11):
            tiles.append(Piece('O'))
        for t in range(9):
            tiles.append(Piece('T'))
        for r in range(9):
            tiles.append(Piece('R'))
        for n in range(8):
            tiles.append(Piece('N'))
        for d in range(6):
            tiles.append(Piece('D'))
        for s in range(6):
            tiles.append(Piece('S'))
        for u in range(6):
            tiles.append(Piece('U'))
        for l in range(5):
            tiles.append(Piece('L'))
        for g in range(4):
            tiles.append(Piece('G'))
        for b in range(3):
            tiles.append(Piece('B'))
        for c in range(3):
            tiles.append(Piece('C'))
        for f in range(3):
            tiles.append(Piece('F'))
        for h in range(3):
            tiles.append(Piece('H'))
        for m in range(3):
            tiles.append(Piece('M'))
        for p in range(3):
            tiles.append(Piece('P'))
        for v in range(3):
            tiles.append(Piece('V'))
        for w in range(3):
            tiles.append(Piece('W'))
        for y in range(3):
            tiles.append(Piece('Y'))
        random.shuffle(tiles)
        self.secret_tiles = tiles

    def create_tiles(self):
        tiles = []
        for j in range(2):
            tiles.append(Piece('J'))
        for k in range (2):
            tiles.append(Piece('K'))
        for q in range (2):
            tiles.append(Piece('Q'))
        for x in range (2):
            tiles.append(Piece('X'))
        for z in range (2):
            tiles.append(Piece('Z'))
        for e in range (18):
            tiles.append(Piece('E'))
        for k in range (13):
            tiles.append(Piece('A'))
        for i in range (12):
            tiles.append(Piece('I'))
        for o in range (11):
            tiles.append(Piece('O'))
        for t in range (9):
            tiles.append(Piece('T'))
        for r in range (9):
            tiles.append(Piece('R'))
        for n in range (8):
            tiles.append(Piece('N'))
        for d in range (6):
            tiles.append(Piece('D'))
        for s in range (6):
            tiles.append(Piece('S'))
        for u in range (6):
            tiles.append(Piece('U'))
        for l in range (5):
            tiles.append(Piece('L'))
        for g in range (4):
            tiles.append(Piece('G'))
        for b in range (3):
            tiles.append(Piece('B'))
        for c in range (3):
            tiles.append(Piece('C'))
        for f in range (3):
            tiles.append(Piece('F'))
        for h in range (3):
            tiles.append(Piece('H'))
        for m in range (3):
            tiles.append(Piece('M'))
        for p in range (3):
            tiles.append(Piece('P'))
        for v in range (3):
            tiles.append(Piece('V'))
        for w in range (3):
            tiles.append(Piece('W'))
        for y in range (3):
            tiles.append(Piece('Y'))

        random.shuffle(tiles)

        #self.tiles = tiles
        self.tiles = tiles[:77]

    def deal_inital(self):
        i = 0
        while i < 15:
            tile = self.tiles[0]
            self.player1_hand.append(tile)
            self.tiles.pop(0)
            i += 1

        k = 0
        while k < 15:
            tile = self.tiles[0]
            self.player2_hand.append(tile)
            self.tiles.pop(0)
            k += 1

    def player1_hand_to_list_of_letters(self):
        list_of_letters = []
        for i in self.player1_hand:
            if i == 0:
                list_of_letters.append(0)
            else:
                list_of_letters.append(i.letter)

        return list_of_letters

    def player2_hand_to_list_of_letters(self):
        list_of_letters = []
        for i in self.player2_hand:
            if i == 0:
                list_of_letters.append(0)
            else:
                list_of_letters.append(i.letter)

        return list_of_letters


    def player1_hand_to_list_of_letters_no_zero(self):
        list_of_letters = []
        for i in self.player1_hand:
            if i != 0:
                list_of_letters.append(i.letter)
        return list_of_letters


    def create_board(self):
        for row in range(15):
            self.board.append([])
            for col in range(15):
                    self.board[row].append(None)

        self.board.append([])
        for col in range(len(self.player1_hand)):
            self.board[15].append(self.player1_hand[col])
            self.player1_hand[col].set_row_col(15, col)

        for row in range(15):
            self.player2_board.append([])
            for col in range(15):
                    self.player2_board[row].append(None)

        self.player2_board.append([])

        for col in range(len(self.player2_hand)):
            self.player2_board[15].append(self.player2_hand[col])
            self.player2_hand[col].player2_set_row_col(15, col)


    def get_piece(self, row, col):
        return self.board[row][col]

    def player2_get_piece(self, row, col):
        return self.player2_board[row][col]

    def draw(self, win):
        self.draw_squares(win)

        for row in range(16):
            for col in range(15):
                piece = self.board[row][col]
                if piece != None:
                    if piece != 0:
                        piece.draw(win)

        for row in range(16):
            for col in range(15):
                piece = self.player2_board[row][col]
                if piece != None:
                    if piece != 0:
                        piece.draw(win)



