import pygame
import math
import os
import time

from pygame.locals import *
from MapEditor.Widgets.Button import Button

RADIUS = 50

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)
YELLOW = pygame.Color(255, 255, 0)
GREY = pygame.Color(80, 80, 80)
GOLD = pygame.Color(204, 204, 0)


class MapView(object):
    def __init__(self):

        pygame.init()

        self.resolution = (1366, 768)
        #self.resolution = (800,600)

        self.screen_resolution = self.resolution

        # Parameters of pop-up screen
        self.pop_screen_width = 400
        self.pop_screen_height = 400

        self.initial_rect_coordinates = (int(self.resolution[0]/2)-int(self.pop_screen_width/2), int(self.resolution[1]/2)-int(self.pop_screen_height/2))

        self.pop_screen_rect1 = pygame.Rect(self.initial_rect_coordinates[0], self.initial_rect_coordinates[1], self.pop_screen_width, self.pop_screen_height)
        self.pop_screen_rect2 = pygame.Rect(self.initial_rect_coordinates[0]+5, self.initial_rect_coordinates[1]+5, self.pop_screen_width-10, self.pop_screen_height-10)

        # Creation of the screen display
        self.screen = pygame.display.set_mode(self.screen_resolution) # Resolution

        # Load terrain images
        self.mountain_tile = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Terrain\\Mountains.png").convert_alpha()
        self.mountain_tile = pygame.transform.scale(self.mountain_tile, (RADIUS*2, RADIUS*2))
        self.grass_tile = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Terrain\\Grass.png").convert_alpha()
        self.grass_tile = pygame.transform.scale(self.grass_tile, (RADIUS*2, RADIUS*2))
        self.forest_tile = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Terrain\\Forest.png").convert_alpha()
        self.forest_tile = pygame.transform.scale(self.forest_tile, (RADIUS*2, RADIUS*2))
        self.sand_tile = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Terrain\\Sand.png").convert_alpha()
        self.sand_tile = pygame.transform.scale(self.sand_tile, (RADIUS*2, RADIUS*2))
        self.dirt_tile = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Terrain\\Dirt.png").convert_alpha()
        self.dirt_tile = pygame.transform.scale(self.dirt_tile, (RADIUS*2, RADIUS*2))
        self.swamp_tile = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Terrain\\Swamp.png").convert_alpha()
        self.swamp_tile = pygame.transform.scale(self.swamp_tile, (RADIUS*2, RADIUS*2))
        self.hills_tile = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Terrain\\Hills.png").convert_alpha()
        self.hills_tile = pygame.transform.scale(self.hills_tile, (RADIUS*2, RADIUS*2))
        self.water_tile = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Terrain\\Water.png").convert_alpha()
        self.water_tile = pygame.transform.scale(self.water_tile, (RADIUS*2, RADIUS*2))

        # Load money dolar sign image
        self.money_image = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Money.png").convert_alpha()
        self.money_image = pygame.transform.scale(self.money_image, (75,75))

        # Creation of the exit button
        self.exit_button = Button((10, 10), self.screen, "exit_button.png", "exit_button_pressed.png")

        # (self.initial_rect_coordinates[0] + 15, self.initial_rect_coordinates[1] + 15)
        # Creation of the load screen exit button
        self.load_screen_exit_button = Button((self.initial_rect_coordinates[0] + 15, self.initial_rect_coordinates[1] + 15), self.screen, "exit_button.png", "exit_button_pressed.png", (60,40))

        # Creation of the new unit button
        self.new_button = Button((100, 10), self.screen, "new_button.png", "new_button_pressed.png")

        # Creation of the load button
        self.load_button = Button((195, 16), self.screen, "load_button.png", "load_button.png", (60,20))

        # Creation of the load button
        self.save_button = Button((190, 40), self.screen, "save_button.png", "save_button.png", (70,25))

        # Load increase-decrease row-column buttons
        self.up_row_button = Button((325, 10), self.screen, "up_arrow.png", "up_arrow.png", (10,10))
        self.down_row_button = Button((325, 25), self.screen, "down_arrow.png", "down_arrow.png", (10,10))
        self.up_column_button = Button((325, 45), self.screen, "up_arrow.png", "up_arrow.png", (10,10))
        self.down_column_button = Button((325, 60), self.screen, "down_arrow.png", "down_arrow.png", (10,10))

        # Load increase-decrease group and team buttons
        self.up_group_button = Button((540, 10), self.screen, "up_arrow.png", "up_arrow.png", (10,10))
        self.down_group_button = Button((540, 25), self.screen, "down_arrow.png", "down_arrow.png", (10,10))
        self.up_team_button = Button((540, 45), self.screen, "up_arrow.png", "up_arrow.png", (10,10))
        self.down_team_button = Button((540, 60), self.screen, "down_arrow.png", "down_arrow.png", (10,10))

        # Load terrain buttons
        self.grass_button = Button((410, 10), self.screen, "Grass.png", "Grass.png", (26,26))
        self.forest_button = Button((445, 10), self.screen, "Forest.png", "Forest.png", (26,26))
        self.hills_button = Button((445, 45), self.screen, "Hills.png", "Hills.png", (26,26))
        self.water_button = Button((480, 45), self.screen, "Water.png", "Water.png", (26,26))
        self.mountains_button = Button((375, 10), self.screen, "Mountains.png", "Mountains.png", (26,26))
        self.sand_button = Button((480, 10), self.screen, "Sand.png", "Sand.png", (26,26))
        self.dirt_button = Button((375, 45), self.screen, "Dirt.png", "Dirt.png", (26,26))
        self.swamp_button = Button((410, 45), self.screen, "Swamp.png", "Swamp.png", (26,26))
        
        # Create units race button
        self.human_button = Button((580, 1), self.screen, "human_button.png", "human_button.png", (60,45))
        self.undead_button = Button((640, 1), self.screen, "undead_button.png", "undead_button.png", (60,45))

        # Create human buttons
        self.human_warrior_button = Button((590, 45), self.screen, "human_warrior.png", "human_warrior.png", (30,25))

        # Create undead buttons
        self.undead_ghost_button = Button((590, 45), self.screen, "undead_ghost.png", "undead_ghost.png", (30,25))

        # Font creation
        self.font = pygame.font.SysFont(None, 16)
        self.winning_font = pygame.font.SysFont(None, 96)

    

    # PRINT_POSITION
    # Prints the position of the tile on the screen
    def print_position(self, tile):

        pixel_position = tile.get_pixel_position()
        pixel_position = (pixel_position[0], pixel_position[1] - 35)
        tile = tile.get_position()
        tile = (tile[0]+1, tile[1]+1)
       
        img = self.font.render(str(tile), False, BLACK)
        self.screen.blit(img, pixel_position)



    # SET_RESOLUTION
    def set_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution



    # GET_RESOLUTION
    def get_resolution(self):
        return self.screen_resolution



    # DRAW_HEXAGON
    # Draws one hexagon having the center and the radius
    def draw_hexagon(self, center, colour = BLACK, radius = RADIUS, thick = 5):
        points = [(center[0] + radius, center[1]),
                 (center[0] + int(radius*math.cos(math.pi/3)), center[1] + int(radius*math.sin(math.pi/3))),
                 (center[0] - int(radius*math.cos(math.pi/3)), center[1] + int(radius*math.sin(math.pi/3))),
                 (center[0] - radius, center[1]),
                 (center[0] - int(radius*math.cos(math.pi/3)), center[1] - int(radius*math.sin(math.pi/3))),
                 (center[0] + int(radius*math.cos(math.pi/3)), center[1] - int(radius*math.sin(math.pi/3)))]
        pygame.draw.polygon(self.screen, colour, points, thick)



    # PAINT_HEXAGON
    # Draws one hexagon at the desired center and fills it with the color passed by argument
    def paint_hexagon(self, center, colour = WHITE, radius = RADIUS):
        centero = (RADIUS, RADIUS)
        points = [(centero[0] + radius, centero[1]),
                 (centero[0] + int(radius*math.cos(math.pi/3)), centero[1] + int(radius*math.sin(math.pi/3))),
                 (centero[0] - int(radius*math.cos(math.pi/3)), centero[1] + int(radius*math.sin(math.pi/3))),
                 (centero[0] - radius, centero[1]),
                 (centero[0] - int(radius*math.cos(math.pi/3)), centero[1] - int(radius*math.sin(math.pi/3))),
                 (centero[0] + int(radius*math.cos(math.pi/3)), centero[1] - int(radius*math.sin(math.pi/3)))]
        hex_surface = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
        pygame.draw.polygon(hex_surface, colour, points)
        self.screen.blit(hex_surface, (center[0]-RADIUS, center[1]-RADIUS))



    # LOAD_TERRAIN
    # Paints the terrain on the tile on the map
    def load_terrain(self, nodebase):
        terrain = nodebase.get_terrain()
        center = nodebase.get_pixel_position()

        if terrain != None:

            if terrain == 0:

                self.screen.blit(self.grass_tile, (center[0] - RADIUS, center[1] - RADIUS + 5))
                
            elif terrain == 1:

                self.screen.blit(self.forest_tile, (center[0] - RADIUS, center[1] - RADIUS + 5))

            elif terrain == 2:

                self.screen.blit(self.hills_tile, (center[0] - RADIUS, center[1] - RADIUS + 5))
                
            elif terrain == 3:

                self.screen.blit(self.water_tile, (center[0] - RADIUS, center[1] - RADIUS + 5))
                
            elif terrain == 4:

                self.screen.blit(self.mountain_tile, (center[0] - RADIUS, center[1] - RADIUS + 5))
                
            elif terrain == 5:

                self.screen.blit(self.sand_tile, (center[0] - RADIUS, center[1] - RADIUS + 5))
                
            elif terrain == 6:

                self.screen.blit(self.dirt_tile, (center[0] - RADIUS, center[1] - RADIUS + 5))
                
            elif terrain == 7:

                self.screen.blit(self.swamp_tile, (center[0] - RADIUS, center[1] - RADIUS + 5))



    # UP_ROW_BUTTON_PUSHED
    def up_row_button_pushed(self):
        if self.up_row_button.is_pushed():
            return True
        return False



    # DOWN_ROW_BUTTON_PUSHED
    def down_row_button_pushed(self):
        if self.down_row_button.is_pushed():
            return True
        return False



    # UP_COLUMN_BUTTON_PUSHED
    def up_column_button_pushed(self):
        if self.up_column_button.is_pushed():
            return True
        return False



    # DOWN_COLUMN_BUTTON_PUSHED
    def down_column_button_pushed(self):
        if self.down_column_button.is_pushed():
            return True
        return False



    # NEW_BUTTON_PUSHED
    def new_button_pushed(self):
        if self.new_button.is_pushed():
            return True
        return False



    # LOAD_BUTTON_PUSHED
    def load_button_pushed(self):
        if self.load_button.is_pushed():
            return True
        return False



    # LOAD_BUTTON_PUSHED
    def load_screen_exit_button_pushed(self):
        if self.load_screen_exit_button.is_pushed():
            return True
        return False



    # SAVE_BUTTON_PUSHED
    def save_button_pushed(self):
        if self.save_button.is_pushed():
            return True
        return False



    # EXIT_BUTTON_PUSHED
    def exit_button_pushed(self):
        if self.exit_button.is_pushed():
            return True
        return False



    # GRASS_BUTTON_PUSHED
    def grass_button_pushed(self):
        if self.grass_button.is_pushed():
            return True
        return False



    # FOREST_BUTTON_PUSHED
    def forest_button_pushed(self):
        if self.forest_button.is_pushed():
            return True
        return False



    # HILLS_BUTTON_PUSHED
    def hills_button_pushed(self):
        if self.hills_button.is_pushed():
            return True
        return False



    # WATER_BUTTON_PUSHED
    def water_button_pushed(self):
        if self.water_button.is_pushed():
            return True
        return False



    # MOUNTAINS_BUTTON_PUSHED
    def mountains_button_pushed(self):
        if self.mountains_button.is_pushed():
            return True
        return False



    # SAND_BUTTON_PUSHED
    def sand_button_pushed(self):
        if self.sand_button.is_pushed():
            return True
        return False



    # DIRT_BUTTON_PUSHED
    def dirt_button_pushed(self):
        if self.dirt_button.is_pushed():
            return True
        return False



    # SWAMP_BUTTON_PUSHED
    def swamp_button_pushed(self):
        if self.swamp_button.is_pushed():
            return True
        return False



    # PRINT_GROUP_NUMBER
    def print_group_number(self, group):
        img = self.font.render(str(group), False, BLACK)
        pixel_position = (560, 17)
        self.screen.blit(img, pixel_position)



    # PRINT_TEAM_NUMBER
    def print_team_number(self, team):
        img = self.font.render(str(team), False, BLACK)
        pixel_position = (560, 52)
        self.screen.blit(img, pixel_position)



    # UP_TEAM_BUTTON_PUSHED
    def up_team_button_pushed(self):
        if self.up_team_button.is_pushed():
            return True
        return False



    # DOWN_TEAM_BUTTON_PUSHED
    def down_team_button_pushed(self):
        if self.down_team_button.is_pushed():
            return True
        return False



    # UP_GROUP_BUTTON_PUSHED
    def up_group_button_pushed(self):
        if self.up_group_button.is_pushed():
            return True
        return False


    # DOWN_GROUP_BUTTON_PUSHED
    def down_group_button_pushed(self):
        if self.down_group_button.is_pushed():
            return True
        return False



    # HUMAN_BUTTON_PUSHED
    def human_button_pushed(self):
        if self.human_button.is_pushed():
            return True
        return False



    # GET_HUMAN_BUTTON_RECT
    def get_human_button_rect(self):
        return self.human_button.get_rect()



    # UNDEAD_BUTTON_PUSHED
    def undead_button_pushed(self):
        if self.undead_button.is_pushed():
            return True
        return False



    # GET_UNDEAD_BUTTON_RECT
    def get_undead_button_rect(self):
        return self.undead_button.get_rect()



    # GET_UNDEAD_BUTTON_RECT
    def undead_ghost_button_pushed(self):
        return self.undead_ghost_button.is_pushed()



    # GET_UNDEAD_BUTTON_RECT
    def human_warrior_button_pushed(self):
        return self.human_warrior_button.is_pushed()



    # LEFT_MOUSE_BUTTON_PUSHED
    # Returns true if the left mouse button is pushed
    def left_mouse_button_pushed(self):
        if pygame.mouse.get_pressed()[0]:
            return True
        return False



    # RIGHT_MOUSE_BUTTON_PUSHED
    # Returns true if the right mouse button is pushed
    def right_mouse_button_pushed(self):
        if pygame.mouse.get_pressed()[2]:
            return True
        return False



    # PRINT_MONEY
    # Prints the available money for the player
    def print_money(self, money):
        self.screen.blit(self.money_image, (170, 25))

        img = self.font.render(str(money), False, BLACK)
        pixel_position = (205, 38)
        self.screen.blit(img, pixel_position)



    # PRINT_UNIT
    # Prints one unit in the map
    def print_unit(self, unit):
        #center_pos = tile_dictionary[unit.get_position()].get_pixel_position()
        center_pos = unit.get_pixel_position()
        max_health = unit.get_max_health()
        health = unit.get_health()
        life = int((health*40)/max_health)
        image = unit.get_image().convert_alpha()

        if unit.get_moved():
            self.paint_hexagon(unit.get_pixel_position(), pygame.Color(255, 0, 0, 80))

        self.screen.blit(image, (center_pos[0]-image.get_width()/2, center_pos[1]-image.get_height()/2)) # Draws button
        pygame.draw.rect(self.screen, GREY, pygame.Rect(center_pos[0] + 20, center_pos[1]-21, 5, 42))
        

        # If life is full pint green bar
        if life == 40:

            pygame.draw.rect(self.screen, GREEN, pygame.Rect(center_pos[0] + 21, center_pos[1]-20, 3, 40))

        # If life is more than half bar
        elif life >= 20:

            # When life is above 25 of 40, print the bar with GREEN
            if life > 25:

                pygame.draw.rect(self.screen, GREEN, pygame.Rect(center_pos[0] + 21, center_pos[1]-(20-(40-life)), 3, 40-(40-life)))
            
            # When life reaches 25 of 40, print the bar with yellow
            else:

                pygame.draw.rect(self.screen, YELLOW, pygame.Rect(center_pos[0] + 21, center_pos[1]-(20-(40-life)), 3, 40-(40-life)))

        else:

            # When life is above 10 over 40 print with yellow
            if life > 10:

                pygame.draw.rect(self.screen, YELLOW, pygame.Rect(center_pos[0] + 21, center_pos[1]+(20-life), 3, 40-(40-life)))
            
            # If life is over 10 of 40, print it in red
            else:

                pygame.draw.rect(self.screen, RED, pygame.Rect(center_pos[0] + 21, center_pos[1]+(20-life), 3, 40-(40-life)))



    # PRINT_UNITS
    # Prints every unit on the map
    def print_units(self, unit_dictionary):

        for unit in unit_dictionary.values():

            self.print_unit(unit)



    # PRINT_MOUSE_HEXAGON
    # Draws the hexagon where the mouse pointer is at
    def print_mouse_hexagon(self, mouse_position, color = GOLD):
        if mouse_position != None:
            self.draw_hexagon(mouse_position, color)
 
    

    # CLEAR_SCREEN
    # Paints all screen with white
    def clear_screen(self):
        self.screen.fill(WHITE)

    

    # PRINT_MAP_DIMENSIONS
    # Prints the number of rows and cols of the map
    def print_map_dimensions(self, rows, cols):

        rows_img = self.font.render(str(rows), False, BLACK)
        pixel_position = (300, 17)
        self.screen.blit(rows_img, pixel_position)

        cols_img = self.font.render(str(cols), False, BLACK)
        pixel_position = (300, 52)
        self.screen.blit(cols_img, pixel_position)



    # PRINT_LOAD_SCREEN
    # Prints map load screen
    def print_load_screen(self):
        
        pygame.draw.rect(self.screen, BLACK, self.pop_screen_rect1)
        pygame.draw.rect(self.screen, WHITE, self.pop_screen_rect2)
        #self.screen.blit()
        pygame.display.flip()



    # PRINT_RECT
    def print_rect(self, rect, colour = WHITE, thickness = 0):
        pygame.draw.rect(self.screen, colour, rect, thickness)
        #pygame.display.update()



    # PRINT_MENU
    # Prints rect and lines from the menu
    def print_menu(self):

        self.print_rect(pygame.Rect(0, 0, self.resolution[0], 80))
        pygame.draw.line(self.screen, BLACK, (0, 1), (self.screen_resolution[0], 1), 4)
        pygame.draw.line(self.screen, BLACK, (1, 0), (1, 80), 4)
        pygame.draw.line(self.screen, BLACK, (0, 80), (self.screen_resolution[0], 80), 4)
        pygame.draw.line(self.screen, BLACK, (275, 0), (275, 80), 4)
        pygame.draw.line(self.screen, BLACK, (350, 0), (350, 80), 4)
        pygame.draw.line(self.screen, BLACK, (525, 0), (525, 80), 4)
        pygame.draw.line(self.screen, BLACK, (575, 0), (575, 80), 4)


    def print_buttons(self):

        # Creation of the exit button
        self.exit_button.draw_button()

        # Creation of the new unit button
        self.new_button.draw_button()

        # Creation of the load button
        self.load_button.draw_button()

        # Creation of the load button
        self.save_button.draw_button()

        # Load increase-decrease row-column buttons
        self.up_row_button.draw_button()
        self.down_row_button.draw_button()
        self.up_column_button.draw_button()
        self.down_column_button.draw_button()

        # Load increase-decrease group and team buttons
        self.up_group_button.draw_button()
        self.down_group_button.draw_button()
        self.up_team_button.draw_button()
        self.down_team_button.draw_button()

        # Load terrain buttons
        self.grass_button.draw_button()
        self.forest_button.draw_button()
        self.hills_button.draw_button()
        self.water_button.draw_button()
        self.mountains_button.draw_button()
        self.sand_button.draw_button()
        self.dirt_button.draw_button()
        self.swamp_button.draw_button()
        
        # Create units race button
        self.human_button.draw_button()
        self.undead_button.draw_button()
        
       

    # DRAW_MAP
    # Draws the GUI part of the map
    def draw_map(self, tiles_dictionary):

        self.clear_screen() # Paints background
        
        if tiles_dictionary:

            for value in tiles_dictionary.values():
                self.load_terrain(value) # loads every tile of grass
                self.draw_hexagon(value.get_pixel_position())
                self.print_position(value)
        
        
        
        
  
        
                
        





