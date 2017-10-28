class BoardEvaluator:

    def __init__(self):
        pass

    def evaluate(self, board, depth):
        pass


class StandardBoardEvaluator(BoardEvaluator):

    CHECK_BONUS = 50
    CHECKMATE_BONUS = 10000
    DEPTH_BONUS = 100
    CASTLE_BONUS = 50

    def __init__(self):
        BoardEvaluator.__init__(self)

    def evaluate(self, board, depth):
        return self.score(board, board.get_white_player(), depth) - \
               self.score(board, board.get_black_player(), depth)

    def score(self, board, player, depth):
        return self.value(player) + \
               self.mobility(player) + \
               self.check(player) + \
               self.checkmate(player, depth) + \
               self.castle(player)

    def depth_bonus(self, depth):
        if depth == 0:
            return 1
        else:
            return self.DEPTH_BONUS * depth

    @staticmethod
    def value(player):
        piece_value = 0
        for piece in player.get_active_pieces():
            piece_value += piece.get_piece_type()
        return piece_value

    @staticmethod
    def mobility(player):
        return len(player.get_legal_moves())

    def check(self, player):
        if player.get_opponent().is_check():
            return self.CHECK_BONUS
        else:
            return 0

    def checkmate(self, player, depth):
        if player.get_opponent().is_checkmate():
            return self.CHECKMATE_BONUS * self.depth_bonus(depth)
        else:
            return 0

    def castle(self, player):
        if player.is_castled():
            return self.CASTLE_BONUS
        else:
            return 0
