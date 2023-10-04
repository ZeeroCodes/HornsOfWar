import pygame
import math

from pygame.locals import *
from MapEditor.Widgets.NodeBase import NodeBase
from MapEditor.Units.HumanWarrior import HumanWarrior
from MapEditor.MapModel import MapModel
from MapEditor.MapView import MapView
from MapEditor.Units.UndeadGhost import UndeadGhost

import Constants

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

    def __init__(self):
        
            
        pygame.init()
        self.map_model = MapModel()
        self.map_view = MapView()

        self.clicked = False

        self.selected_terrain = None
        self.selected_race = None
        self.selected_unit = None
        self.team = 1
        self.group = 1

        self.map_model.set_rect_view((0, 80), self.map_view.get_resolution())
  
    

    # GET_MOUSE_PIXEL_POSITION
    # Returns the real mouse pixel position after aplying the offset
    def get_mouse_pixel_position(self):

        # Gets the actual mouse pixel position
        mouse_pixel_position = pygame.mouse.get_pos()
        # Gets the rect view square
        rect_view = self.map_model.get_rect_view()
        # Applyies offset
        corrected_pixel_position = (mouse_pixel_position[0] + rect_view.left, mouse_pixel_position[1] + rect_view.top - 80)

        return corrected_pixel_position



    # GET_MOUSE_POSITION
    # Returns the real mouse position after aplyinf the offset
    def get_mouse_position(self):

        # Gets real mouse pixel position
        pixel_position = self.get_mouse_pixel_position()
        # Calculates new position
        position = self.map_model.get_position_by_coords(pixel_position)

        return position



    # PRINT_MOUSE_HEXAGON
    # Prints the mouse hexagon with the color depending on the position
    # Unit = BLUE
    # Empty = GOLD
    def print_mouse_hexagon(self, dictionary):

        mouse_pixel_position = pygame.mouse.get_pos()

        if self.is_inside(mouse_pixel_position):

            mouse_position = self.get_mouse_position()
           
            if mouse_position in dictionary.keys():
                
                hexagon_pixel_position = dictionary[mouse_position].get_pixel_position()

                if self.map_model.get_unit_in_position(mouse_position) == None:

                    self.map_view.print_mouse_hexagon(hexagon_pixel_position, GOLD)

                else:

                    self.map_view.print_mouse_hexagon(hexagon_pixel_position, BLUE)



    # IS_INSIDE
    # Returns true if the position is inside the boundings of the map
    def is_inside(self, pixel_position):

        resolution = self.map_view.get_resolution()

        if pixel_position[0] > 0 and pixel_position[0] < resolution[0] and pixel_position[1] > 80 and pixel_position[1] < resolution[1]:

            return True

        return False

    

    # MANAGE_TERRAIN_BUTTONS
    # Sets the selected terrain depending on the pushed button
    def manage_terrain_buttons(self):

        # Checks grass button
        if self.map_view.grass_button_pushed():

            self.selected_race = None
            self.selected_unit = None
            self.selected_terrain = Constants.GRASS_TERRAIN

        # Checks forest button
        elif self.map_view.forest_button_pushed():

            self.selected_race = None
            self.selected_unit = None
            self.selected_terrain = Constants.FOREST_TERRAIN

        # Checks hills button
        elif self.map_view.hills_button_pushed():

            self.selected_race = None
            self.selected_unit = None
            self.selected_terrain = Constants.HILLS_TERRAIN

        # Checks water button
        elif self.map_view.water_button_pushed():

            self.selected_race = None
            self.selected_unit = None
            self.selected_terrain = Constants.WATER_TERRAIN

        # Checks mountains button
        elif self.map_view.mountains_button_pushed():

            self.selected_race = None
            self.selected_unit = None
            self.selected_terrain = Constants.MOUNTAIN_TERRAIN

        # Checks sand button
        elif self.map_view.sand_button_pushed():

            self.selected_race = None
            self.selected_unit = None
            self.selected_terrain = Constants.SAND_TERRAIN

        # Checks snow button
        elif self.map_view.dirt_button_pushed():

            self.selected_race = None
            self.selected_unit = None
            self.selected_terrain = Constants.DIRT_TERRAIN

        # Checks swamp button
        elif self.map_view.swamp_button_pushed():

            self.selected_race = None
            self.selected_unit = None
            self.selected_terrain = Constants.SWAMP_TERRAIN

    

    # PRINT_TERRAIN_SELECTION
    # Sets the position for the selected terrain button and prints its bounding hexagon
    def print_terrain_selection(self):

        if self.selected_terrain != None:

            selected_terrain_position = None

            if self.selected_terrain == Constants.GRASS_TERRAIN:

                selected_terrain_position = (423, 23)
                
            elif self.selected_terrain == Constants.FOREST_TERRAIN:

                selected_terrain_position = (458, 23)

            elif self.selected_terrain == Constants.HILLS_TERRAIN:

                selected_terrain_position = (458, 58)
                
            elif self.selected_terrain == Constants.WATER_TERRAIN:

                selected_terrain_position = (493, 58)
                
            elif self.selected_terrain == Constants.MOUNTAIN_TERRAIN:

                selected_terrain_position = (388, 23)
                
            elif self.selected_terrain == Constants.SAND_TERRAIN:

                selected_terrain_position = (493, 23)
                
            elif self.selected_terrain == Constants.DIRT_TERRAIN:

                selected_terrain_position = (388, 58)
                
            elif self.selected_terrain == Constants.SWAMP_TERRAIN:

                selected_terrain_position = (423, 58)

            self.map_view.draw_hexagon(selected_terrain_position, BLACK, 14, 3)



    # MANAGE_UNIT_BUTTONS
    # Selects the race and unit type depending on the psuehd buttons
    def manage_unit_buttons(self):

        # Checks human race button
        if self.map_view.human_button_pushed():

            self.selected_race = 1
            self.selected_unit = None
            self.selected_terrain = None

        # Checks undead race button
        if self.map_view.undead_button_pushed():

            self.selected_race = 2
            self.selected_unit = None
            self.selected_terrain = None
        
        if self.selected_race != None:

            # If the human race is chosen and the unit 1 button is pushed
            if self.selected_race == 1 and self.map_view.human_warrior_button_pushed():

                self.selected_unit = 1

            # If the undead race is chosen and the unit 1 button is pushed
            elif self.selected_race == 2 and self.map_view.undead_ghost_button_pushed():

                self.selected_unit = 1

 

    # PRINT_UNIT_SELECTION
    # Draws the bounding rect of the selected race and the bounding hexagon for the selected unit
    def print_unit_selection(self):

        if self.selected_race != None:

            if self.selected_race == 1:

                self.map_view.human_warrior_button.draw_button()
                self.map_view.print_rect(pygame.Rect(584, 12, 54, 23), BLACK, 4)
                
                if self.selected_unit == 1:
                    
                    self.map_view.draw_hexagon((605, 58), BLACK, 20, 4)

                else:

                    self.map_view.draw_hexagon((605, 58), BLACK, 20, 2)

            elif self.selected_race == 2:

                self.map_view.undead_ghost_button.draw_button()
                self.map_view.print_rect(pygame.Rect(644, 12, 54, 23), BLACK, 4)
                
                if self.selected_unit == 1:

                    self.map_view.draw_hexagon((605, 58), BLACK, 20, 4)

                else:

                    self.map_view.draw_hexagon((605, 58), BLACK, 20, 2)



    # MANAGE_TEAM_SELECTION
    # Manages the group and team selection for the units
    def manage_team_selection(self):

        if self.map_view.up_group_button_pushed():

            if self.group < 8:

                self.group += 1

        if self.map_view.down_group_button_pushed():

            if self.group > 1:

                self.group -= 1

        if self.map_view.up_team_button_pushed():

            if self.team < 8:

                self.team += 1

        if self.map_view.down_team_button_pushed():

            if self.team > 1:

                self.team -= 1
        
   

    # MANAGE_MAP_DIMENSIONS
    # Decreases or increases the value of the rows and cols depending on what button have been pushed
    def manage_map_dimensions(self):

        # Checks increase row button
        if self.map_view.up_row_button_pushed():
            # Increases rows
            self.map_model.set_rows(self.map_model.get_rows() + 1)

        # Checks decrease row button
        if self.map_view.down_row_button_pushed():
            # Decreases rows
            self.map_model.set_rows(self.map_model.get_rows() - 1)

        # Checks increase column button
        if self.map_view.up_column_button_pushed():
            # Increases columns
            self.map_model.set_cols(self.map_model.get_cols() + 1)

        # Checks decrease column button
        if self.map_view.down_column_button_pushed():
            # Decreases columns
            self.map_model.set_cols(self.map_model.get_cols() - 1)

    

    # MANAGE_MENU_BUTTONS
    # Checks the exit, new, load and save buttons
    def manage_menu_buttons(self):

        # Checks new button
        if self.map_view.new_button_pushed():

            self.map_model.delete_all_units()
            self.map_model.clear_all_terrains()


        # Checks exit button
        if self.map_view.exit_button_pushed():

            return 0


        # Checks load button
        if self.map_view.load_button_pushed():  

            self.map_model.set_rect_view((0, 80), self.map_view.get_resolution())
            self.map_model.load_map()

        
        # Checks save button
        if self.map_view.save_button_pushed():

            if self.map_model.all_positions_have_terrains():

                self.map_model.save_map()

        return 1



    # MANAGE_RIGHT_MOUSE_BUTTON
    # Deletes a unit if it exists at the right-clicked position
    def manage_right_mouse_button(self):

        if self.map_view.right_mouse_button_pushed() and self.clicked == False:

            unit = self.map_model.get_unit_in_position(self.get_mouse_position())

            if unit != None:

                self.map_model.delete_unit(unit)

    

    # MANAGE_TERRAIN_CREATION
    # Creates the selected terrain in the clicked location
    def manage_terrain_creation(self):

        terrain_pixel_position = self.get_mouse_pixel_position()

        # If left mouse button is pushed
        if pygame.mouse.get_pressed()[0] == 1:
            
            # If there is a terrain selected
            if self.selected_terrain != None and self.is_inside(terrain_pixel_position):
                
                terrain_position = self.get_mouse_position()

                # If the mouse position is a valid tile position
                if terrain_position:

                    self.map_model.set_tile_terrain(terrain_position, self.selected_terrain)



    # MANAGE_UNIT_CREATION
    # Creates a new unit at the clicked position
    def manage_unit_creation(self):
            
        # Get mouse position and mouse position
        unit_pixel_position = self.get_mouse_pixel_position()

        if self.is_inside(unit_pixel_position) and self.selected_unit != None and self.selected_race != None:
           
            unit_position = self.get_mouse_position()

            if unit_position:

                unit_id = str(self.selected_race) + str(self.selected_unit) + '1'
                unit = self.map_model.get_unit_by_id(unit_id)
                unit.set_nodebase(NodeBase(unit_position, unit_pixel_position))
                unit.set_group(self.group)
                unit.set_team(self.team)
                unit.set_id(unit_id)
                self.map_model.add_unit(unit)



    # MAP_CAN_SCROLL_IN_DIRECTION
    # Returns true if the map is still able to scroll in that direction
    def map_can_scroll_in_direction(self, direction):
        
        # Gets the tile at the maximum row and column and the rect view
        max_tile = self.map_model.get_maximum_tile()
        rect_view = self.map_model.get_rect_view()

        # If the max tile exists means that there are some tiles in the map
        if max_tile:

            if direction == 'UP':

                if rect_view.top > 80:

                    return True

            elif direction == 'RIGHT':

                if rect_view.right < max_tile.get_pixel_position()[0] + RADIUS:
                    
                    return True

            elif direction == 'DOWN':

                if rect_view.bottom < max_tile.get_pixel_position()[1] + RADIUS + 80:

                    return True

            elif direction == 'LEFT':

                if rect_view.left > 0:

                    return True

            else:

                return False

        return False



    # MANAGE_MAP_SCROLL
    # Manages map movement
    def manage_map_scroll(self):

        mouse_pixel_position = pygame.mouse.get_pos()
        resolution = self.map_view.get_resolution()
        movement = None
        speed = 15

        if mouse_pixel_position != None:
            
            if mouse_pixel_position[0] > resolution[0] - 25:

                if self.map_can_scroll_in_direction('RIGHT'):
                    
                    movement = (speed, 0)

            elif mouse_pixel_position[1] > resolution[1] - 25:

                if self.map_can_scroll_in_direction('DOWN'):

                    movement = (0, speed)

            elif mouse_pixel_position[0] < 25:

                if self.map_can_scroll_in_direction('LEFT'):
                    
                    movement = (-speed, 0)

            elif mouse_pixel_position[1] < 25:

                if self.map_can_scroll_in_direction('UP'):
                    
                    movement = (0, -speed)

        if movement:

            self.map_model.map_scroll(movement)
            

            
    # UPDATE_MAP
    # Update of the map status
    def update_map(self):

        # Checks if the mouse is near the limits of the screen and moves the map accordingly
        self.manage_map_scroll()


        # Draw map tiles
        draw_dictionary = self.map_model.get_painting_dictionary()
        self.map_view.draw_map(draw_dictionary)   

        
        # Prints mouse hexagon
        self.print_mouse_hexagon(draw_dictionary)


        # Prints units in its tiles
        self.map_view.print_units(self.map_model.get_painting_units(draw_dictionary))


        # Prints the menu background, lines and separations
        self.map_view.print_menu()


        # Prints all buttons on the menu
        self.map_view.print_buttons()
        

        # If the mouse is pushed
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:

            self.clicked = True

            # Checks if exit, new, load, save buttons ahve been pushed
            if self.manage_menu_buttons() == 0:

                return 0
            
            # Checks if the decreasing/increasing row/column buttons have been pushed
            self.manage_map_dimensions()

            # Checks if any of the terrain buttons have been pushed
            self.manage_terrain_buttons()

            # Checks if the increasing/decreasing group/team buttons have been pushed
            self.manage_team_selection()

            # Checks what race and unit buttons have been pushed
            self.manage_unit_buttons()

            # Creates a unit in a position if there is any selected 
            self.manage_unit_creation()
        
        # Creates terrain sprites at the pushed location
        self.manage_terrain_creation()

        # Print the bounding hexagon for the selected terrain
        self.print_terrain_selection()

        # Checks if the right mouse button have been pushed on a unit to delete it
        self.manage_right_mouse_button()
        
        # Prints the number of the team and the group of the unit
        self.map_view.print_group_number(self.group)
        self.map_view.print_team_number(self.team)

        # Prints the rect and hexagon on the desired race and unit
        self.print_unit_selection()

        # Prints the number of rows and columns the map has
        self.map_view.print_map_dimensions(self.map_model.get_rows(), self.map_model.get_cols())


        # Restart auxiliar variable
        if not self.map_view.left_mouse_button_pushed() and not self.map_view.right_mouse_button_pushed():
            self.clicked = False

        return 1




