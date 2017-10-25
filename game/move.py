from piece_type import Type
from alliance import Alliance


class Move:

    board = None
    moved_piece = None
    destination_coordinate = None

    def __init__(self, board, moved_piece, destination_coordinate):
        self.board = board
        self.moved_piece = moved_piece
        self.destination_coordinate = destination_coordinate

    def equals(self, move):
        if self.destination_coordinate == move.destination_coordinate and \
           self.moved_piece.equals(move.moved_piece):
            return True
        return False

    def get_destination_coordinate(self):
        return self.destination_coordinate

    def get_moved_piece(self):
        return self.moved_piece

    def get_current_coordinate(self):
        return self.moved_piece.get_piece_position()

    def is_attack(self):
        return False

    def is_castling(self):
        return False

    def get_attacked_piece(self):
        return None

    def string(self):
        return ''

    def execute(self):
        from board import Board
        new_board = Board(1)
        for piece in self.board.get_current_player().get_active_pieces():
            if not piece.equals(self.moved_piece):
                new_board.set_piece(piece)
            else:
                pass
                # print 'i am here'
        for piece in self.board.get_current_player().get_opponent().get_active_pieces():
            new_board.set_piece(piece)

        self.moved_piece.set_piece_position(self.destination_coordinate)
        self.moved_piece.set_first_move(False)
        new_board.set_piece(self.moved_piece)
        new_board.set_move_alliance(self.board.get_current_player().get_opponent().get_alliance())
        new_board.set_remaining_attributes()
        # print len(self.board.board_config), self.board.board_config
        # print len(new_board.board_config), new_board.board_config
        return new_board


class MajorMove(Move):

    def __init__(self, board, moved_piece, destination_coordinate):
        Move.__init__(self, board, moved_piece, destination_coordinate)


class AttackMove(Move):

    attacked_piece = None

    def __init__(self, board, moved_piece, destination_coordinate, attacked_piece):
        Move.__init__(self, board, moved_piece, destination_coordinate)
        self.attacked_piece = attacked_piece

    def is_attack(self):
        return True

    def get_attacked_piece(self):
        return self.attacked_piece

    def equals(self, move):
        if Move.equals(self, move) and self.attacked_piece.equals(move.get_attacked_piece()):
            return True
        return False

    def string(self):
        if self.moved_piece.get_piece_type() == Type.PAWN:
            if self.moved_piece.get_piece_alliance() == Alliance.WHITE:
                return 'Px'
            else:
                return 'px'
        elif self.moved_piece.get_piece_type() == Type.BISHOP:
            if self.moved_piece.get_piece_alliance() == Alliance.WHITE:
                return 'Bx'
            else:
                return 'bx'
        elif self.moved_piece.get_piece_type() == Type.ROOK:
            if self.moved_piece.get_piece_alliance() == Alliance.WHITE:
                return 'Rx'
            else:
                return 'rx'
        elif self.moved_piece.get_piece_type() == Type.KNIGHT:
            if self.moved_piece.get_piece_alliance() == Alliance.WHITE:
                return 'Nx'
            else:
                return 'nx'
        elif self.moved_piece.get_piece_type() == Type.QUEEN:
            if self.moved_piece.get_piece_alliance() == Alliance.WHITE:
                return 'Qx'
            else:
                return 'qx'
        elif self.moved_piece.get_piece_type() == Type.KING:
            if self.moved_piece.get_piece_alliance() == Alliance.WHITE:
                return 'Kx'
            else:
                return 'kx'

    def execute(self):

        from board import Board
        new_board = Board(1)
        for piece in self.board.get_current_player().get_active_pieces():
            if not piece.equals(self.moved_piece):
                new_board.set_piece(piece)

        for piece in self.board.get_current_player().get_opponent().get_active_pieces():
            if not piece.equals(self.attacked_piece):
                new_board.set_piece(piece)

        self.moved_piece.set_piece_position(self.destination_coordinate)
        self.moved_piece.set_first_move(False)
        new_board.set_piece(self.moved_piece)
        new_board.set_move_alliance(self.board.get_current_player().get_opponent().get_alliance())
        new_board.set_remaining_attributes()
        return new_board


