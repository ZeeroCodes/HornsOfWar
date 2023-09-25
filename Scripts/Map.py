import pygame
import math
import numpy as np
from pygame.locals import *

from Scripts.MapModel import MapModel
from Scripts.MapView import MapView

from Scripts.Widgets.NodeBase import NodeBase

from Scripts.Units.Humans.HumanWarrior.HumanWarrior import HumanWarrior
from Scripts.Units.Undead.UndeadGhost.UndeadGhost import UndeadGhost

RADIUS = 50

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
YELLOW = pygame.Color(255, 255, 0)
GREEN = pygame.Color(0, 255, 0)
GREY = pygame.Color(80, 80, 80)
GOLD = pygame.Color(204, 204, 0)

HEIGHT = RADIUS*math.cos(math.radians(30))

class Map(object):

    def __init__(self, map_name = "TestMap"):
        
        pygame.init()
        self.map_model = MapModel()
        self.map_model.load_map(map_name)
        self.map_view = MapView()

        self.clicked = False

        self.previous_position = None
        self.last_path_position = None
        self.last_unit_in_last_position = False

        self.movement_speed = 3 # 1 = Fast
                                # 2 = Medium
                                # 3 = Slow

        self.turn = 1
        self.finished = False

        nodebase1 = NodeBase((1,4), (350, 236))
        ghost = UndeadGhost(nodebase1, 2, False)
        self.map_model.add_unit(ghost, 2)
        nodebase2 = NodeBase((2,3), (275, 365))
        ghost2 = UndeadGhost(nodebase2, 2, False)
        self.map_model.add_unit(ghost2, 2)
        nodebase1 = NodeBase((4,1), (125, 537))
        ghost = UndeadGhost(nodebase1, 2, False)
        self.map_model.add_unit(ghost, 2)
        nodebase2 = NodeBase((4,0), (50, 494))
        ghost2 = UndeadGhost(nodebase2, 2, False)
        self.map_model.add_unit(ghost2, 2)

        nodebase1 = NodeBase((2,0), (50, 322))
        ghost = HumanWarrior(nodebase1)
        self.map_model.add_unit(ghost)
        #nodebase2 = NodeBase((4,0), (50, 494))
        #ghost2 = HumanWarrior(nodebase2)
        #self.map_model.add_unit(ghost2)
        
    

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
        horizontal = np.round(list(np.linspace(actual_pixel_position[0], final_pixel_position[0], self.movement_speed*20)))[:int((self.movement_speed*20)/2)]
        vertical = np.round(list(np.linspace(actual_pixel_position[1], final_pixel_position[1], self.movement_speed*20)))[:int((self.movement_speed*20)/2)]

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
            horizontal = np.round(list(np.linspace(actual_pixel_position[0], final_position[0], self.movement_speed*20)))
            vertical = np.round(list(np.linspace(actual_pixel_position[1], final_position[1], self.movement_speed*20)))

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
                            unit_in_position.hurt(selected_unit.get_damage())
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
                            self.print_path(movement_path)
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
            self.map_view.paint_hexagon(self.map_model.get_coords_by_position(self.map_model.get_selected_unit().get_position()), pygame.Color(0, 255, 0, 150))
            self.map_view.draw_hexagon(self.map_model.get_coords_by_position(self.map_model.get_selected_unit().get_position()), BLUE) 
            
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
                            
                        # Prints path
                        self.previous_position = mouse_position
                        path = self.map_model.get_path()
                        self.map_view.print_path(path[1:])
                        self.map_view.print_path(path[:2], RED)

      

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
                self.map_view.print_mouse_hexagon(mouse_pixel_position, BLUE)
            else:
                self.map_view.print_mouse_hexagon(mouse_pixel_position, RED)

    
    # AI_TURN
    # Manages the movement and attack of every enemy unit
    def AI_turn(self, unit):

        self.map_model.get_nearest_enemy_unit(unit)

        # Get available movements and units that the unit can attack
        available_movements = self.map_model.get_movement_positions(unit)
        available_movements.append(unit.get_nodebase())
        attacking_movements = self.map_model.get_attacking_positions(available_movements, unit)
        self.print_path(available_movements)
        movement_dictionary = dict()
        terrain = 1.0

        # For every available movement calculate its value
        for tile in available_movements:

            movement_value = int(10*terrain) - self.map_model.movements_between_positions(unit.get_nodebase(), 
                                                                                          self.map_model.get_nearest_enemy_unit(unit).get_nodebase())
            movement_dictionary[(tile.get_position(), None)] = movement_value

        # For every unit it can attack calculate its value
        for tile in attacking_movements:

            # Get the tile around the unit it can attack
            neighbour_tiles = self.map_model.get_movement_positions_from_position(tile.get_position(),1)

            attacking_tiles = list()

            # For every tile around the unit that is a coincidence with the available movements, append to the list
            for attacking_tile in neighbour_tiles:

                if self.map_model.nodebase_exists(attacking_tile, available_movements):

                    attacking_tiles.append(attacking_tile)
            
            # For every tile where it can attack a enemy unit
            for attacking_tile in attacking_tiles:

                # Get the attacked_unit
                attacked_unit = self.map_model.get_unit_in_position(tile)
                movement_value = 0

                # Calculate its value
                if attacked_unit.get_health() == attacked_unit.get_max_health():
                    movement_value = int(10*terrain) + int(unit.get_damage()*terrain - 0)
                else:
                    movement_value = int(10*terrain) + int((unit.get_damage()*terrain)*(attacked_unit.get_max_health() - (attacked_unit.get_health()/attacked_unit.get_max_health())))
                
                # Add this action to dictionary
                movement_dictionary[(attacking_tile.get_position(), tile.get_position())] = movement_value
        
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
                attacked_unit.hurt(unit.get_damage())

                # If the enemy health is under0, it is killed and it convert to team 2
                if attacked_unit.get_health() <= 0:

                    self.map_model.delete_unit(attacked_unit)
                    nodebase = attacked_unit.get_nodebase()
                    ghost = UndeadGhost(nodebase, 2, False)
                    self.create_new_unit(ghost)



    # CHECK_WIN_CONDITIONS
    # The teams who lefts with no more units loses
    def check_win_conditions(self):

        teams = self.map_model.get_team_units()

        if teams[1].get_unit_array() == []:
            self.map_view.print_winner_team(2)
            self.finished = True

        elif teams[2].get_unit_array() == []:
            self.map_view.print_winner_team(1)
            self.finished = True
        


    # UPDATE_MAP
    # Update of the map status
    def update_map(self):

        # Draw map tiles
        self.map_view.draw_map(self.map_model.get_tile_dictionary())
        #print("Testing")
        #print(self.moving)
        self.map_view.print_money(self.map_model.get_money())

        # Checks new button
        if self.map_view.new_button_pushed():
            if self.map_model.get_money() >= 20:
                self.create_new_unit(HumanWarrior(NodeBase((0, 0),(50, 150))))
                self.map_model.spend(20)

        # Checks exit button
        if self.map_view.exit_button_pushed():
            return 0

        # Print all units
        self.map_view.print_units(self.map_model.get_team_units(), self.map_model.get_tile_dictionary())

        self.check_win_conditions()

        if not self.finished:

            if self.turn == 1:
            
                # Prints selected unit and its movement tiles
                self.print_selected_unit()

                # Draw an hexagon where the mouse pointer is
                self.print_mouse_hexagon()

                # Gets and prints the attacking hexagons
                self.get_attack_movements()

                # If the mouse is clicked
                if self.map_view.left_mouse_button_pushed() and self.clicked == False:

                    self.clicked = True
                    # Manages and prints selected unit
                    self.manage_selected_unit()

                if self.map_model.all_units_in_team_moved(self.turn):
                    print("Turno del equipo 2")
                    self.turn = 2

                elif self.map_view.right_mouse_button_pushed() and self.clicked == False:

                    self.clicked = True
                    self.map_model.set_selected_unit(None)
                    self.map_model.set_selected_unit_movements()

            else:

                for group in self.map_model.get_team_groups():

                    for team in group:

                        if team != 1:

                            for unit in self.map_model.get_team_units()[team].get_unit_array():
                                print("Turno de: ")
                                unit.toString()
                                self.AI_turn(unit)
                                self.check_win_conditions()
                                if self.finished:
                                    break;

                        if self.finished:
                            break;

                    if self.finished:
                        break;

                self.turn = 1
                self.map_model.restart_unit_movements()
                print("Turno del equipo 1")
            

        # Restart auxiliar variable
        if not self.map_view.left_mouse_button_pushed() and not self.map_view.right_mouse_button_pushed():
            self.clicked = False

        return 1




