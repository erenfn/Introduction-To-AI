from typing import Dict, Optional, Tuple, List
import copy
import sys
import math
DIMENSION = 8
STATE_DICT = {}


class Piece:
    """
    based on my CSC111 final project
    """
    is_crowned: bool
    red: bool
    position: str

    def __init__(self, is_red: bool, start_pos: str) -> None:
        self.is_crowned = False
        self.red = is_red
        self.position = start_pos

    def crown_piece(self) -> None:
        self.is_crowned = True


class Checkers:
    """
    based on my CSC111 final project
    """

    red_pieces: Dict[str, Piece]
    black_pieces: Dict[str, Piece]
    is_red_move: bool
    valid_positions: list

    def __init__(self, valid_positions: Optional[List] = None,
                 red: Optional[Dict[str, Piece]] = None,
                 black: Optional[Dict[str, Piece]] = None,
                 curr_player: Optional[bool] = None) -> None:

        if red is not None and black is not None and curr_player is not None and valid_positions is not None:
            self.red_pieces = red
            self.black_pieces = black
            self.is_red_move = curr_player
            self.valid_positions = valid_positions

        else:
            self.red_pieces = {}
            self.black_pieces = {}
            self.is_red_move = True
            self.valid_positions = []

    def get_winner(self) -> Optional[str]:
        if len(self.black_pieces) == 0:
            return 'red'
        elif len(self.red_pieces) == 0:
            return 'black'
        elif self.get_valid_moves() == []:
            if self.is_red_move:
                return 'black'
            else:
                return 'red'
        else:
            return None

    def make_move(self, move: tuple[str, str, str]) -> None:

        if self.is_red_move:
            piece = self.red_pieces[move[0]]
            if move[1] != '':

                self.capture(move[1])
            self.red_pieces[move[2]] = piece
            piece.position = move[2]
            self.red_pieces.pop(move[0])

        else:
            piece = self.black_pieces[move[0]]
            if move[1] != '':

                self.capture(move[1])

            self.black_pieces[move[2]] = piece
            piece.position = move[2]
            self.black_pieces.pop(move[0])

    def capture(self, position: str) -> None:
        if self.is_red_move:
            self.black_pieces.pop(position)
        else:
            self.red_pieces.pop(position)

    def get_neighbours(self, piece: Piece) -> list:

        position = piece.position

        top_right = chr(ord(position[0]) + 1) + str(int(position[1]) + 1)
        top_left = chr(ord(position[0]) - 1) + str(int(position[1]) + 1)
        bottom_right = chr(ord(position[0]) + 1) + str(int(position[1]) - 1)
        bottom_left = chr(ord(position[0]) - 1) + str(int(position[1]) - 1)

        corners = [top_right, top_left, bottom_right, bottom_left]
        neighbours_so_far = []
        for i in range(0, 4):

            if corners[i] not in self.valid_positions:
                neighbours_so_far.append(())

            elif (corners[i] not in self.red_pieces and
                  corners[i] not in self.black_pieces):
                neighbours_so_far.append(('none', corners[i]))

            elif corners[i] in self.red_pieces:
                if piece.red:
                    neighbours_so_far.append(('same', corners[i]))
                else:
                    neighbours_so_far.append(('diff', corners[i]))

            elif corners[i] in self.black_pieces:
                if piece.red:
                    neighbours_so_far.append(('diff', corners[i]))
                else:
                    neighbours_so_far.append(('same', corners[i]))
        return neighbours_so_far

    def get_valid_moves(self) -> List[tuple]:

        capture_moves = []
        non_capture_moves = []
        if self.is_red_move:
            pieces_to_check = [self.red_pieces[piece] for piece in self.red_pieces]
        else:
            pieces_to_check = [self.black_pieces[piece] for piece in self.black_pieces]
        for piece in pieces_to_check:
            moves, is_capture = self.get_valid_move_piece(piece)
            if is_capture:
                capture_moves.extend(moves)
            else:
                non_capture_moves.extend(moves)
        if capture_moves != []:
            return capture_moves
        else:
            return non_capture_moves

    def get_valid_move_piece(self, piece) -> Tuple[list, bool]:
        capture_moves = []
        non_capture_moves = []
        corners = self.get_neighbours(piece)

        if piece.red and not piece.is_crowned:
            start = 2
            end = 4

        elif not (piece.red or piece.is_crowned):
            start = 0
            end = 2

        else:
            start = 0
            end = 4
        for i in range(start, end):
            corner = corners[i]
            if corner == ():
                continue
            elif corner[0] == 'none':
                non_capture_moves.append((piece.position, '', corner[1]))
            elif corner[0] == 'diff':
                letter = chr(ord(corner[1][0]) - ord(piece.position[0]) + ord(corner[1][0]))
                num = str(int(corner[1][1]) - int(piece.position[1]) + int(corner[1][1]))
                check = letter + num
                if check not in self.red_pieces and check not in self.black_pieces and \
                        check in self.valid_positions:
                    capture_moves.append((piece.position, corner[1], check))
        if capture_moves != []:
            return (capture_moves, True)
        else:
            return (non_capture_moves, False)

    def heuristic3(self, move: tuple[str, str, str]) -> int:
        """
        Additional heuristic function that uses distance between a regular piece to become a crown,
        and the position of the crowned pieces (better if it is close to the center)
        """
        game = copy.deepcopy(self)
        game.make_move(move)
        red_value = 0
        black_value = 0

        for pos in game.red_pieces.keys():
            if game.red_pieces[pos].is_crowned:
                red_value += 18
            else:
                red_value += 8

        for pos in game.black_pieces.keys():
            if game.black_pieces[pos].is_crowned:
                black_value += 18
            else:
                black_value += 8

        return round(red_value - black_value)