class PawnMove(Move):

    def __init__(self, board, moved_piece, destination_coordinate):
        Move.__init__(self, board, moved_piece, destination_coordinate)


class PawnAttackMove(AttackMove):

    def __init__(self, board, moved_piece, destination_coordinate, attacked_piece):
        AttackMove.__init__(self, board, moved_piece, destination_coordinate, attacked_piece)


class PawnEnPassantAttackMove(PawnAttackMove):

    def __init__(self, board, moved_piece, destination_coordinate, attacked_piece):
        PawnAttackMove.__init__(self, board, moved_piece, destination_coordinate, attacked_piece)


class PawnJump(Move):

    def __init__(self, board, moved_piece, destination_coordinate):
        Move.__init__(self, board, moved_piece, destination_coordinate)

    def execute(self):
        from board import Board
        new_board = Board(1)
        for piece in self.board.get_current_player().get_active_pieces():
            if not piece.equals(self.moved_piece):
                new_board.set_piece(piece)

        for piece in self.board.get_current_player().get_opponent().get_active_pieces():
            new_board.set_piece(piece)

        self.moved_piece.set_piece_position(self.destination_coordinate)
        new_board.set_piece(self.moved_piece)
        new_board.set_enpassant_pawn(self.moved_piece)
        new_board.set_move_alliance(self.board.get_current_player().get_opponent().get_alliance())
        new_board.set_remaining_attributes()
        return new_board


# TODO errors in castling move
class CastleMove(Move):

    castle_rook = None
    castle_rook_initial = None
    castle_rook_final = None

    def __init__(self, board, moved_piece, destination_coordinate,
                 castle_rook, castle_rook_initial, castle_rook_final):
        Move.__init__(self, board, moved_piece, destination_coordinate)
        self.castle_rook = castle_rook
        self.castle_rook_initial = castle_rook_initial
        self.castle_rook_final = castle_rook_final

    def get_castle_rook(self):
        return self.castle_rook

    def is_castling(self):
        return True

    def execute(self):
        from board import Board
        new_board = Board(1)
        for piece in self.board.get_current_player().get_active_pieces():
            if not piece.equals(self.moved_piece) and not piece.equals(self.castle_rook):
                new_board.set_piece(piece)

        for piece in self.board.get_current_player().get_opponent().get_active_pieces():
            new_board.set_piece(piece)

        self.moved_piece.set_piece_position(self.destination_coordinate)
        self.castle_rook.set_piece_position(self.castle_rook_final)
        new_board.set_piece(self.moved_piece)
        new_board.set_piece(self.castle_rook)
        new_board.set_move_alliance(self.board.get_current_player().get_opponent().get_alliance())
        new_board.set_remaining_attributes()
        return new_board


class KingSideCastleMove(CastleMove):

    def __init__(self, board, moved_piece, destination_coordinate,
                 castle_rook, castle_rook_initial, castle_rook_final):
        CastleMove.__init__(self, board, moved_piece, destination_coordinate,
                            castle_rook, castle_rook_initial, castle_rook_final)


class QueenSideCastleMove(CastleMove):
    def __init__(self, board, moved_piece, destination_coordinate,
                 castle_rook, castle_rook_initial, castle_rook_final):
        CastleMove.__init__(self, board, moved_piece, destination_coordinate,
                            castle_rook, castle_rook_initial, castle_rook_final)


class NoMove(Move):

    def __init__(self):
        Move.__init__(self, None, None, -1)

    def execute(self):
        raise RuntimeError('No move cannot be executed')


NO_MOVE = NoMove()


class MoveCreator:

    def __init__(self):
        pass

    def create_move(self,board, current_coordinate, destination_coordinate):

        for move in board.get_all_legal_moves():
            if move.get_current_coordinate() == current_coordinate and \
               move.get_destination_coordinate() == destination_coordinate:
                return move

        return NO_MOVE
