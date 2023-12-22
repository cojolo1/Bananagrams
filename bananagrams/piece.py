from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN, BLACK, LETTERCOLOR
import pygame

class Piece:
    PADDING = 15
    OUTLINE = 2
    def __init__(self, letter):
        self.row = None
        self.col = None
        self.letter = letter
        self.x = None
        self.y = None
        #self.calc_pos()
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def player2_set_row_col(self, row, col):
        self.row = row
        self.col = col
        self.player2_calc_pos()

    def set_row_col(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def player2_calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 + SQUARE_SIZE * 16
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def set_row_col_without_calc(self, row, col):
        self.row = row
        self.col = col

    def draw(self, win):
        pygame.init()
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(self.letter, True, LETTERCOLOR)
        textRect = text.get_rect()
        textRect.center = (self.x, self.y)
        pygame.draw.rect(win, RED, (self.x - SQUARE_SIZE // 2, self.y - SQUARE_SIZE // 2, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(win, LETTERCOLOR, (self.x - SQUARE_SIZE // 2, self.y - SQUARE_SIZE // 2, SQUARE_SIZE, SQUARE_SIZE), 1)
        win.blit(text, textRect)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def player2_move(self, row, col):
        self.row = row
        self.col = col
        self.player2_calc_pos()

    def __repr__(self):
        return str(self.letter)
