from alliance import Alliance
from piece_type import Type


class Pieces:

    piece_position = None
    _piece_type = None
    _piece_alliance = None
    first_move = None

    def __init__(self, piece_position, piece_alliance, piece_type):
        self.piece_position = piece_position
        self._piece_alliance = piece_alliance
        self._piece_type = piece_type
        self.first_move = True

    def calculate_legal_moves(self, board):
        pass

    def _calculate_coordinates(self):
        x = self.piece_position / 8
        y = self.piece_position % 8
        return x,y

    def get_piece_alliance(self):
        return self._piece_alliance

    def get_first_move(self):
        return self.first_move

    def get_piece_position(self):
        return self.piece_position

    def set_piece_position(self, piece_position):
        self.piece_position = piece_position

    def get_piece_type(self):
        return self._piece_type

    def equals(self, piece):
        if self.get_piece_alliance() == piece.get_piece_alliance() and \
           self.get_piece_type() == piece.get_piece_type() and \
           self.get_piece_position() == piece.get_piece_position():
            return True
        return False

    def is_king(self):

        if self._piece_type == Type.KING:
            return True
        else:
            return False

    def set_first_move(self, first_move):
        self.first_move = first_move

    def set_path(self, alliance, piece_type):
        if Alliance.BLACK == alliance:
            if Type.BISHOP == piece_type:
                return 'BB.gif'
            elif Type.KING == piece_type:
                return 'BK.gif'
            elif Type.KNIGHT == piece_type:
                return 'BN.gif'
            elif Type.PAWN == piece_type:
                return 'BP.gif'
            elif Type.QUEEN == piece_type:
                return 'BQ.gif'
            elif Type.ROOK == piece_type:
                return 'BR.gif'
        else:
            if Type.BISHOP == piece_type:
                return 'WB.gif'
            elif Type.KING == piece_type:
                return 'WK.gif'
            elif Type.KNIGHT == piece_type:
                return 'WN.gif'
            elif Type.PAWN == piece_type:
                return 'WP.gif'
            elif Type.QUEEN == piece_type:
                return 'WQ.gif'
            elif Type.ROOK == piece_type:
                return 'WR.gif'


