from alliance import Alliance
from move_status import Status
from move_transition import MoveTransition
from piece_type import Type


class Player:
    _board = None
    _player_king = None
    _legal_moves = None
    _check = None

    def __init__(self, board, legal_moves, opponent_moves):
        self._board = board
        self._player_king = self.get_king()
        self._legal_moves = legal_moves
        if self.calculate_attack_on_tile(self._player_king.get_piece_position(), opponent_moves):
            self._check = True
        else:
            self._check = False

    def get_king(self):
        for piece in self.get_active_pieces():
            if piece.is_king():
                return piece
        else:
            raise RuntimeError("King doesn't exist")

    def get_player_king(self):
        return self._player_king

    def get_legal_moves(self):
        return self._legal_moves

    def get_active_pieces(self):
        pass

    def get_alliance(self):
        pass

    def get_opponent(self):
        pass

    @staticmethod
    def calculate_attack_on_tile(piece_position, moves):
        attack_moves = list()
        for move in moves:
            if piece_position == move.get_destination_coordinate():
                attack_moves.append(move)
        return attack_moves

    # TODO work below methods
    def no_escape_moves(self):
        for move in self._legal_moves:
            transition = self.make_move(move)
            if transition.get_move_status() == Status.DONE:
                return False
        return True

    def is_move_legal(self, move_legal):
        for moves in self._legal_moves:
            if move_legal.destination_coordinate == moves.destination_coordinate and \
               move_legal.get_piece_position() == moves.get_piece_position() and \
               move_legal.get_piece_type() == moves.get_piece_type() and \
               move_legal.get_piece_alliance() == moves.get_piece_alliance():
                return True
        return False

    def is_check(self):
        return self._check

    def is_checkmate(self):
        return self._check and self.no_escape_moves()

    def is_stalemate(self):
        return not self._check and self.no_escape_moves()

    def is_castled(self):
        pass

    def make_move(self, move_execute):

        if not self.is_move_legal(move_execute):
            return MoveTransition(self._board, move_execute, Status.ILLEGAL_MOVE)

        transition_board = move_execute.execute()
        king_attacks = Player.calculate_attack_on_tile(transition_board.get_current_player()
                                                       .get_player_king().get_piece_position(),
                                                       transition_board.get_current_player().
                                                       get_legal_moves())

        if king_attacks:
            return MoveTransition(self._board, move_execute, Status.LEAVES_PLAYER_IN_CHECK)

        return MoveTransition(transition_board, move_execute, Status.DONE)

    def calculate_king_castles(self, player_legal, opponent_legal):
        pass


class WhitePlayer(Player):

    def __init__(self, board, legal_moves, opponent_moves):
        Player.__init__(self, board, legal_moves, opponent_moves)

    def get_active_pieces(self):
        return self._board.white_pieces

    def get_alliance(self):
        return Alliance.WHITE

    def get_opponent(self):
        return self._board.get_black_player()

    def calculate_king_castles(self, player_legal, opponent_legal):
        king_castles = list()

        if self._player_king.get_first_move() and not self.is_check():
            if not self._board.get_tile(5).is_tile_occupied() and \
               not self._board.get_tile(6).is_tile_occupied():
                rook_tile = self._board.get_tile(7)
                if rook_tile.is_tile_occupied() and rook_tile.get_pieces().get_first_move():
                    if not Player.calculate_attack_on_tile(5, opponent_legal) and \
                       not Player.calculate_attack_on_tile(6, opponent_legal) and \
                       rook_tile.get_pieces().get_piece_type() == Type.ROOK:
                        king_castles.append(None)

            if not self._board.get_tile(1).is_tile_occupied() and \
               not self._board.get_tile(2).is_tile_occupied() and \
               not self._board.get_tile(3).is_tile_occupied():
                rook_tile = self._board.get_tile(0)
                if rook_tile.is_tile_occupied() and rook_tile.get_pieces().get_first_move():
                    king_castles.append(None)

        return king_castles


class BlackPlayer(Player):

    def __init__(self, board, legal_moves, opponent_moves):
        Player.__init__(self, board, legal_moves, opponent_moves)

    def get_active_pieces(self):
        return self._board.black_pieces

    def get_alliance(self):
        return Alliance.BLACK

    def get_opponent(self):
        return self._board.get_white_player()

    def calculate_king_castles(self, player_legal, opponent_legal):
        pass