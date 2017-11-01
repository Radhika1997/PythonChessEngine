from alliance import Alliance
from tile import *
from player import BlackPlayer, WhitePlayer


class Board:
    board_config = dict()
    move_alliance = None
    game_board = list()
    white_pieces = list()
    black_pieces = list()
    white_legal_moves = list()
    black_legal_moves = list()
    white_player = None
    black_player = None
    current_player = None
    enpassant_pawn = None

    def __init__(self, usage_type):
        if usage_type == 0:
            self.create_standard_game()
            self.game_board = self.create_game_board()
            self.white_pieces = self.calculate_active_pieces(self.game_board, Alliance.WHITE)
            self.black_pieces = self.calculate_active_pieces(self.game_board, Alliance.BLACK)
            self.white_legal_moves = self.calculate_total_legal_moves(self.white_pieces)
            self.black_legal_moves = self.calculate_total_legal_moves(self.black_pieces)
            self.white_player = WhitePlayer(self, self.white_legal_moves, self.black_legal_moves)
            self.black_player = BlackPlayer(self, self.black_legal_moves, self.white_legal_moves)
            if self.move_alliance == Alliance.WHITE:
                self.current_player = self.white_player
            elif self.move_alliance == Alliance.BLACK:
                self.current_player = self.black_player
        else:
            self.board_config = dict()

    def get_white_player(self):
        return self.white_player

    def get_black_player(self):
        return self.black_player

    def get_current_player(self):
        return self.current_player

    def get_enpassant_pawn(self):
        return self.enpassant_pawn

    def get_all_legal_moves(self):
        all_moves = self.white_legal_moves
        all_moves.extend(self.black_legal_moves)
        return all_moves

    @staticmethod
    def calculate_active_pieces(game_board, alliance):
        active_pieces = list()
        for i in game_board:

            if i.is_tile_occupied():
                piece = i.get_pieces()

                if piece.get_piece_alliance() == alliance:
                    active_pieces.append(piece)
        return active_pieces

    def calculate_total_legal_moves(self, all_pieces):
        legal_moves = list()
        for piece in all_pieces:
            legal_moves.extend(piece.calculate_legal_moves(self))
        return legal_moves

    def set_remaining_attributes(self):
        self.game_board = self.create_game_board()
        self.white_pieces = self.calculate_active_pieces(self.game_board, Alliance.WHITE)
        self.black_pieces = self.calculate_active_pieces(self.game_board, Alliance.BLACK)
        self.white_legal_moves = self.calculate_total_legal_moves(self.white_pieces)
        self.black_legal_moves = self.calculate_total_legal_moves(self.black_pieces)
        self.white_player = WhitePlayer(self, self.white_legal_moves, self.black_legal_moves)
        self.black_player = BlackPlayer(self, self.black_legal_moves, self.white_legal_moves)
        if self.move_alliance == Alliance.WHITE:
            self.current_player = self.white_player
        elif self.move_alliance == Alliance.BLACK:
            self.current_player = self.black_player

    def set_piece(self, piece):
        self.board_config[piece.get_piece_position()] = piece

    def set_move_alliance(self, move_alliance):
        self.move_alliance = move_alliance

    def set_enpassant_pawn(self, piece):
        self.enpassant_pawn = piece

    def create_game_board(self):
        tiles = list()
        for i in range(64):
            tile_var = Tile(i)
            try:
                tiles.append(tile_var.create_tile(i, self.board_config[i]))
            except KeyError:
                tiles.append(tile_var.create_tile(i, None))
        return tiles

    def create_standard_game(self):
        from bishop import Bishop
        from king import King
        from knight import Knight
        from pawn import Pawn
        from queen import Queen
        from rook import Rook
        self.set_piece(Rook(0, Alliance.WHITE))
        self.set_piece(Knight(1, Alliance.WHITE))
        self.set_piece(Bishop(2, Alliance.WHITE))
        self.set_piece(Queen(3, Alliance.WHITE))
        self.set_piece(King(4, Alliance.WHITE))
        self.set_piece(Bishop(5, Alliance.WHITE))
        self.set_piece(Knight(6, Alliance.WHITE))
        self.set_piece(Rook(7, Alliance.WHITE))
        self.set_piece(Pawn(8, Alliance.WHITE))
        self.set_piece(Pawn(9, Alliance.WHITE))
        self.set_piece(Pawn(10, Alliance.WHITE))
        self.set_piece(Pawn(11, Alliance.WHITE))
        self.set_piece(Pawn(12, Alliance.WHITE))
        self.set_piece(Pawn(13, Alliance.WHITE))
        self.set_piece(Pawn(14, Alliance.WHITE))
        self.set_piece(Pawn(15, Alliance.WHITE))

        self.set_piece(Pawn(48, Alliance.BLACK))
        self.set_piece(Pawn(49, Alliance.BLACK))
        self.set_piece(Pawn(50, Alliance.BLACK))
        self.set_piece(Pawn(51, Alliance.BLACK))
        self.set_piece(Pawn(52, Alliance.BLACK))
        self.set_piece(Pawn(53, Alliance.BLACK))
        self.set_piece(Pawn(54, Alliance.BLACK))
        self.set_piece(Pawn(55, Alliance.BLACK))
        self.set_piece(Rook(56, Alliance.BLACK))
        self.set_piece(Knight(57, Alliance.BLACK))
        self.set_piece(Bishop(58, Alliance.BLACK))
        self.set_piece(Queen(59, Alliance.BLACK))
        self.set_piece(King(60, Alliance.BLACK))
        self.set_piece(Bishop(61, Alliance.BLACK))
        self.set_piece(Knight(62, Alliance.BLACK))
        self.set_piece(Rook(63, Alliance.BLACK))

        self.set_move_alliance(Alliance.WHITE)

    # tile method to be changed changes to be made in knight class
    def get_tile(self, coordinate):
        return self.game_board[coordinate]
