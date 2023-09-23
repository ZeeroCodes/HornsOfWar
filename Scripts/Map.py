import pygame

from pygame.locals import *
from NodeBase import NodeBase
from HumanWarrior import HumanWarrior
from MapModel import MapModel
from MapView import MapView

RADIUS = 50

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)
GREY = pygame.Color(80, 80, 80)
GOLD = pygame.Color(204, 204, 0)

class Map(object):

    def __init__(self, map_name = "TestMap"):

        pygame.init()
        self.map_model = MapModel()
        self.map_model.load_map(map_name)
        self.map_view = MapView()

        self.clicked = False
        self.previous_position = None
    


    # CREATE_NEW_UNIT
    # Creates new unit in friendly or enemy array
    def create_new_unit(self, unit = HumanWarrior()):
        if not self.map_model.occupied(unit.get_position()):
            self.map_model.add_unit(unit)

    
    # MANAGE_SELECTED_UNIT
    # Manages the selected unit
    def manage_selected_unit(self):

        mouse_pixel_position = self.map_model.closest_hexagon(pygame.mouse.get_pos())
        mouse_position = self.map_model.get_position_by_coords(mouse_pixel_position)

        if mouse_position != None: # If the click is inside the map

            unit_in_position = self.map_model.get_unit_in_position(mouse_position)

            if self.map_model.get_selected_unit() == None:  

                if self.map_model.is_friendly(unit_in_position):

                    self.map_model.set_selected_unit(unit_in_position)

            else:

                if self.map_model.occupied(mouse_position):

                    if unit_in_position == self.map_model.get_selected_unit():

                        self.map_model.set_selected_unit(None)

                    elif self.map_model.is_friendly(unit_in_position):

                        self.map_model.set_selected_unit(unit_in_position)
                        self.previous_position = None

                    else:

                        self.map_model.set_selected_unit(None)
                        self.map_model.clear_selected_unit_movements()

                else: # If the position clicked is empty, move the selected unit to that position

                    if self.map_model.reachable(mouse_position):

                        self.map_model.modify_unit_position(self.map_model.get_selected_unit(), mouse_position)
                        self.map_model.set_selected_unit_position(mouse_position)
                        self.map_model.set_path()

                    self.map_model.set_selected_unit(None) 
                    self.map_model.clear_selected_unit_movements()

        else:
            self.map_model.set_selected_unit(None) 
            self.map_model.clear_selected_unit_movements()

    
    
    # PRINT_SELECTED_UNIT
    # Prints the selected units hexagon and posible movements
    def print_selected_unit(self):

        if self.map_model.get_selected_unit() != None:

            selected_unit_movements = self.map_model.get_movement_positions()

            self.map_view.print_unit_movements(selected_unit_movements)
            
            self.map_view.paint_hexagon(self.map_model.get_coords_by_position(self.map_model.get_selected_unit().get_position()), RADIUS, pygame.Color(0, 255, 0, 150))
            self.map_view.draw_hexagon(self.map_model.get_coords_by_position(self.map_model.get_selected_unit().get_position()), RADIUS, 5, BLUE) 
            mouse_pixel_position = self.map_model.closest_hexagon(pygame.mouse.get_pos())
            mouse_position = self.map_model.get_position_by_coords(mouse_pixel_position)

            if mouse_pixel_position != None and not self.map_model.occupied(mouse_position):

                if mouse_position != self.previous_position:

                    self.previous_position = mouse_position
                    nodebase1 = NodeBase(self.map_model.get_selected_unit().get_position(), self.map_model.get_coords_by_position(self.map_model.get_selected_unit().get_position()))
                    nodebase2 = NodeBase(mouse_position, mouse_pixel_position)
                    self.map_model.get_new_path(nodebase1, nodebase2)

                if self.map_model.get_path():
                    self.map_view.print_path(self.map_model.get_path())
                    


    # UPDATE_MAP
    # Update of the map status
    def update_map(self):

        # Draw map tiles
        self.map_view.draw_map(self.map_model.get_tile_dictionary())

        # Checks new button
        if self.map_view.new_button_pushed():
            self.create_new_unit(HumanWarrior())

        # Checks exit button
        if self.map_view.exit_button_pushed():
            return 0

        # Print all units
        self.map_view.print_units(self.map_model.get_friendly_units(), self.map_model.get_enemy_units(), self.map_model.get_tile_dictionary())

        # Prints selected unit and its movement tiles
        self.print_selected_unit()

        # Draw an hexagon where the mouse pointer is
        mouse_position = self.map_model.closest_hexagon(pygame.mouse.get_pos())
        self.map_view.print_mouse_hexagon(mouse_position)

        # If the mouse is clicked
        if self.map_view.left_mouse_button_pushed() and self.clicked == False:

            self.clicked = True
            # Manages and prints selected unit
            self.manage_selected_unit()

        elif self.map_view.right_mouse_button_pushed() and self.clicked == False:
            self.clicked = True
            self.map_model.set_selected_unit(None)
            self.map_model.clear_selected_unit_movements()
            

        # Restart auxiliar variable
        if not self.map_view.left_mouse_button_pushed() and not self.map_view.right_mouse_button_pushed():
            self.clicked = False

        return 1




