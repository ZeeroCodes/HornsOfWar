from MapEditor.Units.UnitArray import UnitArray

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

    def set_tiles_dictionary(self, tiles_dictionary):
        self.tiles_dictionary = tiles_dictionary

    def get_tiles_dictionary(self):
        return self.tiles_dictionary

    def set_nodebase(self, key, nodebase, modify_existent_tile = True):

        if modify_existent_tile:
            if key in self.tiles_dictionary.keys():
                self.tiles_dictionary[key] = nodebase
        else:
            self.tiles_dictionary[key] = nodebase

    def set_terrain(self, key, terrain):

        self.tiles_dictionary[key].set_terrain(terrain)