def heuristic(game: Checkers) -> int:
    red_value = 0
    black_value = 0

    for pos in game.red_pieces.keys():
        if game.red_pieces[pos].is_crowned:
            red_value += 2
        else:
            red_value += 1

    for pos in game.black_pieces.keys():
        if game.black_pieces[pos].is_crowned:
            black_value += 2
        else:
            black_value += 1

    return red_value - black_value


# def heuristic2(game: Checkers) -> int:
#     """
#     Additional heuristic function that uses distance between a regular piece to become a crown,
#     and the position of the crowned pieces (better if it is close to the center)
#     :param game:
#     :return:
#     """
#     red_value = 0
#     black_value = 0
#
#     for pos in game.red_pieces.keys():
#         if game.red_pieces[pos].is_crowned:
#             red_value += 18 + 3 / (abs(4.5 - int(pos[1])) * abs(100.5 - ord(pos[0])))
#         else:
#             red_value += 16 - int(pos[1])
#
#     for pos in game.black_pieces.keys():
#         if game.black_pieces[pos].is_crowned:
#             black_value += 18 + 3 / (abs(4.5 - int(pos[1])) * abs(100.5 - ord(pos[0])))
#         else:
#             black_value += 8 + int(pos[1])
#
#     return round(red_value - black_value)



def alphabeta(game: Checkers, d: int, alpha=-math.inf, beta=math.inf) -> \
        Tuple[Optional[Tuple[str, str, str]], float]:

    player = game.is_red_move
    winner = game.get_winner()
    best_move = None

    if winner is not None:
        if winner == 'black':
            return best_move, -math.inf
        elif winner == 'red':
            return best_move, math.inf
        else:
            return best_move, heuristic(game)
    elif d == 0:
        return best_move, heuristic(game)

    if player:
        value = -math.inf
    else:
        value = math.inf

    # moves = sorted(game.get_valid_moves(), key=game.heuristic3)
    moves = game.get_valid_moves()

    for move in moves:
        new_game = copy.deepcopy(game)
        new_game.make_move(move)

        # does crowning
        if new_game.is_red_move:
            piece = new_game.red_pieces[move[2]]
            if not piece.is_crowned and move[2][1] == '1':
                piece.crown_piece()
        else:
            piece = new_game.black_pieces[move[2]]
            if not piece.is_crowned and move[2][1] == '8':
                piece.crown_piece()

        is_continued = False

        if move[1] != '':
            is_continued = new_game.get_valid_move_piece(piece)[1]

        if is_continued is not True:
            # Change who is current player
            new_game.is_red_move = not new_game.is_red_move

        if new_game in STATE_DICT.keys():
            pass
        else:
            n_v = alphabeta(new_game, d - 1, alpha, beta)[1]

            if player:
                if value < n_v:
                    value, best_move = n_v, move
                if value >= beta:
                    return best_move, value
                alpha = max(alpha, value)
            else:
                if value > n_v:
                    value, best_move = n_v, move
                if value <= alpha:
                    return best_move, value
                beta = min(beta, value)

    STATE_DICT[game] = value
    return best_move, value

