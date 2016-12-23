import sys


class Reversi:
    board = []
    best_move = None
    current_best_case = 0
    current_worst_case = sys.maxint
    current_player_turn = 'w'

    def __init__(self, parent=None, size=None):

        # setup board
        if parent:
            self.import_board(parent.board)

            # setup best move
            self.best_move = parent.best_move
            self.current_best_case = parent.current_best_case
            self.current_worst_case = parent.current_worst_case
            self.current_player_turn = parent.current_player_turn
            self.turns_taken = parent.turns_taken
            self.center_square = parent.center_square
        else:
            self.turns_taken = 0

            m = int((size / 2) - 1)
            self.center_square = [(m, m), (m+1, m), (m, m+1), (m+1, m+1)]

            self.board = []
            for x in range(size):
                self.board.append([None] * size)

    def import_board(self, board):
        self.board = []
        for line in board:
            new_line = []
            for square_value in line:
                new_line.append(square_value)
            self.board.append(new_line)

    # this method will recursively calculate the best possible move for the current player
    # and return it
    def get_optimal_move(self):
        pass  # todo

    def __str__(self):
        cell_width = 10
        result = "\n" + " " * int(cell_width * 1.5)
        for x in range(len(self.board)):
            result += str(x).ljust(cell_width)
        result += "\n"

        for index, line in enumerate(self.board):

            # top of cell
            line_string = " " * cell_width + '#' * cell_width * len(line) + "\n"

            # first empty row of cell
            line_string += " " * cell_width
            line_string += ("#" + "".center(cell_width - 2) + "#") * len(line)

            # row number
            line_string += "\n" + str(index).rjust(cell_width - 1) + " "

            # contents
            for character in line:
                if character is None:
                    line_string += "#" + " ".center(cell_width - 2) + "#"
                else:
                    line_string += "#" + str(character).upper().center(cell_width - 2) + "#"

            # empty row after contents
            line_string += "\n" + " " * cell_width
            line_string += ("#" + "".center(cell_width - 2) + "#") * len(line)

            line_string += "\n"
            result += line_string

        # bottom of cell
        result += " " * cell_width + '#' * cell_width * len(self.board[0]) + "\n"

        return result

    def get_board_contents_at(self, location):

        if location[0] < 0 or location[0] >= len(self.board):
            return False
        elif location[1] < 0 or location[1] >= len(self.board[0]):
            return False

        return self.board[location[0]][location[1]]

    def find_convertable_directions(self, move):

        neighbor_deltas = [
            (1, 1),
            (1, 0),
            (1, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, 1),
            (0, -1)
        ]

        valid_deltas = []

        # if it isn't, check the neighbors for one of your opponent's pieces
        opponent_color = self.get_opponent_color(self.current_player_turn)
        for neighbor_delta in neighbor_deltas:
            neighbor_location = (move[0] + neighbor_delta[0], move[1] + neighbor_delta[1])

            contents = self.get_board_contents_at(neighbor_location)

            # the adjacent piece has to be your opponent's
            if contents is not opponent_color:
                continue

            ray_location = (neighbor_location[0], neighbor_location[1])

            while True:
                ray_location = (ray_location[0] + neighbor_delta[0], ray_location[1] + neighbor_delta[1])
                ray_location_contents = self.get_board_contents_at(ray_location)

                if ray_location_contents is self.current_player_turn:  # your piece, to the position is valid
                    valid_deltas.append(neighbor_delta)
                elif ray_location_contents is opponent_color:  # opponent's piece, so keep going
                    continue
                else:  # either an empty space or the edge of the board, so go on to another neighbor
                    break

        return valid_deltas

    def space_unoccupied(self, move):
        return self.get_board_contents_at(move) is None

    # sample move: (5, 5)
    # will determine if the move is valid for the current player
    def move_is_valid(self, move):

        if self.turns_taken < 4:
            if move == "pass":
                return False

            return self.space_unoccupied(move) and move in self.center_square

        else:

            if move == "pass":
                possible_moves = self.get_possible_moves()
                return len(possible_moves) == 0
            
            return self.space_unoccupied(move) and len(self.find_convertable_directions(move)) > 0

    # get all of the valid moves for the current player
    def get_possible_moves(self):
        possible_moves = []

        # First 4 moves must be within the center square
        if self.turns_taken < 4:
            for square in self.center_square:
                if self.space_unoccupied(square):
                    possible_moves.append(square)

        else:
            for x in xrange(0, len(self.board)):
                for y in xrange(0, len(self.board[0])):
                    if self.move_is_valid((x, y)):
                        possible_moves.append((x, y))

        return possible_moves

    def get_opponent_color(self, color):
        if color == 'w':
            return 'b'
        else:
            return 'w'

    # make the given move for the current player and make it the other player's turn
    def make_move(self, move):

        self.board[move[0]][move[1]] = self.current_player_turn

        for delta in self.find_convertable_directions(move):
            current_location = move

            while True:
                current_location = (current_location[0] + delta[0], current_location[1] + delta[1])

                if self.get_board_contents_at(current_location) is self.current_player_turn:
                    break
                else:
                    self.board[current_location[0]][current_location[1]] = self.current_player_turn

        self.current_player_turn = self.get_opponent_color(self.current_player_turn)
        self.turns_taken += 1

    # count up the number of spaces currently controlled by each player and return them as a tuple
    # white should be the first element, black should be the second one
    def get_score(self):
        result = [(line.count('w'), line.count('b')) for line in self.board]
        result = [sum(x) for x in zip(*result)]
        return result


if __name__ == "__main__":
    parent = Reversi(size=6)
    child = Reversi(parent=parent)
    # child.make_move((0,0))
    parent.board[1][1] = 'w'
    parent.board[1][2] = 'b'
    print parent
