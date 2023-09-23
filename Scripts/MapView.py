import pygame
import math
import os

from pygame.locals import *
from Button import Button

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)
GREY = pygame.Color(80, 80, 80)
GOLD = pygame.Color(204, 204, 0)

RADIUS = 50

class MapView(object):
    def __init__(self):

        pygame.init()

        self.screen_resolution = (1366, 768)
        #self.screen_resolution = (800,600)

        # Creation of the screen display
        self.screen = pygame.display.set_mode(self.screen_resolution) # Resolution

        # Load grass tile
        self.grass_tile = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Terrain\\Grass.png").convert_alpha()
        self.grass_tile = pygame.transform.scale(self.grass_tile, (RADIUS*2, RADIUS*2))

        # Creation of the exit button
        self.exit_button = Button((10,10),self.screen, "exit_button.png", "exit_button_pressed.png")

        # Creation of the new unit button
        self.new_button = Button((100,10),self.screen, "new_button.png", "new_button_pressed.png")




    # SET_RESOLUTION
    def set_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution



    # GET_RESOLUTION
    def get_resolution(self):
        return self.screen_resolution



    # DRAW_HEXAGONS
    # Draws one hexagon having the center and the radius
    def draw_hexagon(self, center, radius = RADIUS, thick = 5, colour = BLACK):# BLACK
        points = [(center[0] + radius, center[1]),
                 (center[0] + int(radius*math.cos(math.pi/3)), center[1] + int(radius*math.sin(math.pi/3))),
                 (center[0] - int(radius*math.cos(math.pi/3)), center[1] + int(radius*math.sin(math.pi/3))),
                 (center[0] - radius, center[1]),
                 (center[0] - int(radius*math.cos(math.pi/3)), center[1] - int(radius*math.sin(math.pi/3))),
                 (center[0] + int(radius*math.cos(math.pi/3)), center[1] - int(radius*math.sin(math.pi/3)))]
        pygame.draw.polygon(self.screen, colour, points, thick)



    # PAINT_HEXAGON
    # Draws one hexagon at the desired center and fills it with the color passed by argument
    def paint_hexagon(self, center, radius = RADIUS, colour = WHITE):
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



    # LOAD_GRASS
    # Paints the hex grass tile on the map
    def load_grass(self, center):
        self.screen.blit(self.grass_tile, (center[0] - RADIUS, center[1] - RADIUS + 5))



    # PRINT_UNIT
    # Prints one unit in the map
    def print_unit(self, unit, center_pos):
        image = unit.get_image().convert_alpha()
        self.screen.blit(image, (center_pos[0]-image.get_width()/2, center_pos[1]-image.get_height()/2)) # Draws button
        pygame.draw.rect(self.screen, GREY, pygame.Rect(center_pos[0] + 20, center_pos[1]-21, 5, 42))
        life = int((unit.get_health()*40)/(unit.get_max_health()))
        if life == 40:
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(center_pos[0] + 21, center_pos[1]-20, 3, 40))
        elif life >= 20:
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(center_pos[0] + 21, center_pos[1]-(20-(40-life)), 3, 40-(40-life)))
        else:
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(center_pos[0] + 21, center_pos[1]+(20-(40-life)), 3, 40-(40-life)))


    
    # PRINT_UNITS
    # Prints every unit on the map
    def print_units(self, friendly_units, enemy_units, tile_dictionary):
        for unit in friendly_units.get_unit_array():
            self.print_unit(unit, tile_dictionary[unit.get_position()].get_pixel_position())
        for unit in enemy_units.get_unit_array():
            self.print_unit(unit, tile_dictionary[unit.get_position()].get_pixel_position())



    # NEW_BUTTON_PUSHED
    # Return true if new button is pushed
    def new_button_pushed(self):
        if self.new_button.is_pushed():
            return True
        return False



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



    # EXIT_BUTTON_PUSHED
    # Returns true if exit button pushed
    def exit_button_pushed(self):
        if self.exit_button.is_pushed():
            return True
        return False



    # PRINT_MOUSE_HEXAGON
    # Draws the hexagon where the mouse pointer is at
    def print_mouse_hexagon(self, mouse_position):
        if mouse_position != None:
            self.draw_hexagon(mouse_position, RADIUS, 5, GOLD)



    # PRINT_UNIT_MOVEMENTS
    # Paint an hexagon for every movement position
    def print_unit_movements(self, unit_movements):
        for tile in unit_movements:
            self.paint_hexagon(tile.get_pixel_position(), RADIUS, pygame.Color(0, 255, 0, 80))
            self.draw_hexagon(tile.get_pixel_position(), RADIUS, 5)
        

    
    # PRINT_PATH
    # Draws lines between path positions
    def print_path(self, path):
        nodebase1 = path[0]
        for tile in path:
            pygame.draw.line(self.screen, GOLD, nodebase1.get_pixel_position(), tile.get_pixel_position(), 4)
            nodebase1 = tile



    # DRAW_MAP
    # Draws the GUI part of the map
    def draw_map(self, tiles_dictionary):

        self.screen.fill(WHITE) # Paints background

        for value in tiles_dictionary.values():
            self.load_grass(value.get_pixel_position()) # Loads every tile of grass
            self.draw_hexagon(value.get_pixel_position())
            
        # Height of the hexagon

        # print selected unit hexagon and movement tiles       
        
                
        





