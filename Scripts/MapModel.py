import pygame
import math
import os
import numpy as np

from pygame.locals import *
from Scripts.Widgets.NodeBase import NodeBase
from Scripts.Units.UnitArray import UnitArray
from Scripts.Units.Humans.HumanWarrior.HumanWarrior import HumanWarrior
from Scripts.MapData import MapData

available_movements_even_col = ((-1, 0), (-1, 1), (0, 1), (1, 0), (0, -1), (-1, -1))
available_movements_odd_col = ((-1, 0), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))

RADIUS = 50

class MapModel(object):

    def __init__(self):
        pygame.init()
        self.map_data = MapData()
        self.selected_unit = None
        self.selected_unit_movements = set()
        self.selected_unit_attack_movements = []
        self.path = []
        self.team_units = [2,UnitArray(),UnitArray()]
        self.team_groups = [[1],[2]]
        self.playing_team = 1

        self.money = 100
    


    def print_units(self):
        print("#########################################")
        print("Printing units...")
        cont = 1
        for team in self.team_units[1:]:
            print("For team " + str(cont) + " :")
            cont += 1
            for unit in team.get_unit_array():
                #print(unit)
                unit.toString()


    #################################################################
    ################ GETTERS ########################################
    #################################################################



    def get_money(self):
        return self.money



    # GET_TEAM_GROUPS
    # Returns array with the groups of teams
    def get_team_groups(self):
        return self.team_groups



    # GET_MAP_DATA
    # Return the map_data
    def get_map_data(self):
        return self.map_data



    # GET_FRIENDLY_UNITS
    # Returns friendly_units_array
    def get_friendly_units(self):
        return self.friendly_units



    # GET_SELECTED_UNIT
    # Returns the selected unit
    def get_selected_unit(self):
        return self.selected_unit



    # GET_SELECTED_UNIT_MOVEMENTS
    # Return the available movements for the selected unit
    def get_selected_unit_movements(self):
        return self.selected_unit_movements



    # GET_SELECTED_UNIT_ATTACK_MOVEMENTS
    # Returns the selected unit attack movements
    def get_selected_unit_attack_movements(self):
        return self.selected_unit_attack_movements



    # GET_PATH
    # Returns the actual path between tiles
    def get_path(self):
        return self.path



    # GET_TILE_DICTIONARY
    # Return the tile dictionary
    def get_tile_dictionary(self):
        return self.map_data.get_tiles()


    # GET_TEAM_UNITS
    # Returns the total of units
    def get_team_units(self):
        return self.team_units

    def get_units_from_team(self, team):
        return self.team_units[team]

    # GET_GROUP
    # Returns the group of teams the unit team is in
    def get_group(self, unit):

        team = unit.get_team()

        for group_team in self.team_groups:

            if team in group_team:

                return group_team



    #################################################################
    ################ SETTERS ########################################
    #################################################################


    def spend(self, money):
        self.money -= money

    def earn(self, money):
        self.money += money


    # SET_MAP_DATA
    # Sets the map_data as the argument
    def set_map_data(self, map_data):
        self.map_data = map_data



    # SET_SELECTED_UNIT
    # Sets the new selected unit
    def set_selected_unit(self, unit):
        self.selected_unit = unit



    # SET_SELECTED_UNIT_MOVEMENTS
    # Sets the available movements for the selected unit to the argument
    def set_selected_unit_movements(self, movements = []):
        self.selected_unit_movements = movements



    # SET_SELECTED_UNIT_ATTACK_MOVEMENTS
    # Sets the selected unit attack movements
    def set_selected_unit_attack_movements(self, selected_unit_attack_movements):
        self.selected_unit_attack_movements = selected_unit_attack_movements


    
    # SET_PATH
    # Sets a new path for the selected unit path
    def set_path(self, path = []):
        self.path = path
    


    # SET_SELECTED_UNIT_POSITION
    # Sets the new selected unit
    def set_selected_unit_position(self, nodebase):

        self.selected_unit.set_position(nodebase)
 


    #################################################################
    ################ FUNCTIONS ######################################
    #################################################################



    #################################################################
    ################ UNITS RELATED###### ############################
    #################################################################



    # MODIFY_UNIT_POSITION
    # Modifies the position of the argument unit
    def modify_unit_position(self, target_unit, nodebase):

        final_nodebase = nodebase

        if not isinstance(nodebase, NodeBase):

            final_nodebase = NodeBase(nodebase, self.get_coords_by_position(nodebase))
        
        self.team_units[target_unit.get_team()].modify_unit_position(target_unit, final_nodebase)

    

    # SET_UNIT_MOVED
    # Changes if a unit has moved or not
    def set_unit_moved(self, target_unit, moved):
        
        self.team_units[target_unit.get_team()].set_unit_moved(target_unit, moved)

    

    # RESTART_UNIT_MOVEMENTS
    # Restarts all units movement to False in the desired team
    def restart_unit_movements(self):

        for team in self.team_units[1:]:

            for unit in team.get_unit_array():

                self.set_unit_moved(unit, False)



    # ADD_UNIT
    # Adds a unit to the friendly or enemy array
    def add_unit(self, unit = HumanWarrior((0,0)), team = 1):

        self.team_units[team].add_unit(unit)
        self.print_units()



    # DELETE_UNIT
    # Deletes a unit from the friendly or enemy ones
    def delete_unit(self, unit):

        self.team_units[unit.get_team()].remove_unit(unit)

    

    # ALL_UNITS_IN_TEAM_MOVED
    # Return true if all units in the team have moved and false if there is some left to move
    def all_units_in_team_moved(self, team):

        for unit in self.team_units[team].get_unit_array():

            #print(unit.get_moved())
            if not unit.get_moved():
                #print("Una que no")
                return False

        return True



    #################################################################
    ################ ESSENTIALS #####################################
    #################################################################



    # REACHABLE
    # Returns true if the desired position if inside unit movement
    def reachable(self, position):
        
        if isinstance(position, NodeBase):

            position = position.get_position()

        for selected_unit_movement in self.selected_unit_movements:

            if position == selected_unit_movement.get_position() or position == self.selected_unit.get_position():

                return True

        return False



    # IS_FRIENDLY
    # Returns true if the unit is in the friendly units array
    def is_friendly(self, unit):

        if unit == None:

            return False

        team_group = self.get_group(unit)

        if self.playing_team in team_group:

            return True

        return False



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

        hex_position = position

        if isinstance(position, NodeBase):

            hex_position = position.get_position()

        if self.is_inside(hex_position):

            return self.map_data.get_tiles()[hex_position].get_pixel_position()


    
    # GET_UNIT_IN_POSITION
    # Return unit in the clicked hexagon
    def get_unit_in_position(self, position):

        if isinstance(position, NodeBase):

            position = position.get_position()

        for team in self.team_units[1:]:

            for unit in team.get_unit_array():

                if unit.get_position() == position:

                    return unit 

        return None



    # OCCUPIED
    # Returns true if the position is occupied by any unit
    def occupied(self, position):

        if isinstance(position, NodeBase):

            position = position.get_position()
        #print(f"Checking {position}")

        for team in self.team_units[1:]:

            for unit in team.get_unit_array():
                #unit.toString()
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

        if isinstance(position, NodeBase):

            position = position.get_position()

        if self.is_even(position[1]):#position[1]%2 == 0:

            return True

        return False



    # IS_INSIDE
    # Returns true if the argument position is inside the limits of the map
    def is_inside(self, position):

        pos = position

        if isinstance(position, NodeBase):

            pos = position.get_position()

        if pos[0] >= 0 and pos[0] < math.ceil(self.map_data.get_rows()/2) and pos[1] >= 0 and pos[1] < self.map_data.get_cols():
            
            return True

        return False


    
    # IS_EVEN
    # Auxiliar function that returns true if a number is even
    def is_even(self, number):

        if number%2 == 0:

            return True

        return False



    # IS_ODD
    # Auxiliar function that returns true if a number is odd
    def is_odd(self, number):

        if number%2 == 1:

            return True

        return False
   


    # POSITION_IN_NODEBASES
    # Returns true if there is a Nodebase that has the desired position
    def position_in_nodebases(self, position, nodebase_array):

        for node in nodebase_array:

            if position == node.get_position():

                return True

        return False



    # NODEBASE_EXISTS
    # Returns true if there is a nodebase with the same position in the array
    def nodebase_exists(self, nodebase, nodebase_array):

        array = nodebase_array

        if isinstance(nodebase_array, dict):

            array = nodebase_array.values()

        #for node in array:

        #    if nodebase.get_position() == node.get_position():

        #        return True

        #return False

        return self.position_in_nodebases(nodebase.get_position(), array)



    #################################################################
    ################ MAP RELATED ####################################
    #################################################################
    

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



    # GET_UNIT_MOVEMENT_POSITIONS
    # Gets the available movement hexagons of the selected unit 
    def get_movement_positions(self, unit = None):

        if unit == None:

            return []

        initial_position = unit.get_position()
        movements = unit.get_movement()

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

        
        if unit == self.selected_unit:

            self.selected_unit_movements = final_available_positions

        return final_available_positions



    # GET_MOVEMENT_POSITIONS_FROM_POSITION
    # Gets the available movement hexagons from a initial position and movements
    def get_movement_positions_from_position(self, initial_position, movements):

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

                    if self.is_inside(next_pos):
                        available_positions.add(next_pos)


            movements -= 1

        available_positions.remove(initial_position)

        for position in available_positions:
            final_available_positions.append(NodeBase(position, self.get_coords_by_position(position)))

        return final_available_positions



    # GET_FEASIBLE_NEIGHBOURS
    # Returns all neighbours of the argument position which are inside the map and not occupied by a unit
    def get_feasible_neighbours(self, actual_nodebase, final_nodebase):

        available_neighbours = set()

        if self.is_even_column(actual_nodebase.get_position()):

            available_movements = available_movements_even_col

        else:

            available_movements = available_movements_odd_col

        for next_position in available_movements:

            next_pos = self.sum_positions(actual_nodebase.get_position(), next_position)

            if self.is_inside(next_pos):

                unit = self.get_unit_in_position(next_pos)

                if not self.occupied(next_pos) or next_pos == final_nodebase.get_position():

                    neighbour_nodebase = NodeBase(next_pos, self.get_coords_by_position(next_pos))
                    neighbour_nodebase.set_parent(actual_nodebase)
                    available_neighbours.add(neighbour_nodebase)

        return available_neighbours



    # MOVEMENTS_BETWEEN_POSITIONS
    # Return the movements between two hexagons
    def movements_between_positions(self, nodebase1, nodebase2):

        if nodebase1 != None and nodebase2 != None:

            position1 = nodebase1

            if isinstance(nodebase1, NodeBase):

                position1 = nodebase1.get_position()
          
            position2 = nodebase2

            if isinstance(nodebase2, NodeBase):

                position2 = nodebase2.get_position()

            dx = abs(position1[0] - position2[0])
            dy = abs(position1[1] - position2[1])

            x1 = position1[0] 
            x2 = position2[0] 
            y1 = position1[1] 
            y2 = position2[1] 

            penalty = 0

            if (self.is_odd(y1) and self.is_even(y2) and (x2 < x1)) or (self.is_odd(y2) and self.is_even(y1) and (x1 < x2)):
                
                penalty = 1

            return max(dy, dx + math.floor(dy/2) + penalty); 

        #return max(abs(position1[0]-position2[0]), abs(position1[1]-position2[1]), abs((position2[0] - position2[1])*-1 - (position1[0] - position1[1])*-1))
        return 0
    


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



    # GET_NEW_PATH
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

            if actual_nodebase.get_position() == initial_nodebase.get_position() or not self.occupied(actual_nodebase.get_position()):
                
                # Add the actual position to the closed list
                if actual_nodebase.get_position() not in closed_list.keys():

                    closed_list[actual_nodebase.get_position()] = actual_nodebase
                    # Get all its feasible neighbours
                    neighbours = list(self.get_feasible_neighbours(actual_nodebase, final_nodebase))
                    #print("Checking")
                    #actual_nodebase.toString()
                    #for tile in neighbours:
                    #    tile.toString()
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



    # GET_ATTACKING_POSITIONS
    # Calculate posible attacking positions
    def get_attacking_positions(self, movement_positions, unit):

        attacking_positions = set()

        for movement in movement_positions:

            attacking_positions.update(set(self.get_movement_positions_from_position(movement.get_position(),1)))
        
        final_attacking_positions = list()

        for i in attacking_positions.copy():
            unit_in_position = self.get_unit_in_position(i)
            if self.occupied(i) and unit_in_position.get_team() != unit.get_team() and not self.nodebase_exists(i, final_attacking_positions):
                final_attacking_positions.append(i)
                #attacking_positions.remove(i)
                       
        if self.selected_unit != None:

            self.selected_unit_attack_movements = final_attacking_positions

        return final_attacking_positions
    


    # GET_ENEMY_TEAMS
    # Return the teams that are enemies from the argument team
    def get_enemy_teams(self, unit_team):
        enemy_teams = list()
        for teams in self.team_groups:
            if unit_team not in teams:
                for team in teams:
                    enemy_teams.append(team)
        return enemy_teams



    # GET_NEAREST_ENEMY_UNIT
    # Return the nearest enemy unit from the argument unit
    def get_nearest_enemy_unit(self, origin_unit):

        enemy_teams = self.get_enemy_teams(origin_unit.get_team())
        nearest_enemy_unit = None
        shortest_path_to_nearest_enemy_unit = self.map_data.get_rows() * self.map_data.get_cols()

        for team in enemy_teams:

            enemy_units = self.get_units_from_team(team).get_unit_array()

            for enemy_unit in enemy_units:

                distance = self.movements_between_positions(origin_unit.get_nodebase(), enemy_unit.get_nodebase())

                if distance < shortest_path_to_nearest_enemy_unit:

                    shortest_path_to_nearest_enemy_unit = distance
                    nearest_enemy_unit = enemy_unit

        return nearest_enemy_unit
        










    

        



