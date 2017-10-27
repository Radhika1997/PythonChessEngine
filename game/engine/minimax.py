from move_strategy import MoveStrategy
from board_evaluator import BoardEvaluator


class MiniMax(MoveStrategy):

    board_evaluate = None

    def __init__(self):
        MoveStrategy.__init__(self)
        self.board_evaluate = BoardEvaluator()

    def execute(self, board, depth):
        pass
