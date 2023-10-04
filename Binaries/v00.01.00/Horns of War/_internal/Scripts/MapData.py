class MapData(object):

    def __init__(self, rows = 0, cols = 0, tiles_dictionary = None):
        self.rows = rows
        self.cols = cols
        self.tiles_dictionary = tiles_dictionary

    def set_rows(self, rows):
        self.rows = rows

    def get_rows(self):
        return self.rows

    def set_cols(self, cols):
        self.cols = cols

    def get_cols(self):
        return self.cols

    def set_tiles(self, tiles_dictionary):
        self.tiles_dictionary = tiles_dictionary

    def get_tiles(self):
        return self.tiles_dictionary






