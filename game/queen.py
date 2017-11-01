from pieces import *
from move import *
from piece_type import Type


class Queen(Pieces):
    def __init__(self, piece_position, piece_alliance):
        Pieces.__init__(self, piece_position, piece_alliance, Type.QUEEN)

    @staticmethod
    def __queen_valid_moves(x, y):
        valid_moves_direction1 = list()
        valid_moves_direction2 = list()
        valid_moves_direction3 = list()
        valid_moves_direction4 = list()
        valid_moves_direction5 = list()
        valid_moves_direction6 = list()
        valid_moves_direction7 = list()
        valid_moves_direction8 = list()
        for i in range(1, 9):
            valid_moves_direction1.append((x + i, y))
            valid_moves_direction2.append((x, y - i))
            valid_moves_direction3.append((x, y + i))
            valid_moves_direction4.append((x - i, y))
            valid_moves_direction5.append((x + i, y + i))
            valid_moves_direction6.append((x + i, y - i))
            valid_moves_direction7.append((x - i, y + i))
            valid_moves_direction8.append((x - i, y - i))

        return valid_moves_direction1, valid_moves_direction2, valid_moves_direction3, valid_moves_direction4, \
            valid_moves_direction5, valid_moves_direction6, valid_moves_direction7, valid_moves_direction8

    def calculate_legal_moves(self, board):
        x, y = self._calculate_coordinates()
        legal_moves = list()
        valid_moves = self.__queen_valid_moves(x, y)

        for k in range(8):
            for i, j in valid_moves[k]:
                possibility = i * 8 + j
                if 64 > possibility >= 0 and (8 > i >= 0 and 8 > j >= 0):
                    destination_tile = board.get_tile(possibility)
                    if destination_tile.is_tile_occupied():  # change required
                        piece_on_destination = destination_tile.get_pieces()
                        alliance = piece_on_destination.get_piece_alliance()

                        if self._piece_alliance != alliance:
                            legal_moves.append(AttackMove(board, self, possibility, piece_on_destination))
                        break
                    else:
                        legal_moves.append(MajorMove(board, self, possibility))
        return legal_moves
