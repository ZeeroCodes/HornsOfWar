import pygame
import math
import numpy as np
from pygame.locals import *
from random import random

from Scripts.MapModel import MapModel
from Scripts.MapView import MapView

from Scripts.Widgets.NodeBase import NodeBase

from Scripts.Units.Humans.HumanWarrior.HumanWarrior import HumanWarrior
from Scripts.Units.Humans.HumanHero.HumanHero import HumanHero
from Scripts.Units.Undead.UndeadGhost.UndeadGhost import UndeadGhost
from Scripts.Units.Undead.UndeadHero.UndeadHero import UndeadHero

import Constants

HEIGHT = Constants.RADIUS*math.cos(math.radians(30))

class Map(object):

    def __init__(self, map_name = "new_map"):
        
        pygame.init()
        self.map_model = MapModel()
        self.map_model.load_map(map_name)
        self.map_view = MapView()

        self.clicked = False

        self.previous_position = None
        self.last_path_position = None
        self.last_unit_in_last_position = False

        

        self.turn = 1
        self.finished = False
        self.savegame_number = 0


    # CREATE_NEW_UNIT
    # Creates new unit in friendly or enemy array
    def create_new_unit(self, unit = HumanWarrior()):

        if not self.map_model.occupied(unit.get_position()):

            self.map_model.add_unit(unit, unit.get_team())



    # AUXILIAR
    # PRINT_PATH
    # Prints the Nodebases of a list
    def print_path(self, path):

        if path:

            for tile in path:

                tile.toString()

        else:

            print("Path vacio")
    
    

    # UPDATE_MAP_MOVING
    # Based on the original update_map, but with the minimum requisites to make the movement
    def update_map_moving(self, unit):

        # Draw map tiles
        self.map_view.draw_map(self.map_model.get_tile_dictionary())
        
        #self.map_model.print_units()
        self.map_view.print_units(self.map_model.get_team_units(), self.map_model.get_tile_dictionary())
        pygame.display.update()

        # Draw an hexagon where the mouse pointer is
        self.print_mouse_hexagon()



    # START_ATTACKING_MOVEMENT
    # This function makes the attacking unit move half ditance to the attacked unit and return
    def start_attacking_movement(self, path, unit = None):
        print("Starting attacking movement...")
        path_movement = path.copy()

        # Get position actual and final (unit attacking and unit attacked)
        actual_position = unit.get_position()  
        actual_pixel_position = unit.get_pixel_position()

        final_position = path_movement[0]
        final_pixel_position = self.map_model.get_coords_by_position(final_position)

        # Get all desired pixels between these 2 positions to paint the unit on and simulate movement
        horizontal = np.round(list(np.linspace(actual_pixel_position[0], final_pixel_position[0], Constants.MOVEMENT_SPEED*20)))[:int((Constants.MOVEMENT_SPEED*20)/2)]
        vertical = np.round(list(np.linspace(actual_pixel_position[1], final_pixel_position[1], Constants.MOVEMENT_SPEED*20)))[:int((Constants.MOVEMENT_SPEED*20)/2)]

        # Make aproximation to the attacked unit
        for i in range(len(horizontal)):

            new_pixel_position = (int(horizontal[i]), int(vertical[i]))
            nodebase = NodeBase(actual_position, new_pixel_position)
            self.map_model.modify_unit_position(unit, nodebase)
            #self.map_model.set_selected_unit_position(nodebase)
            self.update_map_moving(unit)
        
        # Reverse the list to come back
        horizontal = list(reversed(horizontal))
        vertical = list(reversed(vertical))

        # Move the unit to its positions
        for i in range(len(horizontal)):

            new_pixel_position = (int(horizontal[i]), int(vertical[i]))
            nodebase = NodeBase(actual_position, new_pixel_position)
            self.map_model.modify_unit_position(unit, nodebase)
            #self.map_model.set_selected_unit_position(nodebase)
            self.update_map_moving(unit)



    # START_MOVEMENT
    # Manages the movement positions and calling to the drawing functions
    def start_movement(self, path, unit = None, attacking = False):

        print("Starting movement...")

        # If the unit is attacking someone, add the positions where it will be attacking to the list,
        # so it can come back later
        if attacking:

            path_movement = path.copy()
            path_movement.insert(0, path[1])
            path_movement = list(reversed(path_movement))[1:]
        
        else:

            path_movement = list(reversed(path.copy()))[1:]
        
        # This process has to be done for every tile in the path
        for tile in path_movement.copy():

            # When it only remains to attack the unit, call the other function and end loop
            if attacking and len(path_movement) == 2:

                self.start_attacking_movement(path_movement, unit)
                break;

            # Break loop if there is no more tile to move to
            if path_movement == []:

                break;

            # Get and eliminate a tile from the path, get its pixel positions
            final_position = path_movement.pop(0)
            final_position = self.map_model.get_coords_by_position(final_position)
            actual_position = tile.get_position()
            actual_pixel_position = unit.get_pixel_position()

            # Calculate pixel positions between these 2 positions
            horizontal = np.round(list(np.linspace(actual_pixel_position[0], final_position[0], Constants.MOVEMENT_SPEED*20)))
            vertical = np.round(list(np.linspace(actual_pixel_position[1], final_position[1], Constants.MOVEMENT_SPEED*20)))

            # Move the unit and update its position
            for i in range(len(horizontal)):

                new_pixel_position = (int(horizontal[i]), int(vertical[i]))
                nodebase = NodeBase(actual_position, new_pixel_position)
                self.map_model.modify_unit_position(unit, nodebase)
                #self.map_model.set_selected_unit_position(nodebase)
                self.update_map_moving(unit)
                # This is a delay
                #time = pygame.time.get_ticks() + 1
                #while pygame.time.get_ticks() < time:
                #    pass



    # MANAGE_SELECTED_UNIT
    # Manages the selected unit
    def manage_selected_unit(self):

        # Get mouse position and mouse position
        mouse_pixel_position = self.map_model.closest_hexagon(pygame.mouse.get_pos())
        mouse_position = self.map_model.get_position_by_coords(mouse_pixel_position)

        selected_unit = self.map_model.get_selected_unit()

        # If the mouse is inside the map
        if mouse_position != None:

            # Gets the unit at the mouse position
            unit_in_position = self.map_model.get_unit_in_position(mouse_position)

            # If there is no selected unit
            if selected_unit == None:  

                # If the clicked unit is friendly
                if unit_in_position != None and unit_in_position.get_team() == 1 and not unit_in_position.get_moved():

                    # Set the selected unit to the clicked unit
                    self.map_model.set_selected_unit(unit_in_position)
            
            # If there is a selected unit
            else:

                # If the position is occupied by a unit
                if self.map_model.occupied(mouse_position):
                    
                    self.map_model.set_selected_tile(None)

                    # If the unit is a friendly one
                    if self.map_model.is_friendly(unit_in_position):

                        # If the clicked unit is the same as the selected one
                        if unit_in_position == selected_unit:

                            # Deselect the selected unit
                            self.map_model.set_selected_unit(None)
                            self.map_model.set_selected_unit_movements()
                            self.previous_position = None
                            self.last_path_position = None

                        else:

                            # If the unit is owned by the player select it
                            if unit_in_position.get_team() == 1 and not unit_in_position.get_moved():

                                # Change the selected unit
                                self.map_model.set_selected_unit(unit_in_position)
                                self.last_path_position = unit_in_position.get_position()
                                self.previous_position = unit_in_position.get_position()
                        
                            # If the unit is an allied but not controlled by the player, deselect unit
                            else:

                                self.map_model.set_selected_unit(None)
                                self.map_model.set_selected_unit_movements()
                                self.previous_position = None
                                self.last_path_position = None
      
                    # If the unit is enemy, move and attack it 
                    elif not self.map_model.is_friendly(unit_in_position):
                                                    
                        last_position = self.map_model.get_path()[1].get_position()

                        # If the position where it is gonna attack is reachable
                        if self.map_model.reachable(last_position):
                            # Change its position and attack
                            self.start_movement(self.map_model.get_path(), selected_unit, True)
                            self.map_model.set_path()
                            unit_in_position.hurt(self.get_attack_damage(selected_unit, unit_in_position))
                            self.map_model.set_unit_moved(selected_unit, True)

                        # If the last position is not reachable, move the unit to the maximum position
                        # it can move                            
                        else:

                            movement_path = []

                            # Check wich positions are in both path and movement tiles
                            for tile in self.map_model.get_path().copy():

                                if self.map_model.nodebase_exists(tile, self.map_model.get_selected_unit_movements()):

                                    movement_path.append(tile)

                            # Append the initial position
                            movement_path.append(selected_unit.get_nodebase())

                            # Start movement
                            #self.print_path(movement_path)
                            self.start_movement(movement_path, selected_unit)
                            self.map_model.set_path()
                            self.map_model.set_unit_moved(selected_unit, True)

                        # If the unit health gets beyond 0, it is killed
                        if unit_in_position.get_health() <= 0:

                            self.map_model.delete_unit(unit_in_position)
                            self.map_model.earn(10)

                        # Deselect unit
                        self.map_model.set_selected_unit(None) 
                        self.map_model.set_selected_unit_movements()
                        self.previous_position = None
                        self.last_path_position = None
                    
                    # Any other option deselects the selected unit
                    else:

                        self.map_model.set_selected_unit(None)
                        self.map_model.set_selected_unit_movements()
                        self.previous_position = None
                        self.last_path_position = None

                # If the position clicked is empty, move the selected unit to that position
                else: 

                    # If the position is reachable
                    if self.map_model.reachable(mouse_position):

                        # Updates unit position
                        self.start_movement(self.map_model.get_path(), selected_unit)
                        self.map_model.set_unit_moved(selected_unit, True)
                        self.map_model.set_path()
                        self.map_model.set_selected_unit_position(NodeBase(mouse_position, mouse_pixel_position))
                    
                    # Deselects unit
                    self.map_model.set_selected_unit(None) 
                    self.map_model.set_selected_unit_movements()
                    self.previous_position = None
                    self.last_path_position = None

        # If the mouse is outside the map, deselect the unit
        else:
            self.map_model.set_selected_unit(None) 
            self.map_model.set_selected_unit_movements()
            self.previous_position = None
            self.last_path_position = None



    # PRINT_SELECTED_UNT
    # Prints the path to the selected unit dependind on the obstacles
    def print_selected_unit(self):

        if self.map_model.get_selected_unit() != None:

            # Get and print movement tiles of the selected unit
            selected_unit_movements = self.map_model.get_movement_positions(self.map_model.get_selected_unit())
            self.map_view.print_unit_movements(selected_unit_movements)
            
            # Print a less transparent hexagon and a blue edge at the selected unit
            self.map_view.paint_hexagon(self.map_model.get_coords_by_position(self.map_model.get_selected_unit().get_position()), pygame.Color(0, 255, 0, 100))
            self.map_view.draw_hexagon(self.map_model.get_coords_by_position(self.map_model.get_selected_unit().get_position()), Constants.BLUE) 
            
            # Get mouse position and pixel position
            mouse_pixel_position = self.map_model.closest_hexagon(pygame.mouse.get_pos())
            mouse_position = self.map_model.get_position_by_coords(mouse_pixel_position)

            # Get selected unit
            selected_unit = self.map_model.get_selected_unit()

            # If the mouse is inside the map
            if mouse_pixel_position != None: 

                # Create initial nodebase and final nodebases
                nodebase1 = NodeBase(selected_unit.get_position(), self.map_model.get_coords_by_position(selected_unit.get_position()))
                nodebase2 = NodeBase(mouse_position, mouse_pixel_position)

                # If the selected hexagon is not occupied
                if not self.map_model.occupied(mouse_position):
                    
                    self.last_unit_in_position = None

                    # If the mouse hasn't moved of the last hexagon, don't calculate path again
                    if mouse_position != self.previous_position:

                        # Update auxiliar positions
                        self.previous_position = mouse_position
                        self.last_path_position = mouse_position
                        # Calculate new path
                        self.map_model.get_new_path(nodebase1, nodebase2)

                    # If the path is not empty, print it
                    if self.map_model.get_path():

                        self.map_view.print_path(self.map_model.get_path())
                
                # If the hexagon is occupied
                else:

                    # Get the unit in the mouse position
                    unit_in_position = self.map_model.get_unit_in_position(mouse_position)
         
                    # If the unit is friendly
                    if self.map_model.is_friendly(unit_in_position):

                        # If is a different position than the last_one
                        if mouse_position != self.previous_position:
                            
                            # Update variables
                            self.previous_position = mouse_position
                            self.last_path_position = mouse_position
                            self.last_unit_in_position = unit_in_position
                    
                    # If the unit is an enemy
                    else:
         
                        if self.map_model.can_move(self.map_model.get_selected_unit()):
                           
                            feasible_neighbours = self.map_model.get_feasible_neighbours(selected_unit.get_nodebase())
                            distance_between_units = self.map_model.movements_between_positions(nodebase1, nodebase2)
                            if not feasible_neighbours and distance_between_units == 1:
                                print("PEGADO Y RODEADO")
                                self.map_model.get_new_path(nodebase1, nodebase2)

                            # If is a different position than the last_one
                            if mouse_position != self.previous_position:

                                # If the last position was an empty one, gets the path to that position and then
                                # adds the final movement to attack the enemy
                                if self.last_unit_in_position == None:

                                    nodebase_last = NodeBase(self.last_path_position, self.map_model.get_coords_by_position(self.last_path_position))
                                    path1 = self.map_model.get_new_path(nodebase1, nodebase_last)
                                    path2 = self.map_model.get_new_path(nodebase_last, nodebase2)
                                    self.map_model.set_path(path2 + path1[1:])
                                
                                # If the last position had a unit in it, theres no previous position, so recalculates
                                # the path to the shortest one
                                else:

                                    self.map_model.get_new_path(nodebase1, nodebase2)
                                
                                # Updates last unit in the position
                                self.last_unit_in_position = unit_in_position

                        else:

                            self.map_model.get_new_path(nodebase1, nodebase2)
                            
                        # Prints path
                        self.previous_position = mouse_position
                        path = self.map_model.get_path()
                        self.map_view.print_path(path[1:])
                        self.map_view.print_path(path[:2], Constants.RED)

      

    # GET_ATTACK_MOVEMENTS
    # Calls the function to calculate the possible attack positions
    def get_attack_movements(self):
        # Get mouse position and pixel position
        self.map_model.get_attacking_positions(self.map_model.get_selected_unit_movements(), self.map_model.get_selected_unit())         



    # PRINT_MOUSE_HEXAGON
    # Prints the mouse hexagon with the color depending on the position
    # Friendly = BLUE
    # Enemy = RED
    # Empty = GOLD
    def print_mouse_hexagon(self):
        mouse_pixel_position = self.map_model.closest_hexagon(pygame.mouse.get_pos())
        mouse_position = self.map_model.get_position_by_coords(mouse_pixel_position)
        if not self.map_model.occupied(mouse_position):
            self.map_view.print_mouse_hexagon(mouse_pixel_position)
        else:
            if self.map_model.get_unit_in_position(mouse_position).get_friendly():
                self.map_view.print_mouse_hexagon(mouse_pixel_position, Constants.BLUE)
            else:
                self.map_view.print_mouse_hexagon(mouse_pixel_position, Constants.RED)



    # CALCULATE_TILE_VALUE
    # Return the value of the tile for unit movement
    def calculate_tile_value(self, unit, attacked_unit)->int:

        unit_terrain = self.map_model.get_real_map_nodebase(unit.get_position())
        unit_terrain_bonus = float(unit.get_terrain_bonus(unit_terrain)/100.0) # Value of the terrain, until different terrains it is 1
        
        attacked_unit_terrain = self.map_model.get_real_map_nodebase(attacked_unit.get_position())
        attacked_unit_terrain_bonus = float(unit.get_terrain_bonus(attacked_unit_terrain)/100.0) # Value of the terrain, until different terrains it is 1
        
        unit_estimated_damage = unit.get_damage()*(100 - attacked_unit_terrain_bonus)/100
        movement = Constants.IA_MOVEMENT_VALUE * unit_terrain_bonus
        can_attack = 0
        can_kill = 0
        is_heroe = 0
        percentage_of_damage = (Constants.IA_BONUS_FOR_DAMAGE_PERCENTAGE * unit_estimated_damage) / attacked_unit.get_max_health()
        level_bonus = Constants.IA_BONUS_PER_LEVEL * attacked_unit.get_level()
        health_difference = attacked_unit.get_max_health() - attacked_unit.get_health()

        if attacked_unit != None:

            can_attack = Constants.IA_BONUS_PER_CAN_ATTACK

        if unit_estimated_damage >= attacked_unit.get_health():

            can_kill = Constants.IA_BONUS_PER_CAN_KILL

        if isinstance(unit, HumanHero) or isinstance(unit, UndeadHero):

            is_heroe = Constants.IA_BONUS_PER_IS_HEROE

        return int(unit_estimated_damage * unit_terrain_bonus * (can_attack + can_kill + is_heroe + percentage_of_damage + level_bonus + health_difference))



    # GET_UNIT_VALUES_DICTIONARY
    # Return a dictionary of all available tiles and actions and a value for each of them
    def get_unit_values_dictionary(self, unit):

        unit_terrain = self.map_model.get_real_map_nodebase(unit.get_position())
        terrain = float(unit.get_terrain_bonus(unit_terrain)/100.0) # Value of the terrain, until different terrains it is 1
        
        # Get available movements and units that the unit can attack
        movement_dictionary = dict()
        available_movements = self.map_model.get_movement_positions(unit)
        available_movements.append(self.map_model.get_tile_dictionary()[unit.get_nodebase().get_position()])
        attacking_movements = self.map_model.get_attacking_positions(available_movements, unit)

        nearest_enemy_unit = self.map_model.get_nearest_enemy_unit(unit)
        path = self.map_model.get_new_path(unit.get_nodebase(), nearest_enemy_unit.get_nodebase())
        
        movement_value = 0


        # MOVEMENT CALCULATION WITHOUT ATTACKING FOR REACHABLE TILES
        for tile in available_movements:

            terrain_is_structure = tile.get_terrain_id() == Constants.STRUCTURE_TERRAIN 
            unit_is_hero = isinstance(unit, HumanHero) or isinstance(unit, UndeadHero)
            enough_gold_for_unit = self.map_model.get_money(unit.get_team()) >= Constants.HUMAN_WARRIOR_COST
            exist_feasible_spawnpoints = self.map_model.get_feasible_spawnpoints(unit.get_nodebase()) != []

            if terrain_is_structure and unit_is_hero and enough_gold_for_unit and exist_feasible_spawnpoints:
                    
                    movement_value = int(Constants.IA_STRUCTURE_MOVEMENT_VALUE*terrain)

            else:
                
                distance_to_nearest_enemy = self.map_model.movements_between_positions(tile, nearest_enemy_unit.get_nodebase())
                movement_value = int(Constants.IA_MOVEMENT_VALUE*terrain) - distance_to_nearest_enemy
        
                if self.map_model.nodebase_exists(tile, path):

                    movement_value += Constants.IA_BONUS_FOR_TILE_PATH

            if movement_value < 0:

                movement_value = 0

            movement_dictionary[(tile.get_position(), None)] = movement_value


        # MOVEMENT CALCULATION WITH ATTACKING FOR REACHABLE TILES
        for tile in attacking_movements:

            # Get the tile around the unit it can attack
            neighbour_tiles = self.map_model.get_movement_positions_from_position(tile.get_position(), 1)

            attacking_tiles = list()

            # For every tile around the unit that is a coincidence with the available movements, append to the list
            for attacking_tile in neighbour_tiles:

                if self.map_model.nodebase_exists(attacking_tile, available_movements):

                    attacking_tiles.append(attacking_tile)
            
            # For every tile where it can attack a enemy unit
            for attacking_tile in attacking_tiles:

                # Get the attacked_unit
                attacked_unit = self.map_model.get_unit_in_position(tile)
                movement_value = movement_dictionary[(attacking_tile.get_position(), None)]

                # Update value for attacking
                movement_value += self.calculate_tile_value(unit, attacked_unit)

                # Add this action to dictionary
                movement_dictionary[(attacking_tile.get_position(), tile.get_position())] = movement_value

        return movement_dictionary
    


    # GET_ATTACK_DAMAGE
    # Returns the damage a unit does when attacking
    def get_attack_damage(self, unit, attacked_unit):

        damage = unit.get_damage()

        terrain_bonification = attacked_unit.get_terrain_bonus(self.map_model.get_real_map_nodebase(attacked_unit.get_position()).get_terrain_id())

        return int(damage*((100.0 - terrain_bonification)/100.0))



    # AI_TURN
    # Manages the movement and attack of every enemy unit
    def AI_turn(self, unit):
        
        #if self.map_model.can_move(unit):

        # Get a dictionary with all available tile and its values
        movement_dictionary = self.get_unit_values_dictionary(unit)
    
        # If the dictionary is not empty
        if movement_dictionary:

            # Get the maximum value
            best_value = max(movement_dictionary.values()) 
            best_key = None
            # Search for the key of the maximum value
            for item in movement_dictionary.items():
                
                if item[1] == best_value:
                    
                    best_key = item[0]
        
            # If the best movement don't involucrate an attack
            if best_key[1] == None:

                # Calculate the path and make the movement
                nodebase1 = NodeBase(unit.get_position(), unit.get_pixel_position())
                nodebase2 = NodeBase(best_key[0], self.map_model.get_coords_by_position(best_key[0]))
                path = self.map_model.get_new_path(nodebase1, nodebase2)
                self.start_movement(path, unit, False)
            
            # If the best movement is an attack
            else:
                
                # Calculate path and start movement
                nodebase1 = NodeBase(unit.get_position(), unit.get_pixel_position())
                nodebase2 = NodeBase(best_key[0], self.map_model.get_coords_by_position(best_key[0]))
                nodebase3 = NodeBase(best_key[1], self.map_model.get_coords_by_position(best_key[1]))
                path1 = self.map_model.get_new_path(nodebase1, nodebase2)
                path2 = [nodebase3, nodebase2]
                self.start_movement(path2 + path1[1:], unit, True)

                # Damage enemy unit
                attacked_unit = self.map_model.get_unit_in_position(nodebase3)
                attacked_unit.hurt(self.get_attack_damage(unit, attacked_unit))

                # If the enemy health is under0, it is killed and it convert to team 2
                if (isinstance(unit, UndeadGhost) or isinstance(unit, UndeadHero)) and attacked_unit.get_health() <= 0:

                    self.map_model.delete_unit(attacked_unit)
                    nodebase = attacked_unit.get_nodebase()
                    ghost = UndeadGhost(nodebase, group = unit.get_group(), team = unit.get_team())
                    self.create_new_unit(ghost)
                    self.map_model.earn(Constants.HUMAN_WARRIOR_COST/2, unit.get_team())

        if isinstance(unit, UndeadHero):

            actual_standing_terrain = self.map_model.get_tile_dictionary()[unit.get_nodebase().get_position()].get_terrain_id()
            if actual_standing_terrain == Constants.STRUCTURE_TERRAIN:

                feasible_spawnpoints = self.map_model.get_feasible_spawnpoints(unit.get_nodebase())

                for feasible_spawnpoint in feasible_spawnpoints:

                    if self.map_model.get_money(unit.get_team()) >= Constants.UNDEAD_GHOST_COST:

                        ghost = UndeadGhost(feasible_spawnpoint, unit.get_group(), unit.get_team(), False)
                        self.create_new_unit(ghost)
                        self.map_model.spend(Constants.UNDEAD_GHOST_COST, unit.get_team())



    # CHECK_WIN_CONDITIONS
    # The teams who lefts with no more units loses
    def check_win_conditions(self):

        teams = self.map_model.get_team_units()

        if teams[1].get_unit_array() == [] or self.map_model.all_heroes_in_team_dead(1):
            self.map_view.print_winner_team(2)
            self.finished = True

        elif teams[2].get_unit_array() == [] or self.map_model.all_heroes_in_team_dead(2):
            self.map_view.print_winner_team(1)
            self.finished = True
        


    # MANAGE_SELECTED_TILE
    # Select a spawnpoint tile for player recruiting units
    def manage_selected_tile(self):

        mouse_pixel_position = self.map_model.closest_hexagon(pygame.mouse.get_pos())
        mouse_position = self.map_model.get_position_by_coords(mouse_pixel_position)

        if mouse_position != None:

            if not self.map_model.occupied(mouse_position) and self.map_model.get_tile_dictionary()[mouse_position].get_terrain_id() == Constants.SPAWNPOINT:

                if self.map_model.get_selected_tile() != None:

                    if self.map_model.get_selected_tile().get_position() == mouse_position:

                        self.map_model.set_selected_tile(None)

                    else:
                        
                        self.map_model.selected_tile = NodeBase(mouse_position, mouse_pixel_position, Constants.SPAWNPOINT)

                else:

                    self.map_model.selected_tile = NodeBase(mouse_position, mouse_pixel_position, Constants.SPAWNPOINT)

            else:

                self.map_model.set_selected_tile(None)



    # PRINT_SELECTED_TILE
    # Prints with yellow the selected tile
    def print_selected_tile(self):

        if self.map_model.get_selected_tile() != None:

            self.map_view.print_selected_tile(self.map_model.get_selected_tile())



    # SAVEGAME
    # Saves an instance of the actual map to txt
    def savegame(self):

        if Constants.SAVEGAMES:

            savegame_name = "savegame" + str(self.savegame_number)
            self.map_model.save_map(savegame_name)
            self.savegame_number = self.savegame_number + 1



    # PRINT_TERRAIN_BONUS
    # Prints in the hexagon where the mouse is the terrain bonus for the selected unit
    def print_terrain_bonus(self):

        selected_unit = self.map_model.get_selected_unit()  
        mouse_pixel_position = self.map_model.closest_hexagon(pygame.mouse.get_pos())
        mouse_position = self.map_model.get_position_by_coords(mouse_pixel_position)
        map_nodebase = self.map_model.get_tile_dictionary()

        if mouse_position in self.map_model.get_tile_dictionary().keys() and selected_unit != None:
        
            terrain_bonus = selected_unit.get_terrain_bonus(map_nodebase[mouse_position].get_terrain_id())

            if not self.map_model.occupied(mouse_position):

                if terrain_bonus < 40.0:

                    self.map_view.print_terrain_bonus(mouse_pixel_position, terrain_bonus, Constants.RED)

                elif terrain_bonus < 60.0:

                    self.map_view.print_terrain_bonus(mouse_pixel_position, terrain_bonus, Constants.GOLD)

                else:

                    self.map_view.print_terrain_bonus(mouse_pixel_position, terrain_bonus, Constants.GREEN)



    # UPDATE_MAP
    # Update of the map status
    def update_map(self):

        # Draw map tiles
        self.map_view.draw_map(self.map_model.get_tile_dictionary())
        self.map_view.print_money(self.map_model.get_money(1))
        self.map_view.print_money(self.map_model.get_money(2), (505, 38))

        # Checks new button
        if self.map_view.new_button_pushed():

            if self.map_model.get_money() >= 20 and self.map_model.get_selected_tile() != None:

                self.create_new_unit(HumanWarrior(self.map_model.selected_tile))
                self.map_model.spend(Constants.HUMAN_WARRIOR_COST, self.map_model.get_playing_team())

            self.map_model.set_selected_tile(None)
            self.map_model.set_selected_unit(None)

        # Checks exit button
        if self.map_view.exit_button_pushed():
            return 0
        
        if self.map_view.end_turn_button_pushed():

            self.turn = 2

        # Print all units
        self.map_view.print_units(self.map_model.get_team_units(), self.map_model.get_tile_dictionary())

        self.check_win_conditions()

        if not self.finished:

            if self.turn == 1:
            
                # Prints selected unit and its movement tiles
                self.print_selected_unit()
                self.print_selected_tile()

                # Draw an hexagon where the mouse pointer is
                self.print_mouse_hexagon()
                self.print_terrain_bonus()

                # Gets and prints the attacking hexagons
                self.get_attack_movements()

                # If the mouse is clicked
                if self.map_view.left_mouse_button_pushed() and self.clicked == False:

                    self.clicked = True
                    # Manages and prints selected unit and tile
                    self.manage_selected_tile()
                    self.manage_selected_unit()
                    
                if self.map_model.all_units_in_team_moved(self.turn):
                    print("Turno del equipo 2")
                    self.turn = 2

                elif self.map_view.right_mouse_button_pushed() and self.clicked == False:

                    self.clicked = True
                    self.map_model.set_selected_unit(None)
                    self.map_model.set_selected_unit_movements()
                    self.map_model.set_selected_tile(None)

            else:

                for group in self.map_model.get_team_groups()[1:]:

                    for team in group:

                        if team != 1:

                            for unit in reversed(self.map_model.get_team_units()[team].get_unit_array()):

                                if not unit.get_moved():
                                    print(f"Turno de: ")
                                    unit.toString()
                                    self.AI_turn(unit)
                                    self.check_win_conditions()
                                    if self.finished:
                                        break;

                        if self.finished:
                            break;

                    if self.finished:
                        break;

                self.savegame()
                self.turn = 1
                self.map_model.restart_unit_movements()
                print("Turno del equipo 1")
            

        # Restart auxiliar variable
        if not self.map_view.left_mouse_button_pushed() and not self.map_view.right_mouse_button_pushed():
            self.clicked = False

        return 1




