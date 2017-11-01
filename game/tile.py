class Tile:
    _tile_coordinate = None

    def __init__(self, title_coordinate):
        self._tile_coordinate = title_coordinate

    def is_tile_occupied(self):
        pass

    def get_pieces(self):
        pass

    def get_tile_coordinate(self):
        return self._tile_coordinate

    @staticmethod
    def __create_all_possible_empty_tiles():
        empty_tile_dict = dict()

        for i in range(0, 64):
            empty_tile_dict[i] = EmptyTile(i)

        return empty_tile_dict

    def create_tile(self, tile_coordinate, piece):
        if piece is None:
            return self.__create_all_possible_empty_tiles()[tile_coordinate]
        else:
            return OccupiedTile(tile_coordinate, piece)


class EmptyTile(Tile):
    def __init__(self, coordinate):
        Tile.__init__(self, coordinate)

    def is_tile_occupied(self):
        return False

    def get_pieces(self):
        return None


class OccupiedTile(Tile):
    __piece_on_tile = None

    def __init__(self, coordinate, piece_on_tile):
        Tile.__init__(self, coordinate)
        self.__piece_on_tile = piece_on_tile

    def is_tile_occupied(self):
        return True

    def get_pieces(self):
        return self.__piece_on_tile
