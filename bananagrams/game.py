import copy

import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, LETTERCOLOR, BLACK
from bananagrams.board import Board
from solver import SolveState
from alg_board import Alg_Board
from letter_tree import basic_english
from bananagrams.piece import Piece


class Game:

    def __init__(self, win):
        self.win = win
        self._init()

        self.previous_hand = []
        self.previous_board = []


        self.previous_boards = []
        self.previous_hands = []
        self.previous_hands_tiles = []

        self.trouble_words = []
        self.most_common_trouble_letters = []
        self.backtracker_called_count = 0
        self.secret_dump_called_count = 0
        self.secret_secret_dump_called_count = 0
        self.desired_valid_boards = 30

        self.inital_play = True
        self.second_play = True
        self.is_peel = False
        self.is_dump = False
        self.game_over = False
        self.found_board = True

    def _init(self):
        self.selected = None
        self.board = Board(self.win)

    def ai_rearrange_board(self):
        pass

    def find_most_troublesome_word(self):
        return max(set(self.trouble_words), key=self.trouble_words.count)

    def find_ultimate_troublesome_word(self):
        return max(set(self.most_common_trouble_letters), key=self.most_common_trouble_letters.count)

    def ai_dump(self):
        print("Dump!")
        if len(self.board.tiles) > 3:
            trouble_letter = self.find_most_troublesome_word()

            for x in range(len(self.board.player1_hand)):
                if self.board.player1_hand[x] != 0:
                    if self.board.player1_hand[x].letter == trouble_letter:

                        print("Dumping: " + self.board.player1_hand[x].letter)
                        # Take the element at the filled position and reset it col/row
                        self.board.player1_hand[x].set_row_col_without_calc(None, None)

                        # Take the element at the filled position and place it back in the tiles pile
                        self.board.tiles.append(self.board.player1_hand[x])

                        # Replace the element at the filled position with 0 in the player's hand
                        self.board.player1_hand[x] = 0

                        # Replace the element at the filled position with None on the actual board
                        self.board.board[15][x] = None
                        break

            empty_position = None
            filled_position = None
            k = 0
            j = 0

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
            # self.trouble_words = []
            self.backtracker_called_count = 0
            self.secret_dump_called_count += 1

        else:
            print("Secret Dump")
            self.backtracker_called_count = 0
            self.secret_dump_called_count += 1

    def tiles_board_to_list_of_letters(self, board):
        list_of_letters = []
        for i in range(15):
            for j in range(15):
                if board[i][j] != None:
                    list_of_letters.append(board[i][j].upper())
        return list_of_letters

    def board_to_p1_board_hand(self):
        list_of_letters = []
        for i in range(len(self.board.board[15])):
            if self.board.board[15][i] != None:
                list_of_letters.append(self.board.board[15][i].letter)
        return list_of_letters

    def board_to_list_of_letters(self, board):
        list_of_letters = []
        for i in range(15):
            for j in range(15):
                if board[i][j] != None:
                    list_of_letters.append(board[i][j].letter)
        return list_of_letters

    def backtracker(self):

        self.backtracker_called_count += 1
        print("Backtracker called")
        board_before = self.board_to_list_of_letters(self.board.board)
        hand_before = copy.deepcopy(self.board.player1_hand)

        if self.secret_dump_called_count < 1:
            print("Keeping valid boards at 20")
            self.desired_valid_boards = 50
        elif self.secret_secret_dump_called_count > 1:
            print("Changing Valid Boards to 400")
            self.trouble_words = []
            self.desired_valid_boards = 600
            self.secret_secret_dump_called_count = 0
        else:
            print("Changing Valid Boards to 200")
            self.desired_valid_boards = 200
            self.secret_dump_called_count = 0
            self.secret_secret_dump_called_count += 1

        if self.found_board == False:
            print("Found Board is False")
            self.desired_valid_boards = 40

        self.found_board = False
        steps_back = 0

        for board_num in reversed(range(len(self.previous_boards))):
            print("Steps Back:", steps_back)
            print("Now on board: ", board_num + 1)

            current_hand = []
            for k in self.previous_hands[board_num]:
                if k != 0:
                    current_hand.append(k.letter.lower())


            board_to_parse = Alg_Board(15)
            for i in range(15):
                for j in range(15):
                    if self.previous_boards[board_num][i][j] != None and self.previous_boards[board_num][i][j] != 0:
                        board_to_parse.set_tile((i, j), self.previous_boards[board_num][i][j].letter.lower())

            # found_board = False

            solver = SolveState(basic_english(), board_to_parse, current_hand)
            solver.find_all_options()


            if len(solver.valid_boards) < self.desired_valid_boards:
                steps_back += 1


                continue
            else:
                self.found_board = True
                if self.desired_valid_boards == 200:
                    print("The total valid boards is", len(solver.valid_boards))
                    print("Changing Valid Boards to 30")
                    self.desired_valid_boards = 50
                elif self.desired_valid_boards == 600:
                    print("The total valid boards is", len(solver.valid_boards))
                    print("Changing Valid Boards to 30")
                    self.desired_valid_boards = 50
                """New Test Code Begin"""

                new_board = self.previous_boards[board_num]
                new_hand = self.previous_hands[board_num]

                board_before = self.board_to_list_of_letters(self.board.board)
                board_after = self.board_to_list_of_letters(self.previous_boards[board_num])

                if len(board_after) > len(board_before):
                    print("Case 1")
                else:
                    print("Case 2")
                    newly_removed_letters = [ele for ele in board_before]

                    for a in board_after:
                        if a in board_before:
                            newly_removed_letters.remove(a)


                    for i in range(len(newly_removed_letters)):
                        piece_to_put_back = Piece(newly_removed_letters[i].upper())
                        hand_before.append(piece_to_put_back)
                        empty_spot = False
                        for k in range(15):
                            if new_board[15][k] == None:
                                new_board[15][k] = piece_to_put_back
                                piece_to_put_back.set_row_col(15,k)
                                empty_spot = True

                    while hand_before.count(0):
                        hand_before.remove(0)

                    if len(hand_before) < 15:
                        to_add = 15 - len(hand_before)
                        for i in range(to_add):
                            hand_before.append(0)

                    self.board.board = copy.deepcopy(new_board)
                    self.board.board[15] = copy.deepcopy(hand_before)

                    while self.board.board[15].count(0):
                        self.board.board[15].remove(0)

                    for i in range(len(self.board.board[15])):
                        self.board.board[15][i].move(15,i)

                    if len(self.board.board[15]) < 15:
                        to_add = 15 - len(self.board.board[15])
                        for i in range(to_add):
                            self.board.board[15].append(None)

                    self.board.player1_hand = copy.deepcopy(hand_before)

                del self.previous_boards[board_num + 1:]
                del self.previous_hands[board_num + 1:]
                del self.previous_hands_tiles[board_num + 1:]
            print("Break")
            break

        self.update("")

    def ai_normal_play(self):
        if self.check_game_over():
            return True

        current_hand = []
        for i in self.board.player1_hand:
            if i != 0:
                current_hand.append(i.letter.lower())

        actual_hand = copy.deepcopy(self.board.player1_hand)
        actual_board = copy.deepcopy(self.board.board)
        self.previous_hands.append(actual_hand)
        self.previous_boards.append(actual_board)
        self.previous_hands_tiles.append(self.board_to_list_of_letters(self.board.board))
        self.previous_hand = copy.deepcopy(self.board.player1_hand)
        self.previous_board = copy.deepcopy(self.board.board)
        board_before = self.board_to_list_of_letters(self.board.board)

        board_to_parse = Alg_Board(15)
        for i in range(15):
            for j in range(15):
                if self.board.board[i][j] != None and self.board.board[i][j] != 0:
                    board_to_parse.set_tile((i, j), self.board.board[i][j].letter.lower())

        solver = SolveState(basic_english(), board_to_parse, current_hand)
        solver.find_all_options()
        if self.inital_play:
            print("The Valid Boards After Initial Play", len(solver.valid_boards))
            self.inital_play = False

        if len(self.board.player1_hand_to_list_of_letters_no_zero()) == 0:

            self.peel()

        elif self.backtracker_called_count > 4:
            self.ai_dump()

        elif len(solver.valid_boards) == 0:
            self.backtracker()


        else:

            print("Normal Play")
            print("Valid Board Length")
            print(len(solver.valid_boards))

            if self.second_play:
                new_board_tiles = solver.pic_random_board().get_tiles()
                self.second_play = False
            else:
                self.most_common_trouble_letters.append(self.find_most_troublesome_word())
                new_board_tiles = solver.pic_board_with_trouble_letter(self.find_most_troublesome_word()).get_tiles()
                # self.trouble_words = []
                self.second_play = True


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
        # self.trouble_words.append(self.board.player1_hand[0].letter)
        for i in self.board.player1_hand:
            if i != None and i != 0:
                self.trouble_words.append(i.letter)
                break

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
        if len(self.board.tiles) > 0:
            for i in range(len(self.board.board[15])):
                if self.board.board[15][i] == None:
                    self.board.board[15][i] = self.board.tiles[0]
                    self.board.board[15][i].move(15, i)
                    self.board.player1_hand[i] = self.board.board[15][i]
                    self.board.tiles.pop(0)


                    if len(self.board.tiles) > 1:
                        k = 0
                        for i in range(len(self.board.player2_hand)):
                            if self.board.player2_hand[i] == 0 and k < 1:
                                self.board.player2_board[15][i] = self.board.tiles[0]
                                self.board.player2_board[15][i].player2_move(15, i)
                                self.board.player2_hand[i] = self.board.player2_board[15][i]
                                self.board.tiles.pop(0)
                                k += 1
                        break

                    break


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
        if len(self.board.tiles) > 3:
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
        textRect.center = (1063, 810)
        self.win.blit(text, textRect)

        text2 = font.render("Remaining Tiles: " + str(len(self.board.tiles)), True, LETTERCOLOR)
        textRect2 = text2.get_rect()
        textRect2.center = (697.5, 760)
        self.win.blit(text2, textRect2)

        font2 = pygame.font.Font('freesansbold.ttf', 32)
        text4 = font2.render("Your Board",True, LETTERCOLOR)
        textRect4 = text4.get_rect()
        textRect4.center = (1056.25, 760)

        pygame.draw.rect(self.win, RED, (955, 740, 200, 40), )
        pygame.draw.rect(self.win, LETTERCOLOR, (955, 740, 200, 40), 1)
        self.win.blit(text4, textRect4)

        if self.game_over:
            pygame.draw.rect(self.win, RED, (325, 375, 750, 100))
            pygame.draw.rect(self.win, LETTERCOLOR,(325, 375, 750, 100), 1)
            font = pygame.font.Font('freesansbold.ttf', 78)
            text3 = font.render("BANANAGRAMS!", True, LETTERCOLOR)
            textRect3 = text3.get_rect()
            textRect3.center = (697.5, 425)
            self.win.blit(text3, textRect3)



        # if self.is_peel:
        #     pygame.draw.rect(self.win, RED, (325, 375, 750, 100))
        #     pygame.draw.rect(self.win, LETTERCOLOR, (325, 375, 750, 100), 1)
        #     font = pygame.font.Font('freesansbold.ttf', 78)
        #     text3 = font.render("PEEL!", True, LETTERCOLOR)
        #     textRect3 = text3.get_rect()
        #     textRect3.center = (697.5, 425)
        #     self.win.blit(text3, textRect3)
        #     self.is_peel = False

        #
        # if self.is_dump:
        #     pygame.draw.rect(self.win, RED, (325, 375, 750, 100))
        #     pygame.draw.rect(self.win, LETTERCOLOR, (325, 375, 750, 100), 1)
        #     font = pygame.font.Font('freesansbold.ttf', 78)
        #     text3 = font.render("DUMP!", True, LETTERCOLOR)
        #     textRect3 = text3.get_rect()
        #     textRect3.center = (697.5, 425)
        #     self.win.blit(text3, textRect3)
        pygame.display.update()

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
            print("Game Over is True")
            return True


    def _move(self, row, col):
        piece = self.board.player2_get_piece(row, col)
        if self.selected and piece == None:
            self.board.move_by_click(self.selected, row, col)
        else:
            return False
        return True
