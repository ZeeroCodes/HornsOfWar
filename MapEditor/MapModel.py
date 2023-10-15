import pygame
import math
import os

from copy import copy, deepcopy
from pygame.locals import *
from MapEditor.Widgets.NodeBase import NodeBase
from MapEditor.Units.UnitArray import UnitArray
from MapEditor.Units.HumanWarrior import HumanWarrior
from MapEditor.Units.UndeadGhost import UndeadGhost
from MapEditor.MapData import MapData
from MapEditor.Units.Unit import Unit


available_movements_even_col = ((-1, 0), (-1, 1), (0, 1), (1, 0), (0, -1), (-1, -1))
available_movements_odd_col = ((-1, 0), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))

RADIUS = 50

class MapModel(object):

    def __init__(self):
        pygame.init()
        self.map_data = MapData(12, 12)

        self.team_units = [0]
        self.team_groups = [0]
        self.money = 100
        self.rect_view = None
        self.update_map_data_dictionary()

        self.unit_dictionary = {
            '111': 'HumanWarrior',
            '110': 'HumanWarrior',
            '211': 'UndeadGhost',
            '210': 'UndeadGhost'}
    


    def print_units(self):
        print("#########################################")
        print("Printing units...")
        cont = 1
        for group in self.team_groups[1:]:
            print("Group " + str(cont))
            cont += 1
            for team in group:
                print("For team " + str(team) + " :")
                for unit in self.team_units[team].get_unit_array():
                    #print(unit)
                    unit.toString()


    #################################################################
    ################ GETTERS ########################################
    #################################################################



    # GET_ROWS
    # Returns the actual amount of rows of the map
    def get_rows(self):
        return self.map_data.get_rows()



    # GET_COLS
    # Return the actual amount of columns of the map
    def get_cols(self):
        return self.map_data.get_cols()



    # GET_MONEY
    # Returns current money of the player
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



    # GET_SELECTED_UNIT
    # Returns the selected unit
    def get_selected_unit(self):
        return self.selected_unit



    # GET_TILE_DICTIONARY
    # Return the tile dictionary
    def get_tile_dictionary(self):
        return self.map_data.get_tiles_dictionary()



    # GET_TEAM_UNITS
    # Returns the total of units
    def get_team_units(self):
        return self.team_units



    # GET_GROUP
    # Returns the group of teams the unit team is in
    def get_group(self, unit):

        team = unit.get_team()

        for group_team in self.team_groups[1:]:

            if team in group_team:

                return group_team


    # GET_RECT_VIEW
    # Returns the square to print on the screen
    def get_rect_view(self):
        return self.rect_view



    #################################################################
    ################ SETTERS ########################################
    #################################################################



    # SET_MONEY
    # Sets the aumount of money the player has
    def set_money(self, money):

        self.money = money



    # SET_MAP_DATA
    # Sets the map_data as the argument
    def set_map_data(self, map_data):

        self.map_data = map_data



    # SET_ROWS
    # Set a new amount of rows to the map data
    def set_rows(self, number):

        self.map_data.set_rows(number)
        self.update_map_data_dictionary()



    # SET_COLS
    # Set a new amount of columns to the map_data    
    def set_cols(self, number):

        self.map_data.set_cols(number)
        self.update_map_data_dictionary()



    # SET_RECT_VIEW
    def set_rect_view(self, position = (0, 80), dimensions = (600, 800)):

        self.rect_view = pygame.Rect(position, dimensions)



    #################################################################
    ################ FUNCTIONS ######################################
    #################################################################



    #################################################################
    ################ UNITS RELATED###### ############################
    #################################################################



    # MODIFY_UNIT_POSITION
    # Modifies the position of the argument unit
    def modify_unit_position(self, target_unit, nodebase):

        if target_unit and nodebase:

            final_nodebase = nodebase

            if not isinstance(nodebase, NodeBase):

                final_nodebase = NodeBase(nodebase, self.get_coords_by_position(nodebase))

            self.team_units[target_unit.get_team()].modify_unit_position(target_unit, final_nodebase)



    # ADD_UNIT
    # Adds a unit to the friendly or enemy array
    def add_unit(self, unit = HumanWarrior((0,0))):

        if unit:

            # If there is a unit at the selected position, delete it
            unit_in_position = self.get_unit_in_position(unit.get_position())
            
            if isinstance(unit_in_position, Unit):

                self.delete_unit(unit_in_position)

            unit_team = unit.get_team()
            unit_group = unit.get_group()

            # Increases the number of groups if the unit one doesn't exist
            if unit_group > self.team_groups[0]:

                while unit_group > self.team_groups[0]:

                    self.team_groups.append([])
                    self.team_groups[0] = self.team_groups[0] + 1
    
            # Increases the number of teams if the unit one doesn't exist and adds it to the group if it is not already inside
            if unit_team > self.team_units[0]:

                while unit_team > self.team_units[0]:

                    self.team_units.append(UnitArray())
                    self.team_units[0] = self.team_units[0] + 1
            
            if not unit_team in self.team_groups[unit_group]:

                self.team_groups[unit_group].append(unit_team)

            self.team_units[unit_team].add_unit(unit)

            self.print_units()



    # DELETE_UNIT
    # Deletes a unit from the friendly or enemy ones
    def delete_unit(self, unit):

        self.team_units[unit.get_team()].remove_unit(unit)



    # DELETE_ALL_UNITS
    # Deltes all units for every team
    def delete_all_units(self):

        self.team_units = [0]
        self.team_groups = [0]



    # GET_UNIT_BY_ID
    # Return a unit type depending on the id
    def get_unit_by_id(self, id):
        
        unit_name = self.unit_dictionary[id]

        if unit_name == 'HumanWarrior':

            human_warrior = HumanWarrior()
            image = human_warrior.get_image()
            human_warrior.set_image(None)
            human_warrior2 = deepcopy(human_warrior)
            human_warrior2.set_image(image)

            return human_warrior2

        elif unit_name == 'UndeadGhost':

            undead_ghost = UndeadGhost()
            image = undead_ghost.get_image()
            undead_ghost.set_image(None)
            undead_ghost2 = deepcopy(undead_ghost)
            undead_ghost2.set_image(image)

            return undead_ghost2



    #################################################################
    ################ ESSENTIALS #####################################
    #################################################################



    # CLOSEST_HEXAGON
    # This function finds and return the nearest center of an hexagon to the actual position of the mouse
    def closest_hexagon(self, point):

        if point == None or not self.map_data.get_tiles_dictionary():

            return None

        dictionary = dict()
        keys = self.map_data.get_tiles_dictionary().keys()

        for element in keys:

            dictionary[element] = self.map_data.get_tiles_dictionary()[element].get_pixel_position()

        _, hex_pos = min(dictionary.items(), key=lambda x: math.sqrt(math.pow(x[1][0]-point[0],2) + math.pow(x[1][1]-point[1],2)))    
        
        if math.sqrt(math.pow(hex_pos[0]-point[0],2) + math.pow(hex_pos[1]-point[1],2)) <= RADIUS:

            return hex_pos

        else:

            return None



    # GET_POSITION_BY_COORDS
    # Return a hexagon position from its pixel coordinates
    def get_position_by_coords(self, position_coords): 

        tile_dictionary = self.map_data.get_tiles_dictionary()
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

        if position:

            if isinstance(position, NodeBase):

                position = position.get_position()

            for team in self.team_units[1:]:

                for unit in team.get_unit_array():

                    if unit.get_position() == position:

                        return unit 

        return None



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

        if position:

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



    #################################################################
    ################ MAP RELATED ####################################
    #################################################################
    


    # GET_MAXIMUM_TILE
    # Returns the tile with the largest row and column and None if there is no tiles on the dictionary
    def get_maximum_tile(self):

        row = self.map_data.get_rows()
        column = self.map_data.get_cols()

        if row == 0 or column == 0:
            return None

        return self.map_data.get_tiles_dictionary()[(row-1, column-1)]



    # MAP_SCROLL
    # Moves the hexagons to the desired direction
    def map_scroll(self, direction):

        if direction:

            self.rect_view = pygame.Rect.move(self.rect_view, direction[0], direction[1])

    

    # GET_PAINTING_UNITS
    # Gets a dictionary with all units in the view screen
    def get_painting_units(self, dictionary):
        
        unit_dictionary = dict()

        if dictionary:

            for team in self.team_units[1:]:

                for unit in team.get_unit_array():

                    if unit.get_position() in dictionary.keys():

                        unit_image = unit.get_image()
                        unit.set_image()
                        new_unit = deepcopy(unit)
                        unit.set_image(unit_image)
                        new_unit.set_image(unit_image)
                        new_unit.set_pixel_position(dictionary[unit.get_position()].get_pixel_position())
                        unit_dictionary[unit.get_position()] = new_unit

        return unit_dictionary



    # GET_PAINTING_DICTIONARY
    def get_painting_dictionary(self):

        # Loads tiles dictionary and checks it is not empty
        old_tiles_dictionary = self.map_data.get_tiles_dictionary()

        if not old_tiles_dictionary:

            return None

        # Loads tile (0, 0) from dictionary
        real_initial_position = old_tiles_dictionary[(0, 0)].get_pixel_position()

        # Pixel coordinates of the rect (left, top)
        rect_pixel_position = (self.rect_view.left, self.rect_view.top)
        new_rect_pixel_position = rect_pixel_position

        if rect_pixel_position[0] < real_initial_position[0]:

            new_rect_pixel_position = (real_initial_position[0], new_rect_pixel_position[1])

        if rect_pixel_position[1] < real_initial_position[1]:

            new_rect_pixel_position = (new_rect_pixel_position[0], real_initial_position[1])
       
        # Pixel coordinates of the nearest hexagon
        original_position = self.closest_hexagon(new_rect_pixel_position)

        if original_position == None:

            return None
        
        # Position of the nearest hexagon
        initial_position = self.get_position_by_coords(original_position)
        
        # Calculates the initial pixel position of the first hexagon it is gonna be printed
        initial_pixel_position = (original_position[0] - rect_pixel_position[0], original_position[1] - rect_pixel_position[1] + 80)
        
        hex_height = int(RADIUS*math.cos(math.pi/6))
        
        number_of_rows = int((self.rect_view.height + 100)/math.ceil(2*hex_height))
        number_of_cols = int((self.rect_view.width + 100)/math.ceil((3*RADIUS)/2))

        max_rows = self.map_data.get_rows()
        max_cols = self.map_data.get_cols()

        if number_of_rows + initial_position[0] > max_rows:
            number_of_rows = max_rows - initial_position[0]

        if number_of_cols + initial_position[1] > max_cols:
            number_of_cols = max_cols - initial_position[1]

        new_tiles_dictionary = dict()

        if not self.is_even_column(initial_position):

            initial_position = (initial_position[0], initial_position[1] - 1)
            number_of_cols += 1
            initial_pixel_position = (initial_pixel_position[0] - (3/2)*RADIUS, initial_pixel_position[1] - hex_height)


         # For every row
        for i in range(0, number_of_rows):

            # Set starting hexagon
            point = (int(initial_pixel_position[0]), int(initial_pixel_position[1] + i * 2 * hex_height))

            # For every column
            for j in range(0, number_of_cols):

                actual_position = (i + initial_position[0], j + initial_position[1])

                # If the column is even
                if self.is_even(j):

                    # Save the tile
                    new_tiles_dictionary[actual_position] = NodeBase(actual_position, point, None)
                
                # If the column is odd
                else:

                    # Set a new y coordenate for the hexagon due it has to be a little down and print it
                    new_point = (int(point[0]), int(point[1] + hex_height))
                    new_tiles_dictionary[actual_position] = NodeBase(actual_position, new_point, None)
                
                # Set a new point
                point = (point[0] + (3*RADIUS)/2, point[1])

        

        #print(new_tiles_dictionary)

        #If old dictionary was not empty
        if old_tiles_dictionary:

            new_keys = new_tiles_dictionary.keys()

            # If the key in the new dictionary existed in the old one, get its nodebase
            for key in new_keys:

                key_terrain = old_tiles_dictionary[key].get_terrain()

                if key_terrain != None:

                    new_tiles_dictionary[key].set_terrain(key_terrain)

        else:

            return None

        return new_tiles_dictionary
  
    

    # LOAD_MAP
    # Loads map from a text file
    def load_map(self):

        rows = 0
        cols = 0
        groups = 0
        teams = 0
        dictionary = dict() 
        self.team_units = [0]
        self.team_groups = [0]

        with open(os.path.abspath(os.getcwd()) + "\\Maps\\new_map.txt", 'r') as f:

            dictionary = dict()
            lines = f.readlines()
            rows = int(lines[0])
            cols = int(lines[1])
            groups = int(lines[2])
            teams = int(lines[3])
            self.money = int(lines[4])

            if self.team_groups[0] < groups:

                while self.team_groups[0] < groups:
                    
                    self.team_groups[0] += 1
                    self.team_groups.append([])

            if self.team_units[0] < teams:

                while self.team_units[0] < teams:
                    
                    self.team_units[0] += 1
                    self.team_units.append(UnitArray())


            tiles_number = rows * cols
            for line in lines[5:tiles_number+5]:

                line = line.split(' ')

                position = (int(line[0]), int(line[1]))
                pixel_position = (int(line[2]), int(line[3]))
                terrain = int(line[4])
                unit_nodebase = NodeBase(position, pixel_position, terrain)
                dictionary[position] = unit_nodebase

                if len(line) > 5:

                    unit = self.get_unit_by_id(line[5])
                    unit.set_id(line[5])
                    unit.set_position(unit_nodebase)
                    team = int(line[6])
                    unit.set_team(team)
                    group = int(line[7])
                    unit.set_group(group)
                    unit.set_damage(int(line[10]))
                    unit.set_health(int(line[8]))
                    unit.set_max_health(int(line[9]))
                    unit.set_movement(int(line[11]))

                    if not team in self.team_groups[group]:

                        self.team_groups[group].append(team)
                    
                    self.add_unit(unit)

        self.map_data = MapData(rows, cols, dictionary)



    # SET_TILE_TERRAIN
    # Set a new terrain for the nodebase on key
    def set_tile_terrain(self, nodebase_key, terrain):

        key = nodebase_key

        if isinstance(nodebase_key, NodeBase):

            key = nodebase_key.get_position()

        # If nodebase is not null
        if key:

            # Set new nodebase
            self.map_data.set_terrain(key, terrain)

    

    # SET_NEW_NODEBASE
    # Sets a new nodebase for the key
    def set_new_nodebase(self, key, nodebase):

        # If nodebase is not null
        if nodebase:

            # Set new nodebase
            self.map_data.set_nodebase(key, nodebase)



    # UPDATE_MAP_DATA_DICTIONARY
    # Updates the dictionary with the new rows and columns
    def update_map_data_dictionary(self):

        # Creation of the new dictionary
        new_tiles_dictionary = dict()
        
        # First hexagon position
        initial_point = (RADIUS, 150)
        if self.map_data.get_tiles_dictionary():
            initial_point = self.map_data.get_tiles_dictionary()[(0,0)].get_pixel_position()
        

        # Get dimension of the map
        rows = self.map_data.get_rows()
        cols = self.map_data.get_cols()

        # Calculate heigth of the hexagon
        side_long = int(RADIUS*math.cos(math.pi/6))

        # For every row
        for i in range(0, rows):

            # Set starting hexagon
            point = (int(initial_point[0]), int(initial_point[1] + i * 2 * side_long))

            # For every column
            for j in range(0, cols):

                # If the column is even
                if self.is_even(j):

                    # Save the tile
                    new_tiles_dictionary[(i,j)] = NodeBase((i,j), point, None)
                
                # If the column is odd
                else:

                    # Set a new y coordenate for the hexagon due it has to be a little down and print it
                    new_point = (int(point[0]), int(point[1] + side_long))
                    new_tiles_dictionary[(i,j)] = NodeBase((i,j), new_point, None)
                
                # Set a new point
                point = (point[0] + (3*RADIUS)/2, point[1])
        
        # Update new dictionary with the terrains of the previous dictionary
        old_tiles_dictionary = self.map_data.get_tiles_dictionary()

        # If old dictionary was not empty
        if old_tiles_dictionary:

            new_keys = new_tiles_dictionary.keys()
            old_keys = old_tiles_dictionary.keys()

            # If the key in the new dictionary existed in the old one, get its nodebase
            for key in new_keys:

                if key in old_keys:

                    new_tiles_dictionary[key] = old_tiles_dictionary[key]

        for team in self.team_units[1:]:

            for unit in team.get_unit_array().copy():

                if not unit.get_position() in new_tiles_dictionary.keys():

                    self.delete_unit(unit)
        
        # Update dictionary
        self.map_data.set_tiles_dictionary(new_tiles_dictionary)

    

    # ALL_POSITIONS_HAVE_TERRAINS
    def all_positions_have_terrains(self):

        dictionary = self.map_data.get_tiles_dictionary()

        if dictionary:

            for value in dictionary.values():

                if value.get_terrain() == None:

                    return False

        return True



    # CLEAR_ALL_TERRAINS
    # Removes every terrain from every tile
    def clear_all_terrains(self):

        dictionary = self.map_data.get_tiles_dictionary()

        for key in dictionary.keys():
            self.map_data.set_terrain(key, None)



    # SAVE_MAP
    def save_map(self):

        rows = self.map_data.get_rows()
        cols = self.map_data.get_cols()
        dictionary = self.map_data.get_tiles_dictionary()

        lines = []

        lines.append(str(rows))
        lines.append("\n" + str(cols))
        lines.append("\n" + str(self.team_groups[0]))
        lines.append("\n" + str(self.team_units[0]))
        lines.append("\n" + str(self.money))

        for tile in dictionary.values():
            
            position = tile.get_position()
            pixel_position = tile.get_pixel_position()
            terrain = tile.get_terrain()
            unit = self.get_unit_in_position(position)

            line = "\n" + str(int(position[0])) + " " + str(int(position[1])) + " " + str(int(pixel_position[0])) + " " + str(int(pixel_position[1])) + " " + str(int(terrain))

            if unit:

                unit_id = unit.get_id()
                team = unit.get_team()
                group = unit.get_group()
                health = unit.get_health()
                max_health = unit.get_max_health()
                damage = unit.get_damage()
                movement = unit.get_movement()

                line +=  " " + str(int(unit_id)) + " " + str(int(team)) + " " + str(int(group)) + " " + str(int(health)) + " " + str(int(max_health)) + " " + str(int(damage)) + " " + str(int(movement))

            lines.append(line)

        lines.append("\n" + "team 1")
        lines.append("\n" + "0")
        lines.append("\n" + "team 2")
        lines.append("\n" + "0")

        with open(os.path.abspath(os.getcwd()) + "\\Maps\\new_map.txt", 'w') as f:

            f.writelines(lines)

            f.close()
















    

        



