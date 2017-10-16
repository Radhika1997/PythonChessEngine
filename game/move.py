from pieces import Pieces


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
        pass


class AttackMove(Move):

    attacked_piece = None

    def __init__(self, board, moved_piece, destination_coordinate, attacked_piece):
        Move.__init__(self, board, moved_piece, destination_coordinate)
        self.attacked_piece = attacked_piece

    def execute(self):
        pass
