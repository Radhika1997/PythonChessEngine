from unittest import TestCase, main
from game.board import Board


class TestBoard(TestCase):

    def test_initial_board(self):
        board = Board(0)
        self.assertEquals(len(board.get_current_player().get_legal_moves()), 20)
        self.assertEquals(len(board.get_current_player().get_opponent().get_legal_moves()), 20)
        self.assertFalse(board.get_current_player().is_check())
        self.assertFalse(board.get_current_player().is_checkmate())
        self.assertFalse(board.get_current_player().is_castled())

        self.assertEquals(board.get_current_player(), board.white_player)
        self.assertEquals(board.get_current_player().get_opponent(), board.black_player)
        self.assertFalse(board.get_current_player().get_opponent().is_check())
        self.assertFalse(board.get_current_player().get_opponent().is_checkmate())
        self.assertFalse(board.get_current_player().get_opponent().is_castled())


if __name__ == '__main__':
    main()
