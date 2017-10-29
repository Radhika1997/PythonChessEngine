from unittest import TestCase, main
from game.board import Board
from game.move_status import Status


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

    def test_fools_mate(self):
        board = Board(0)
        from game.move import MoveCreator
        move_transition_1 = board.get_current_player().\
            make_move(MoveCreator().create_move(board, 13, 21))
        self.assertTrue(move_transition_1.get_move_status() == Status.DONE)
        move_transition_2 = move_transition_1.get_transition_board().get_current_player().\
            make_move(MoveCreator().create_move(move_transition_1.get_transition_board(), 52, 36))
        self.assertTrue(move_transition_2.get_move_status() == Status.DONE)
        move_transition_3 = move_transition_2.get_transition_board().get_current_player().\
            make_move(MoveCreator().create_move(move_transition_2.get_transition_board(), 14, 30))
        self.assertTrue(move_transition_3.get_move_status() == Status.DONE)
        from game.engine.minimax import MiniMax
        strategy = MiniMax(4)
        move = strategy.execute(move_transition_3.get_transition_board())
        best_move = MoveCreator().create_move(move_transition_3.get_transition_board(), 59, 31)
        self.assertEqual(move, best_move)


if __name__ == '__main__':
    main()
