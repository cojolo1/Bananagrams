from letter_tree import basic_english
from alg_board import sample_board
import random
class SolveState:
    def __init__(self, dictionary, board, rack):
        self.dictionary = dictionary
        self.board = board
        self.rack = rack
        self.cross_check_results = None
        self.direction = None
        self.valid_starters = []
        self.valid_boards = []
        self.board_if_we_played_that_word = []
    def before(self, pos):
        row, col = pos
        if self.direction == 'across':
            return row, col - 1
        else:
            return row - 1, col

    def after(self, pos):
        row, col = pos
        if self.direction == 'across':
            return row, col + 1
        else:
            return row + 1, col

    def before_cross(self, pos):
        row, col = pos
        if self.direction == 'across':
            return row - 1, col
        else:
            return row, col - 1

    def after_cross(self, pos):
        row, col = pos
        if self.direction == 'across':
            return row + 1, col
        else:
            return row, col + 1

    def legal_move(self, word, last_pos):

        board_if_we_played_that = self.board.copy()
        play_pos = last_pos
        word_idx = len(word) - 1
        while word_idx >= 0:
            board_if_we_played_that.set_tile(play_pos, word[word_idx])
            word_idx -= 1
            play_pos = self.before(play_pos)

        self.valid_boards.append(board_if_we_played_that)
        board_if_we_played_that.get_tiles()[15][0] = word


    def pic_board_with_trouble_letter(self, letter, hand):
        board_with_trouble_letter = None

        print("The trouble letter is: ", letter)
        for i in self.valid_boards:
            if "q" in i.get_tiles()[15][0] and "Q" in hand:
                return i
            elif "z"in i.get_tiles()[15][0] and "Z" in hand:
                return i
            elif "j"in i.get_tiles()[15][0] and "J" in hand:
                return i
            elif "v"in i.get_tiles()[15][0] and "V" in hand:
                return i
            elif "y"in i.get_tiles()[15][0] and "Y" in hand:
                return i
            if letter.lower() in i.get_tiles()[15][0]:
                return i

        if board_with_trouble_letter == None:
            print("No Boards With Trouble Letter")
            return self.pic_random_board()
        else:
            return board_with_trouble_letter

    def pic_random_board(self):
        random.seed(None)
        random.shuffle(self.valid_boards)
        board_to_return = self.valid_boards[0]
        # self.valid_boards.pop(0)
        return board_to_return

    def pick_random_start(self):
        random.shuffle(self.valid_starters)
        return self.valid_starters[0]

    def initial_legal_move(self, word):
        if len(self.valid_starters) == 0:
            if len(word) > 3 and len(word) < 16:
                self.valid_starters.append(word)
        else:
            if len(word) > 5 and len(word) < 16:
                self.valid_starters.append(word)

    def intial_all_words(self, partial_word, current_node):
        list_of_valid_starter_words = []
        if current_node.is_word:
            self.initial_legal_move(partial_word)
        for next_letter in current_node.children.keys():
            if next_letter in self.rack:
                self.rack.remove(next_letter)
                self.intial_all_words(
                    partial_word + next_letter,
                    current_node.children[next_letter]
                )
                self.rack.append(next_letter)
        return list_of_valid_starter_words

    def initial_find_all_options(self):
        self.intial_all_words("", self.dictionary.root)

    def cross_check(self):
        result = dict()
        for pos in self.board.all_positions():
            if self.board.is_filled(pos):
                continue
            letters_before = ""
            scan_pos = pos
            while self.board.is_filled(self.before_cross(scan_pos)):
                scan_pos = self.before_cross(scan_pos)
                letters_before = self.board.get_tile(scan_pos) + letters_before
            letters_after = ""
            scan_pos = pos
            while self.board.is_filled(self.after_cross(scan_pos)):
                scan_pos = self.after_cross(scan_pos)
                letters_after = letters_after + self.board.get_tile(scan_pos)
            if len(letters_before) == 0 and len(letters_after) == 0:
                legal_here = list('abcdefghijklmnopqrstuvwxyz')
            else:
                legal_here = []
                for letter in 'abcdefghijklmnopqrstuvwxyz':
                    word_formed = letters_before + letter + letters_after
                    if self.dictionary.is_word(word_formed):
                        legal_here.append(letter)
            result[pos] = legal_here
        return result

    def find_anchors(self):
        anchors = []
        for pos in self.board.all_positions():
            empty = self.board.is_empty(pos)
            neighbor_filled = self.board.is_filled(self.before(pos)) or \
                              self.board.is_filled(self.after(pos)) or \
                              self.board.is_filled(self.before_cross(pos)) or \
                              self.board.is_filled(self.after_cross(pos))
            if empty and neighbor_filled:
                anchors.append(pos)
        return anchors

    def before_part(self, partial_word, current_node, anchor_pos, limit):
        self.extend_after(partial_word, current_node, anchor_pos, False)
        if limit > 0:
            for next_letter in current_node.children.keys():
                if next_letter in self.rack:
                    self.rack.remove(next_letter)
                    self.before_part(
                        partial_word + next_letter,
                        current_node.children[next_letter],
                        anchor_pos,
                        limit - 1
                    )
                    self.rack.append(next_letter)

    def extend_after(self, partial_word, current_node, next_pos, anchor_filled):
        if not self.board.is_filled(next_pos) and current_node.is_word and anchor_filled:
            self.legal_move(partial_word, self.before(next_pos))
        if self.board.in_bounds(next_pos):
            if self.board.is_empty(next_pos):
                for next_letter in current_node.children.keys():
                    if next_letter in self.rack and next_letter in self.cross_check_results[next_pos]:
                        self.rack.remove(next_letter)
                        self.extend_after(
                            partial_word + next_letter,
                            current_node.children[next_letter],
                            self.after(next_pos),
                            True
                        )
                        self.rack.append(next_letter)
            else:
                existing_letter = self.board.get_tile(next_pos)
                if existing_letter in current_node.children.keys():
                    self.extend_after(
                        partial_word + existing_letter,
                        current_node.children[existing_letter],
                        self.after(next_pos),
                        True
                    )

    def find_all_options(self):
        for direction in ['across', 'down']:
            self.direction = direction
            anchors = self.find_anchors()
            self.cross_check_results = self.cross_check()
            for anchor_pos in anchors:
                if self.board.is_filled(self.before(anchor_pos)):
                    scan_pos = self.before(anchor_pos)
                    partial_word = self.board.get_tile(scan_pos)
                    while self.board.is_filled(self.before(scan_pos)):
                        scan_pos = self.before(scan_pos)
                        partial_word = self.board.get_tile(scan_pos) + partial_word
                    pw_node = self.dictionary.lookup(partial_word)
                    if pw_node is not None:
                        self.extend_after(
                            partial_word,
                            pw_node,
                            anchor_pos,
                            False
                        )
                else:
                    limit = 0
                    scan_pos = anchor_pos
                    while self.board.is_empty(self.before(scan_pos)) and self.before(scan_pos) not in anchors:
                        limit = limit + 1
                        scan_pos = self.before(scan_pos)
                    self.before_part("", self.dictionary.root, anchor_pos, limit)