def set_valid_pos(count: int, num: int) -> list:

    if (count + num) % 2 == 0:
        valid_positions = [letter + str(2 * x) for x in range(1, 5) for letter
                           in 'aceg'] + \
                          [letter + str(2 * x + 1) for x in range(0, 4) for
                           letter in 'bdfh']
    else:
        valid_positions = [letter + str(2 * x + 1) for x in range(0, 4) for letter
                           in 'aceg'] + \
                          [letter + str(2 * x) for x in range(1, 5) for
                           letter in 'bdfh']
    return valid_positions

def input_read(input: str, game: Checkers) -> list:
    with open(input) as f:
        lines = f.readlines()
        count = 1
        valid_pos_set = False
        valid_positions = []

        for line in lines:
            splitted = []
            splitted[:] = line

            for num in range(0, 8):
                if splitted[num] == 'b':
                    pos = chr(ord('a') + num) + str(count)
                    piece = Piece(False, pos)
                    game.black_pieces[pos] = piece
                    if not valid_pos_set:
                        valid_positions = set_valid_pos(count, num)
                        valid_pos_set = True

                elif splitted[num] == 'B':
                    pos = chr(ord('a') + num) + str(count)
                    piece = Piece(False, pos)
                    piece.crown_piece()
                    game.black_pieces[pos] = piece
                    if not valid_pos_set:
                        valid_positions = set_valid_pos(count, num)
                        valid_pos_set = True

                elif splitted[num] == 'r':
                    pos = chr(ord('a') + num) + str(count)
                    piece = Piece(True, pos)
                    game.red_pieces[pos] = piece
                    if not valid_pos_set:
                        valid_positions = set_valid_pos(count, num)
                        valid_pos_set = True
                elif splitted[num] == 'R':
                    pos = chr(ord('a') + num) + str(count)
                    piece = Piece(True, pos)
                    piece.crown_piece()
                    game.red_pieces[pos] = piece
                    if not valid_pos_set:
                        valid_positions = set_valid_pos(count, num)
                        valid_pos_set = True
            count += 1

    return valid_positions


def game_to_list(game: Checkers) -> List[List]:
    lst = []

    for _ in range(0, 8):
        lst2 = []
        for _ in range(0, 8):
            lst2.append('.')
        lst.append(lst2)

    for black_pos in game.black_pieces.keys():
        row = ord(black_pos[0]) - ord('a')
        piece = game.black_pieces[black_pos]
        if piece.is_crowned:
            lst[int(black_pos[1])-1][row] = 'B'
        else:
            lst[int(black_pos[1])-1][row] = 'b'

    for black_pos in game.red_pieces.keys():
        row = ord(black_pos[0]) - ord('a')
        piece = game.red_pieces[black_pos]
        if piece.is_crowned:
            lst[int(black_pos[1])-1][row] = 'R'
        else:
            lst[int(black_pos[1])-1][row] = 'r'

    return lst



def output_to_file(filename: str, game: Checkers) -> None:
    main_out = sys.stdout
    f = open(filename, 'w')
    sys.stdout = f

    game_list = game_to_list(game)

    for column in game_list:
        for row in column:
            print(row, end='')
        print()

    sys.stdout = main_out
    f.close()



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("length of sysargv should be 3")
        exit(1)
    input = sys.argv[1]
    output = sys.argv[2]

    # import time
    # start_time = time.time()
    #
    # input = "input0.txt"
    # output = "sol.txt"

    game = Checkers()
    valid_positions = input_read(input, game)
    game.valid_positions = valid_positions

    if game.get_winner() is None:
        depth = 10
        move = alphabeta(game, depth)[0]

        if move is not None:
            game.make_move(move)

    output_to_file(output, game)

    # print("--- %s seconds ---" % (time.time() - start_time))

