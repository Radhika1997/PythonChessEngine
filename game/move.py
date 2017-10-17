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

    def get_destination_coordinate(self):
        return self.destination_coordinate

    def execute(self):
        pass


class MajorMove(Move):

    def __init__(self, board, moved_piece, destination_coordinate):
        Move.__init__(self, board, moved_piece, destination_coordinate)

    def execute(self):
        new_board = Board(1)
        for piece in self.board.get_current_player().get_active_pieces():
            if not (piece.get_piece_type() == self.moved_piece.get_piece_type() and piece.get_piece_alliance() == self.moved_piece.get_piece_alliance() and piece.get_piece_position() == self.moved_piece.get_piece_position()):
                new_board.set_piece(piece)

        for piece in self.board.get_current_player().get_opponent().get_active_pieces():
            new_board.set_piece(piece)
        new_board.set_piece(None)
        new_board.set_move_alliance(self.board.get_current_player().get_opponent().get_alliance())
        new_board.set_remaining_attributes()
        return new_board


class AttackMove(Move):

    attacked_piece = None

    def __init__(self, board, moved_piece, destination_coordinate, attacked_piece):
        Move.__init__(self, board, moved_piece, destination_coordinate)
        self.attacked_piece = attacked_piece

    def execute(self):
        pass
