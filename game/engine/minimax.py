from move_strategy import MoveStrategy
from board_evaluator import BoardEvaluator
from game.move_status import Status

class MiniMax(MoveStrategy):

    board_evaluate = None

    def __init__(self):
        MoveStrategy.__init__(self)
        self.board_evaluate = BoardEvaluator()

    def execute(self, board, depth):
        pass

    def min(self, board, depth):

        if depth == 0:
            return self.board_evaluate.evaluate()

        lowest_value = 10000000000
        for move in board.get_current_player().get_legal_moves():
            move_transition = board.get_current_player().make_move(move)
            if move_transition.get_move_status() == Status.DONE:
                current_value = self.max(move_transition.get_transition_board(), depth-1)
                if current_value <= lowest_value:
                    lowest_value = current_value

        return lowest_value

    def max(self, board, depth):

        if depth == 0:
            return self.board_evaluate.evaluate()

        highest_value = -10000000000
        for move in board.get_current_player().get_legal_moves():
            move_transition = board.get_current_player().make_move(move)
            if move_transition.get_move_status() == Status.DONE:
                current_value = self.min(move_transition.get_transition_board(), depth-1)
                if current_value >= highest_value:
                    highest_value = current_value

        return highest_value
