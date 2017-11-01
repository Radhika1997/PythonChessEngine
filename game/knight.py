from pieces import *
from move import *
from piece_type import Type


class Knight(Pieces):
    def __init__(self, piece_position, piece_alliance):
        Pieces.__init__(self, piece_position, piece_alliance, Type.KNIGHT)

    @staticmethod
    def __knight_valid_moves(x, y):
        valid_moves = list()
        valid_moves.append((x - 1, y - 2))
        valid_moves.append((x + 1, y - 2))
        valid_moves.append((x + 2, y - 1))
        valid_moves.append((x + 2, y + 1))
        valid_moves.append((x + 1, y + 2))
        valid_moves.append((x - 1, y + 2))
        valid_moves.append((x - 2, y + 1))
        valid_moves.append((x - 2, y - 1))
        return valid_moves

    def calculate_legal_moves(self, board):
        x, y = self._calculate_coordinates()
        legal_moves = list()
        valid_moves = self.__knight_valid_moves(x, y)
        for i, j in valid_moves:
            possibility = i * 8 + j
            if 64 > possibility >= 0 and (8 > i >= 0 and 8 > j >= 0):
                destination_tile = board.get_tile(possibility)
                if destination_tile.is_tile_occupied():  # change required
                    piece_on_destination = destination_tile.get_pieces()
                    alliance = piece_on_destination.get_piece_alliance()

                    if self._piece_alliance != alliance:
                        legal_moves.append(AttackMove(board, self, possibility, piece_on_destination))
                else:
                    legal_moves.append(MajorMove(board, self, possibility))
        return legal_moves
