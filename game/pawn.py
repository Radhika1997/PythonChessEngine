from pieces import *
from move import *
from piece_type import Type


class Pawn(Pieces):

    def __init__(self, piece_position, piece_alliance):
        Pieces.__init__(self, piece_position, piece_alliance, Type.PAWN)

    @staticmethod
    def __pawn_valid_moves(x, y):
        valid_moves = list()
        valid_moves.append((x - 1, y - 2))
        valid_moves.append((x + 1, y - 2))
        valid_moves.append((x + 2, y - 1))
        valid_moves.append((x + 2, y + 1))
        valid_moves.append((x + 1, y + 2))
        valid_moves.append((x - 1, y + 2))
        valid_moves.append((x - 2, y + 1))
        valid_moves.append((x - 2, y - 1))
        return valid_moves

    def calculate_legal_moves(self, board):
        x, y = self._calculate_coordinates()
        legal_moves = list()
        valid_moves = list()
        if self._piece_alliance == Alliance.BLACK:
            valid_moves.append((x-1, y, False))
            if self.get_first_move():
                valid_moves.append((x - 2, y, True))
        else:
            valid_moves.append((x + 1, y, False))
            if self.get_first_move():
                valid_moves.append((x + 2, y, True))

        for i, j, value in valid_moves:
            possibility = i * 8 + j
            if 64 > possibility >= 0 and (8 > i >= 0 and 8 > j >= 0):

                destination_tile = board.get_tile(possibility)
                if destination_tile.is_tile_occupied():
                    break
                else:
                    if value:
                        legal_moves.append(PawnJump(board, self, possibility))
                    else:
                        if self.is_last_square(possibility, self._piece_alliance):
                            # TODO change implementation for under promotion
                            pawn_move = PawnMove(board, self, possibility)
                            pawn_move.set_promoted_piece(Type.QUEEN, possibility, self.get_piece_alliance())
                            legal_moves.append(PawnPromotion(pawn_move))
                        else:
                            legal_moves.append(PawnMove(board, self, possibility))
        attack_moves = list()
        if self._piece_alliance == Alliance.BLACK:
            attack_moves.append((x-1, y-1))
            attack_moves.append((x - 1, y + 1))
        else:
            attack_moves.append((x + 1, y - 1))
            attack_moves.append((x + 1, y + 1))

        for i, j in attack_moves:
            possibility = i * 8 + j
            if 64 > possibility >= 0 and (8 > i >= 0 and 8 > j >= 0):

                destination_tile = board.get_tile(possibility)
                if destination_tile.is_tile_occupied():
                    piece_on_destination = destination_tile.get_pieces()
                    alliance = piece_on_destination.get_piece_alliance()

                    if self._piece_alliance != alliance:
                        if self.is_last_square(possibility, self._piece_alliance):
                            pawn_move = PawnAttackMove(board, self, possibility, piece_on_destination)
                            pawn_move.set_promoted_piece(Type.QUEEN, possibility, self.get_piece_alliance())
                            legal_moves.append(PawnPromotion(pawn_move))
                        else:
                            legal_moves.append(PawnAttackMove(board, self, possibility, piece_on_destination))
                else:
                    if board.get_enpassant_pawn() is not None:
                        position = board.get_enpassant_pawn().get_piece_position()
                        alliance = board.get_enpassant_pawn().get_piece_alliance()
                        if position + 8 == possibility or position - 8 == possibility:
                            if self._piece_alliance != alliance:
                                legal_moves.append(PawnEnPassantAttackMove(board,
                                                                           self,
                                                                           possibility,
                                                                           board.get_enpassant_pawn()))
        return legal_moves
