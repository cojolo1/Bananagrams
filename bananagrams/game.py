import copy

import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, LETTERCOLOR
from bananagrams.board import Board
from solver import SolveState
from alg_board import Alg_Board
from letter_tree import basic_english
from bananagrams.piece import Piece


class Game:

    def __init__(self, win):
        self.win = win
        self._init()
        self.backupboard = []
        self.previous_hand = []
        self.previous_board = []
        self.is_peel = False
        self.is_dump = False
        self.game_over = False

    def _init(self):
        self.selected = None
        self.board = Board(self.win)

    def ai_rearrange_board(self):
        pass
    def ai_dump(self):
        print("Dump!")
        if len(self.board.tiles) > 3:

            empty_position = None
            filled_position = None
            k = 0
            j = 0
            for i in self.board.player1_hand:
                if i != 0 and j < 1:

                    filled_position = self.board.player1_hand.index(i)
                    # Take the element at the filled position and reset it col/row
                    self.board.player1_hand[filled_position].set_row_col_without_calc(None, None)
                    # Take the element at the filled position and place it back in the tiles pile
                    self.board.tiles.append(self.board.player1_hand[filled_position])
                    # Replace the element at the filled position with 0 in the player's hand
                    self.board.player1_hand[filled_position] = 0
                    # Replace the element at the filled position with None on the actual board
                    self.board.board[15][filled_position] = None
                    j += 1
            for i in self.board.player1_hand:
                if i == 0 and k < 3:

                    empty_position = self.board.player1_hand.index(i)
                    # Replace the first empty position in the players hand with the first tile from the board
                    self.board.player1_hand[empty_position] = self.board.tiles[0]
                    # Remove the take tile from tile of piles
                    self.board.tiles.pop(0)
                    # Set row/col of new piece
                    self.board.player1_hand[empty_position].set_row_col(15, empty_position)
                    # Set tile on the actual board
                    self.board.board[15][empty_position] = self.board.player1_hand[empty_position]
                    k += 1

            self.update("")
        else:
            empty_position = None
            filled_position = None
            k = 0
            j = 0
            for i in self.board.player1_hand:
                if i != 0 and j < 1:
                    # print("The letter you are dumping is: ")
                    # print(i.letter)
                    filled_position = self.board.player1_hand.index(i)
                    # Take the element at the filled position and reset it col/row
                    self.board.player1_hand[filled_position].set_row_col_without_calc(None, None)
                    # Take the element at the filled position and place it back in the tiles pile
                    self.board.secret_tiles.append(self.board.player1_hand[filled_position])
                    # Replace the element at the filled position with 0 in the player's hand
                    self.board.player1_hand[filled_position] = 0
                    # Replace the element at the filled position with None on the actual board
                    self.board.board[15][filled_position] = None
                    j += 1
            for i in self.board.player1_hand:
                if i == 0 and k < 3:

                    empty_position = self.board.player1_hand.index(i)
                    # empty_positions.append(self.board.player1_hand.index(i))

                    # Replace the first empty position in the players hand with the first tile from the board
                    self.board.player1_hand[empty_position] = self.board.secret_tiles[0]
                    # Remove the take tile from tile of piles
                    self.board.secret_tiles.pop(0)
                    # Set row/col of new piece
                    self.board.player1_hand[empty_position].set_row_col(15, empty_position)
                    # Set tile on the actual board
                    self.board.board[15][empty_position] = self.board.player1_hand[empty_position]
                    k += 1

            self.update("")

    def board_to_list_of_letters(self, board):
        list_of_letters = []
        for i in range(15):
            for j in range(15):
                if board[i][j] != None:
                    list_of_letters.append(board[i][j].letter)
        return list_of_letters

    def ai_normal_play(self):

        current_hand = []
        for i in self.board.player1_hand:
            if i != 0:
                current_hand.append(i.letter.lower())

        self.previous_hand = copy.deepcopy(self.board.player1_hand)
        self.previous_board = copy.deepcopy(self.board.board)
        board_before = self.board_to_list_of_letters(self.board.board)

        board_to_parse = Alg_Board(15)
        for i in range(15):
            for j in range(15):
                if self.board.board[i][j] != None and self.board.board[i][j] != 0:
                    # if self.board.board[i][j] != 0:
                    board_to_parse.set_tile((i, j), self.board.board[i][j].letter.lower())

        solver = SolveState(basic_english(), board_to_parse, current_hand)
        solver.find_all_options()
        print("Length of Valid Boards")
        print(len(solver.valid_boards))

        if len(self.board.player1_hand_to_list_of_letters_no_zero()) == 0:
            self.peel()

        elif len(solver.valid_boards) > 2 and len(solver.valid_boards) < 7:
            self.ai_backup_play()

        elif len(solver.valid_boards) < 2:
            self.ai_dump()

        else:
            new_board_tiles = solver.pic_random_board().get_tiles()

            if len(solver.valid_boards) > 0:
                for q in range(len(solver.valid_boards)):
                    self.backupboard.append(solver.pic_random_board().get_tiles())

            for i in range(15):
                for j in range(15):
                    if new_board_tiles[i][j] != None:
                        piece = Piece(new_board_tiles[i][j].upper())
                        piece.set_row_col(i, j)
                        self.board.board[i][j] = piece

            board_after = self.board_to_list_of_letters(self.board.board)

            newly_added_letters = [ele for ele in board_after]
            for a in board_before:
                if a in board_after:
                    newly_added_letters.remove(a)
            for i in range(len(newly_added_letters)):

                self.board.player1_hand[self.board.player1_hand_to_list_of_letters().index(newly_added_letters[i])] = 0

                for k in range(15):
                    if self.board.board[15][k] != None and self.board.board[15][k] != 0:
                        if self.board.board[15][k].letter == newly_added_letters[i]:
                            self.board.board[15][k] = None
                            break

            self.update("")


    def ai_backup_play(self):

        self.board.player1_hand = copy.deepcopy(self.previous_hand)
        self.board.board = copy.deepcopy(self.previous_board)
        board_before = self.board_to_list_of_letters(self.board.board)

        current_hand = []
        for i in self.board.player1_hand:
            if i != 0:
                current_hand.append(i.letter.lower())

        board_to_parse = Alg_Board(15)
        for i in range(15):
            for j in range(15):
                if self.board.board[i][j] != None and self.board.board[i][j] != 0:
                    # if self.board.board[i][j] != 0:
                    board_to_parse.set_tile((i, j), self.board.board[i][j].letter.lower())

        solver = SolveState(basic_english(), board_to_parse, current_hand)
        solver.find_all_options()

        new_board_tiles = solver.pic_random_board().get_tiles()

        if len(solver.valid_boards) > 0:
            for q in range(len(solver.valid_boards)):
                self.backupboard.append(solver.pic_random_board().get_tiles())

        for i in range(15):
            for j in range(15):
                if new_board_tiles[i][j] != None:
                    piece = Piece(new_board_tiles[i][j].upper())
                    piece.set_row_col(i, j)
                    self.board.board[i][j] = piece

        board_after = self.board_to_list_of_letters(self.board.board)

        newly_added_letters = [ele for ele in board_after]
        for a in board_before:
            if a in board_after:
                newly_added_letters.remove(a)

        for i in range(len(newly_added_letters)):

            self.board.player1_hand[self.board.player1_hand_to_list_of_letters().index(newly_added_letters[i])] = 0

            for k in range(15):
                if self.board.board[15][k] != None and self.board.board[15][k] != 0:
                    if self.board.board[15][k].letter == newly_added_letters[i]:
                        self.board.board[15][k] = None
                        break

        self.update("")

    def ai_play(self):
        """Do not mess with this one"""
        current_hand = []
        for i in self.board.player1_hand:
            if i != 0:
                current_hand.append(i.letter.lower())

        board_to_parse = Alg_Board(15)
        for i in range(15):
            for j in range(15):
                if self.board.board[i][j] != None and self.board.board[i][j] != 0:
                    # if self.board.board[i][j] != 0:
                    board_to_parse.set_tile((i, j), self.board.board[i][j].letter.lower())

        solver = SolveState(basic_english(), board_to_parse, current_hand)
        solver.find_all_options()

        if len(self.board.player1_hand_to_list_of_letters_no_zero()) == 0:
            self.peel()
        elif len(solver.valid_boards) == 0:
            self.ai_dump()

        else:
            self.backupboard = solver.pic_random_board().get_tiles()
            new_board_tiles = solver.pic_random_board().get_tiles()

            for i in range(15):
                for j in range(15):
                    if new_board_tiles[i][j] != None:
                        piece = Piece(new_board_tiles[i][j].upper())
                        piece.set_row_col(i,j)
                        self.board.board[i][j] = piece

                        for k in range(15):
                            if self.board.board[15][k] != None and self.board.board[15][k] != 0:
                                if self.board.board[15][k].letter == new_board_tiles[i][j].upper():
                                    self.board.board[15][k] = None
                                    self.board.player1_hand[k] = 0

                                    #New addition

                                    break

                self.update("")


    def do_nothing(self):
        print()

    def ai_inital_play(self):
        current_hand = []
        for i in self.board.player1_hand:
            current_hand.append(i.letter.lower())
        board_to_parse = Alg_Board(15)


        solver = SolveState(basic_english(), board_to_parse, current_hand)
        solver.initial_find_all_options()
        random_start_word = solver.pick_random_start()

        self.ai_place_word(random_start_word, 7, 3, "RIGHT")


    def peel(self):
        self.is_peel = True
        print("Peel!")
        self.board.board[15][0] = self.board.tiles[0]
        self.board.board[15][0].move(15, 0)
        self.board.player1_hand[0] = self.board.board[15][0]
        self.board.tiles.pop(0)

        k = 0
        for i in range(len(self.board.player2_hand)):

            if self.board.player2_hand[i] == 0 and k < 1:
                self.board.player2_board[15][i] = self.board.tiles[0]
                self.board.player2_board[15][i].player2_move(15, i)
                self.board.player2_hand[i] = self.board.player2_board[15][i]
                self.board.tiles.pop(0)
                k += 1


    def human_peel(self):
        if self.board.player2_board[15][0] == None and self.board.player2_board[15][1] == None and self.board.player2_board[15][2] == None and self.board.player2_board[15][3] == None and self.board.player2_board[15][4] == None \
                and self.board.player2_board[15][5] == None and self.board.player2_board[15][6] == None and self.board.player2_board[15][7] == None and self.board.player2_board[15][8] == None and self.board.player2_board[15][9] == None \
                and self.board.player2_board[15][10] == None  and self.board.player2_board[15][11] == None and self.board.player2_board[15][12] == None and self.board.player2_board[15][13] == None and self.board.player2_board[15][14] == None and len(self.board.tiles) > 0:

            self.board.player2_board[15][0] = self.board.tiles[0]
            self.board.player2_board[15][0].player2_move(15,0)
            self.board.player2_hand[0] = self.board.player2_board[15][0]

            self.board.tiles.pop(0)



            k = 0
            for i in range(len(self.board.player1_hand)):
                if self.board.player1_hand[i] == 0 and k < 1:
                    self.board.board[15][i] = self.board.tiles[0]
                    self.board.board[15][i].move(15, i)
                    self.board.player1_hand[i] = self.board.board[15][i]
                    self.board.tiles.pop(0)
                    k += 1

    def human_dump(self, row, col):
        empty_count = 0
        for q in self.board.player2_hand:
            if q == 0:
                empty_count += 1

        if row == 15 and col >= 0 and col < 15 and self.board.player2_hand[col] != 0 and empty_count >= 2:

            self.board.player2_hand[col].set_row_col_without_calc(None, None)
            self.board.tiles.append(self.board.tiles.append(self.board.player2_hand[col]))
            self.board.player2_hand[col] = 0
            self.board.player2_board[15][col] = None

            q = 0
            for i in range(15):
                if self.board.player2_hand[i] == 0 and q < 3:
                    self.board.player2_board[15][i] = self.board.tiles[0]
                    self.board.player2_board[15][i].player2_move(15, i)
                    self.board.player2_hand[i] = self.board.player2_board[15][i]
                    self.board.tiles.pop(0)
                    q += 1


                        # i = self.board.tiles[0]
                        # self.board.tiles.pop(0)

        # self.update("")



    def get_board(self):
        return self.board.board
    def player2_get_board(self):
        return self.board.player2_board

    def place_word(self, letter, row, col, direction):
        letter = letter.upper()
        has_letters = True
        player2_letter_hand = self.board.player2_hand_to_list_of_letters()

        for i in letter:
            if i not in player2_letter_hand or letter.count(i) > player2_letter_hand.count(i):
                has_letters = False
        if has_letters == True and len(letter) > 0:
            if direction == "RIGHT":
                k = 0
                for i in letter:

                    player2_letter_hand = self.board.player2_hand_to_list_of_letters()
                    if row < 15 and row >= 0 and col + k < 15 and col + k >= 0:
                        if self.board.player2_board[row][col + k] == None:
                            self.board.move(self.board.player2_hand[player2_letter_hand.index(i)], row, col + k)
                    k += 1

            else:
                k = 0
                for i in letter:
                    player2_letter_hand = self.board.player2_hand_to_list_of_letters()

                    if row + k < 15  and row + k >= 0 and col < 15 and col >= 0:
                        if self.board.player2_board[row + k][col] == None:
                            self.board.move(self.board.player2_hand[player2_letter_hand.index(i)], row  + k, col)
                    k += 1

        player2_letter_hand = self.board.player2_hand_to_list_of_letters()
        # self.update("")

    def ai_place_word(self, letter, row, col, direction):

        letter = letter.upper()
        has_letters = True

        k = 0
        for i in letter:
            self.board.ai_move(self.board.player1_hand[self.board.player1_hand_to_list_of_letters().index(i)], row, col + k, 1)
            k += 1

        player1_letter_hand = self.board.player1_hand_to_list_of_letters()

    def update(self, user_txt):
        self.board.draw(self.win)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(user_txt.upper(), True, LETTERCOLOR)
        textRect = text.get_rect()
        textRect.center = (1046.25, 810)
        self.win.blit(text, textRect)

        text2 = font.render("Remaining Tiles: " + str(len(self.board.tiles)), True, LETTERCOLOR)
        textRect2 = text2.get_rect()
        textRect2.center = (697.5, 760)
        self.win.blit(text2, textRect2)

        if self.game_over:
            pygame.draw.rect(self.win, RED, (325, 375, 750, 100))
            pygame.draw.rect(self.win, LETTERCOLOR,(325, 375, 750, 100), 1)
            font = pygame.font.Font('freesansbold.ttf', 78)
            text3 = font.render("BANANAGRAMS!", True, LETTERCOLOR)
            textRect3 = text3.get_rect()
            textRect3.center = (697.5, 425)
            self.win.blit(text3, textRect3)

        if self.is_peel:
            pygame.draw.rect(self.win, RED, (325, 375, 750, 100))
            pygame.draw.rect(self.win, LETTERCOLOR, (325, 375, 750, 100), 1)
            font = pygame.font.Font('freesansbold.ttf', 78)
            text3 = font.render("PEEL!", True, LETTERCOLOR)
            textRect3 = text3.get_rect()
            textRect3.center = (697.5, 425)
            self.win.blit(text3, textRect3)
            self.is_peel = False


        if self.is_dump:
            pygame.draw.rect(self.win, RED, (325, 375, 750, 100))
            pygame.draw.rect(self.win, LETTERCOLOR, (325, 375, 750, 100), 1)
            font = pygame.font.Font('freesansbold.ttf', 78)
            text3 = font.render("DUMP!", True, LETTERCOLOR)
            textRect3 = text3.get_rect()
            textRect3.center = (697.5, 425)
            self.win.blit(text3, textRect3)


        pygame.display.update()

    def right_click_select(self, row, col):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pass



    def select(self, row, col):

        if self.selected:

            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.player2_get_piece(row, col)

        if piece != None:

            self.selected = piece
            return True
        return False

    def check_game_over(self):
        if len(self.board.tiles) < 1 and len(self.board.player1_hand_to_list_of_letters_no_zero()) == 0:
            return True

    def _move(self, row, col):
        piece = self.board.player2_get_piece(row, col)
        # piece = self.board.get_piece(row, col)
        if self.selected and piece == None:
            self.board.move_by_click(self.selected, row, col)
        else:
            return False
        return True
