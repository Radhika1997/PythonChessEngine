class MoveTransition:

    transition_board = None
    move = None
    move_status = None

    def __init__(self, transition_board, move, move_status):
        self.transition_board = transition_board
        self.move = move
        self.move_status = move_status

    def get_move_status(self):
        return self.move_status

    def get_transition_board(self):
        return self.transition_board
