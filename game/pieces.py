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
        return x, y

    def get_chess_coordinate(self, message):
        x, y = self._calculate_coordinates()
        chess_coordinate = None
        alliance = None
        if self._piece_alliance == Alliance.WHITE:
            alliance = "W: "
        else:
            alliance = "B: "

        if message == 'O-O' or message == 'O-O-O':
            return alliance + message
        else:
            if y == 0:
                chess_coordinate = 'a'
            elif y == 1:
                chess_coordinate = 'b'
            elif y == 2:
                chess_coordinate = 'c'
            elif y == 3:
                chess_coordinate = 'd'
            elif y == 4:
                chess_coordinate = 'e'
            elif y == 5:
                chess_coordinate = 'f'
            elif y == 6:
                chess_coordinate = 'g'
            elif y == 7:
                chess_coordinate = 'h'
            return alliance + message + chess_coordinate + str(x + 1)

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

    @staticmethod
    def is_last_square(position, alliance):
        if alliance == Alliance.WHITE:
            if position in [63, 62, 61, 60, 59, 58, 57, 56]:
                return True
        elif alliance == Alliance.BLACK:
            if position in [7, 6, 5, 4, 3, 2, 1, 0]:
                return True
        return False

    def is_king(self):

        if self._piece_type == Type.KING:
            return True
        else:
            return False

    def set_first_move(self, first_move):
        self.first_move = first_move

    @staticmethod
    def set_path(alliance, piece_type):
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
