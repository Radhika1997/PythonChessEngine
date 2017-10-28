class BoardEvaluator:

    def __init__(self):
        pass

    def evaluate(self, board, depth):
        pass


class StandardBoardEvaluator(BoardEvaluator):

    def __init__(self):
        BoardEvaluator.__init__(self)

    def evaluate(self, board, depth):
        return self.score(board, board.get_white_player(), depth) - \
               self.score(board, board.get_black_player(), depth)

    def score(self, board, player, depth):
        return self.value(player)

    def value(self, player):
        piece_value = 0
        for piece in player.get_active_pieces():
            piece_value += piece.get_piece_type()
        return piece_value
