from pieces import Pieces
from board import Board


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

    def get_current_coordinate(self):
        return self.moved_piece.get_piece_position()

    def is_attack(self):
        return False

    def is_castling(self):
        return False

    def get_attacked_piece(self):
        return None

    def execute(self):
        new_board = Board(1)
        for piece in self.board.get_current_player().get_active_pieces():
            if not piece.equals(self.moved_piece):
                new_board.set_piece(piece)

        for piece in self.board.get_current_player().get_opponent().get_active_pieces():
            new_board.set_piece(piece)

        self.moved_piece.set_piece_position(self.destination_coordinate)
        new_board.set_piece(self.moved_piece)
        new_board.set_move_alliance(self.board.get_current_player().get_opponent().get_alliance())
        new_board.set_remaining_attributes()
        return new_board


class MajorMove(Move):

    def __init__(self, board, moved_piece, destination_coordinate):
        Move.__init__(self, board, moved_piece, destination_coordinate)


class AttackMove(Move):

    attacked_piece = None

    def __init__(self, board, moved_piece, destination_coordinate, attacked_piece):
        Move.__init__(self, board, moved_piece, destination_coordinate)
        self.attacked_piece = attacked_piece

    def execute(self):
        pass

    def is_attack(self):
        return True

    def get_attacked_piece(self):
        return self.attacked_piece

    def equals(self, move):
        if Move.equals(self, move) and self.attacked_piece.equals(move.get_attacked_piece()):
            return True
        return False


class PawnMove(Move):

    def __init__(self, board, moved_piece, destination_coordinate):
        Move.__init__(self, board, moved_piece, destination_coordinate)


class PawnAttackMove(AttackMove):

    def __init__(self, board, moved_piece, destination_coordinate, attacked_piece):
        AttackMove.__init__(self, board, moved_piece, destination_coordinate, attacked_piece)


class PawnEnPassantAttackMove(PawnAttackMove):

    def __init__(self, board, moved_piece, destination_coordinate, attacked_piece):
        AttackMove.__init__(self, board, moved_piece, destination_coordinate, attacked_piece)


class PawnJump(Move):

    def __init__(self, board, moved_piece, destination_coordinate):
        Move.__init__(self, board, moved_piece, destination_coordinate)

    def execute(self):

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


class CastleMove(Move):

    def __init__(self, board, moved_piece, destination_coordinate):
        Move.__init__(self, board, moved_piece, destination_coordinate)


class KingSideCastleMove(CastleMove):

    def __init__(self, board, moved_piece, destination_coordinate):
        CastleMove.__init__(self, board, moved_piece, destination_coordinate)


class QueenSideCastleMove(CastleMove):
    def __init__(self, board, moved_piece, destination_coordinate):
        CastleMove.__init__(self, board, moved_piece, destination_coordinate)


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
            if move.get_current_coordinate() == current_coordinate and move.get_destination_coordinate() == destination_coordinate:
                return move

        return NO_MOVE
