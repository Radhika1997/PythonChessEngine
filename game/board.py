from move import *
from alliance import Alliance
from bishop import Bishop
from king import King
from knight import Knight
from pawn import Pawn
from queen import Queen
from rook import Rook
from tile import *
from player import BlackPlayer,WhitePlayer

class Board:

    __board_config = dict()
    __move_alliance = None
    game_board = list()
    white_pieces = list()
    black_pieces = list()
    white_legal_moves = list()
    black_legal_moves = list()
    white_player = None
    black_player = None
    current_player = None

    def __init__(self):
        self.create_standard_game()
        self.game_board = self.create_game_board()
        self.white_pieces = self.calculate_active_pieces(self.game_board, Alliance.WHITE)
        self.black_pieces = self.calculate_active_pieces(self.game_board, Alliance.BLACK)
        self.white_legal_moves = self.calculate_total_legal_moves(self.white_pieces)
        self.black_legal_moves = self.calculate_total_legal_moves(self.black_pieces)
        self.white_player = WhitePlayer(self, self.white_legal_moves, self.black_legal_moves)
        self.black_player = BlackPlayer(self, self.black_legal_moves, self.white_legal_moves)
        self.current_player = None

    def get_white_player(self):
        return self.white_player

    def get_black_player(self):
        return self.black_player

    def get_current_player(self):
        return self.current_player

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
            legal_moves.append(piece.calculate_legal_moves(self))
        return legal_moves

    def set_piece(self, piece):
        self.__board_config[piece.get_piece_postion()] = piece

    def set_move_alliance(self, move_alliance):
        self.__move_alliance = move_alliance

    def create_game_board(self):
        tiles = list()
        for i in range(64):
            tile_var = Tile(i)
            try:
                tiles.append(tile_var.create_tile(i, self.__board_config[i]))
            except KeyError:
                tiles.append(tile_var.create_tile(i, None))
        return tiles

    def create_standard_game(self):

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
