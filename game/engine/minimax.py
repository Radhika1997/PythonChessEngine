from move_strategy import MoveStrategy
from board_evaluator import BoardEvaluator
from game.move_status import Status
from alliance import Alliance
import time

LARGE_NUMBER = 10000000000
SMALL_NUMBER = -10000000000


class MiniMax(MoveStrategy):
    board_evaluate = None

    def __init__(self):
        MoveStrategy.__init__(self)
        self.board_evaluate = BoardEvaluator()

    def execute(self, board, depth):
        start_time = time.time()
        best_move = None
        highest_value = SMALL_NUMBER
        lowest_value = LARGE_NUMBER
        current_value = None
        number_of_moves = len(board.get_current_player().get_legal_moves())

        for move in board.get_current_player().get_legal_moves():
            move_transition = board.get_current_player().make_move(move)
            if move_transition.get_move_status() == Status.DONE:
                if board.get_current_player().get_alliance() == Alliance.WHITE:
                    current_value = self.min(move_transition.get_transition_board(), depth - 1)
                else:
                    current_value = self.min(move_transition.get_transition_board(), depth - 1)

                if board.get_current_player().get_alliance() == Alliance.WHITE and \
                   current_value >= highest_value:
                    highest_value = current_value
                    best_move = move
                elif board.get_current_player().get_alliance() == Alliance.BLACK and \
                     current_value <= lowest_value:
                    highest_value = current_value
                    best_move = move

        execution_time = time.time() - start_time
        return best_move

    def min(self, board, depth):

        if depth == 0:
            return self.board_evaluate.evaluate()

        lowest_value = LARGE_NUMBER
        for move in board.get_current_player().get_legal_moves():
            move_transition = board.get_current_player().make_move(move)
            if move_transition.get_move_status() == Status.DONE:
                current_value = self.max(move_transition.get_transition_board(), depth - 1)
                if current_value <= lowest_value:
                    lowest_value = current_value

        return lowest_value

    def max(self, board, depth):

        if depth == 0:
            return self.board_evaluate.evaluate()

        highest_value = SMALL_NUMBER
        for move in board.get_current_player().get_legal_moves():
            move_transition = board.get_current_player().make_move(move)
            if move_transition.get_move_status() == Status.DONE:
                current_value = self.min(move_transition.get_transition_board(), depth - 1)
                if current_value >= highest_value:
                    highest_value = current_value

        return highest_value
