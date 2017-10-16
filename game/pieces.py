from alliance import Alliance
from piece_type import Type


class Pieces:

    _piece_position = None
    _piece_type = None
    _piece_alliance = None
    _first_move = None

    def __init__(self, piece_position, piece_alliance, piece_type):
        self._piece_position = piece_position
        self._piece_alliance = piece_alliance
        self._piece_type = piece_type
        self._first_move = True

    def calculate_legal_moves(self, board):
        pass

    def _calculate_coordinates(self):
        x = self._piece_position / 8
        y = self._piece_position % 8
        return x,y

    def get_piece_alliance(self):
        return self._piece_alliance

    def get_first_move(self):
        return self._first_move

    def get_piece_position(self):
        return self._piece_position

    def get_piece_type(self):
        return self._piece_type

    def is_king(self):

        if self._piece_type == Type.KING:
            return True
        else:
            return False
