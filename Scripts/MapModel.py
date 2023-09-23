import pygame
import math
import os

from pygame.locals import *
from NodeBase import NodeBase
from UnitArray import UnitArray
from HumanWarrior import HumanWarrior
from MapData import MapData

available_movements_even_col = ((-1, 0), (-1, 1), (0, 1), (1, 0), (0, -1), (-1, -1))
available_movements_odd_col = ((-1, 0), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))

RADIUS = 50

class MapModel(object):

    def __init__(self):
        pygame.init()
        self.map_data = MapData()
        self.friendly_units = UnitArray()
        self.enemy_units = UnitArray()
        self.selected_unit = None
        self.selected_unit_movements = set()
        self.path = []
    
    
    # SET_PATH
    # Sets a new path for the selected unit path
    def set_path(self, path = []):
        self.path = path
    
    

    # GET_PATH
    # Returns the actual path between tiles
    def get_path(self):
        return self.path



    # SET_SELECTED_UNIT
    # Sets the new selected unit
    def set_selected_unit(self, unit):
        self.selected_unit = unit



    # SET_SELECTED_UNIT
    # Sets the new selected unit
    def set_selected_unit_position(self, position):
        self.selected_unit.set_position(position)



    # GET_SELECTED_UNIT
    # Returns the selected unit
    def get_selected_unit(self):
        return self.selected_unit



    # GET_SELECTED_UNIT_MOVEMENTS
    # Return the available movements for the selected unit
    def get_selected_unit_movements(self):
        return self.selected_unit_movements



    # SET_SELECTED_UNIT_MOVEMENTS
    # Sets the available movements for the selected unit to the argument
    def set_selected_unit_movements(self, movements):
        self.selected_unit_movements = movements



    # CLEAR_SELECTED_UNIT_MOVEMENTS
    # Restarts selected unit movements to an empty set
    def clear_selected_unit_movements(self):
        self.selected_unit_movements.clear()



    # REACHABLE
    # Returns true if the desired position if inside unit movement
    def reachable(self, position):
        for selected_unit_movement in self.selected_unit_movements:
            if position == selected_unit_movement.get_position():
                return True
        return False



    # MODIFY_UNIT_POSITION
    # Modifies the position of the argument unit
    def modify_unit_position(self, target_unit, position):
        if target_unit in self.friendly_units.get_unit_array():
            self.friendly_units.modify_unit_position(target_unit, position)
        if target_unit in self.enemy_units.get_unit_array():
            self.enemy_units.modify_unit_position(target_unit, position)



    # SET_MAP_DATA
    # Sets the map_data as the argument
    def set_map_data(self, map_data):
        self.map_data = map_data



    # GET_MAP_DATA
    # Return the map_data
    def get_map_data(self):
        return self.map_data



    # GET_TILE_DICTIONARY
    # Return the tile dictionary
    def get_tile_dictionary(self):
        return self.map_data.get_tiles()



    # GET_FRIENDLY_UNITS
    # Returns friendly_units_array
    def get_friendly_units(self):
        return self.friendly_units



    # GET_ENEMY_UNITS
    # Returns enemy units array
    def get_enemy_units(self):
        return self.enemy_units



    # IS_FRIENDLY
    # Returns true if the unit is in the friendly units array
    def is_friendly(self, unit):
        if unit in self.friendly_units.get_unit_array():
            return True
        return False



    # LOAD_MAP
    # Loads map from a text file
    def load_map(self, map_name):
        rows = 0
        cols = 0
        dictionary = dict()
        with open(os.path.abspath(os.getcwd()) + "\\Maps\\" + map_name + ".txt", 'r') as f:
            lines = f.readlines()
            rows = int(lines[0])
            cols = int(lines[1])
            for line in lines[2:]:
                number = []
                char_number = ""
                for char in line:
                    if char == " ":
                        number.append(int(char_number))
                        char_number = ""
                    else:
                        char_number += char
                number.append(int(char_number))
                dictionary[(number[0], number[1])] = NodeBase((number[0], number[1]), (number[2], number[3]))
        
        self.map_data = MapData(rows, cols, dictionary)
        return self.map_data



    # ADD_UNIT
    # Adds a unit to the friendly or enemy array
    def add_unit(self, unit = HumanWarrior((0,0))):
        if unit.get_friendly():
            self.friendly_units.add_unit(unit)
        else:
            self.enemy_units.add(unit)



    # CLOSEST_HEXAGON
    # This function finds and return the nearest center of an hexagon to the actual position of the mouse
    def closest_hexagon(self, point):

        if point == None:
            return None

        dictionary = dict()
        keys = self.map_data.get_tiles().keys()

        for element in keys:
            dictionary[element] = self.map_data.get_tiles()[element].get_pixel_position()

        _, hex_pos = min(dictionary.items(), key=lambda x: math.sqrt(math.pow(x[1][0]-point[0],2) + math.pow(x[1][1]-point[1],2)))    
        
        if math.sqrt(math.pow(hex_pos[0]-point[0],2) + math.pow(hex_pos[1]-point[1],2)) <= RADIUS:

            return hex_pos

        else:

            return None



    # GET_POSITION_BY_COORDS
    # Return a hexagon position from its pixel coordinates
    def get_position_by_coords(self, position_coords): 
        tile_dictionary = self.map_data.get_tiles()
        position = self.closest_hexagon(position_coords)
        if position != None:
            hexagon_position = [k for k, v in tile_dictionary.items() if v.get_pixel_position() == position]
            return tile_dictionary[hexagon_position[0]].get_position()
        return position



    # GET_COORDS_BY_POSITION
    # Return a pixel position by an hexagon position
    def get_coords_by_position(self, position):
        if self.is_inside(position):
            return self.map_data.get_tiles()[position].get_pixel_position()



    # GET_UNIT_IN_POSITION
    # Return unit in the clicked hexagon
    def get_unit_in_position(self, position):
        for unit in self.friendly_units.get_unit_array():
            if unit.get_position() == position:
                return unit
        for unit in self.enemy_units.get_unit_array():
            if unit.get_position() == position:
                return unit
        return None



    # OCCUPIED
    # Returns true if the position is occupied by any unit
    def occupied(self, position):
        for unit in self.friendly_units.get_unit_array():
            if position == unit.get_position():
                return True
        for unit in self.enemy_units.get_unit_array():
            if position == unit.get_position():
                return True
        return False



    # SUM_POSITIONS
    # Returns the sum of 2 positions
    def sum_positions(self, position1, position2):
        return (position1[0]+position2[0], position1[1] + position2[1])



    # IS_EVEN_COLUMN
    # Returns true if the column of the positions is even
    def is_even_column(self, position):
        if position[1]%2 == 0:
            return True
        return False



    # IS_INSIDE
    # Returns true if the argument position is inside the limits of the map
    def is_inside(self, position):
        if position[0] >= 0 and position[0] < math.ceil(self.map_data.get_rows()/2) and position[1] >= 0 and position[1] < self.map_data.get_cols():
            return True
        return False



    # GET_MOVEMENT_POSITIONS
    # Gets the available movement hexagons of the selected unit 
    def get_movement_positions(self):

        initial_position = self.selected_unit.get_position()
        movements = self.selected_unit.get_movement()

        available_positions = set()
        available_positions.add(initial_position)

        final_available_positions = []

        while movements > 0:

            for position in available_positions.copy():

                if self.is_even_column(position):
                    available_movements = available_movements_even_col
                else:
                    available_movements = available_movements_odd_col

                for next_position in available_movements:
                    next_pos = self.sum_positions(position, next_position)

                    if self.is_inside(next_pos) and not self.occupied(next_pos):
                        available_positions.add(next_pos)
                        

            movements -= 1

        available_positions.remove(initial_position)

        for position in available_positions:
            final_available_positions.append(NodeBase(position, self.get_coords_by_position(position)))

        self.selected_unit_movements = final_available_positions
        return final_available_positions



    # GET_FEASIBLE_NEIGHBOURS
    # Returns all neighbours of the argument position which are inside the map and not occupied by a unit
    def get_feasible_neighbours(self, actual_nodebase):

        available_neighbours = set()

        if self.is_even_column(actual_nodebase.get_position()):
            available_movements = available_movements_even_col
        else:
            available_movements = available_movements_odd_col

        for next_position in available_movements:
            next_pos = self.sum_positions(actual_nodebase.get_position(), next_position)

            if self.is_inside(next_pos) and not self.occupied(next_pos):
                neighbour_nodebase = NodeBase(next_pos, self.get_coords_by_position(next_pos))
                neighbour_nodebase.set_parent(actual_nodebase)
                available_neighbours.add(neighbour_nodebase)

        return available_neighbours
    


    # MOVEMENTS_BETWEEN_POSITIONS
    # Return the movements between two hexagons
    def movements_between_positions(self, nodebase1, nodebase2):
        position1 = nodebase1.get_position()
        position2 = nodebase2.get_position()
        return max(abs(position1[0]-position2[0]), abs(position1[1]-position2[1]), abs((position2[0] - position2[1])*-1 - (position1[0] - position1[1])*-1))
    


    # NEAREST_NEIGHBOUR
    # Returns the nodebase that has the lowest F
    def nearest_neighbour(self, nodebase_dict):
        if nodebase_dict:         
            minimum = list(nodebase_dict.values())[0]
            for nodebase in nodebase_dict.values():
                if nodebase.getF() < minimum.getF():
                    minimum = nodebase
            return minimum
        return None



    # NODEBASE_EXISTS
    # Returns true if there is a nodebase with the same position in the array
    def nodebase_exists(self, nodebase, nodebase_array):
        for node in nodebase_array.values():
            if nodebase.get_position() == node.get_position():
                return True
        return False



    # GET_PATH
    # Returns a list of nodebases from the initial tile to the final tile using A* algorithm
    def get_new_path(self, initial_nodebase, final_nodebase):

        if initial_nodebase.get_position() == final_nodebase.get_position():
            return [initial_nodebase]

        open_list = dict()
        closed_list = dict()
        open_list[initial_nodebase.get_position()] = initial_nodebase
        actual_nodebase = initial_nodebase
        
        while(actual_nodebase.get_position() != final_nodebase.get_position()):

            # Get nearest hexagon by its F
            actual_nodebase = open_list.pop(self.nearest_neighbour(open_list).get_position())

            # Add the actual position to the closed list
            if actual_nodebase.get_position() not in closed_list.keys():

                closed_list[actual_nodebase.get_position()] = actual_nodebase
                # Get all its feasible neighbours
                neighbours = list(self.get_feasible_neighbours(actual_nodebase))

                for neighbour in neighbours:

                    # Sets G, H, F values to the neighbours
                    neighbour.setG(self.movements_between_positions(actual_nodebase, initial_nodebase))
                    neighbour.setH(self.movements_between_positions(actual_nodebase, final_nodebase))
                    neighbour.setF()
                    
                    # Check if this neighbour is the final position
                    if neighbour.get_position() == final_nodebase.get_position():

                        actual_nodebase = neighbour
                        closed_list[actual_nodebase.get_position()] = actual_nodebase

                    else:

                        # Check if any neighbour can reach the initial position faster than the actual path
                        if self.nodebase_exists(neighbour, open_list):

                            actual_length = neighbour.getG() + actual_nodebase.getG()

                            if actual_length < open_list[neighbour.get_position()].getG():

                                open_list[neighbour.get_position()].setG(actual_length)
                                open_list[neighbour.get_position()].setF()
                                open_list[neighbour.get_position()].set_parent(actual_nodebase)

                        else:

                            open_list[neighbour.get_position()] = neighbour
        
        actual_nodebase = closed_list[final_nodebase.get_position()]
        final_path = [actual_nodebase]

        while actual_nodebase.get_position() != initial_nodebase.get_position():
            actual_nodebase = closed_list[actual_nodebase.get_position()].get_parent()
            final_path.append(actual_nodebase)

        self.path = final_path
        return final_path





    

        



