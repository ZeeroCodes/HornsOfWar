import pygame
import math
import os
import time

from pygame.locals import *
from Scripts.Widgets.Button import Button
from Scripts.Units.Humans.HumanHero.HumanHero import HumanHero
from Scripts.Units.Undead.UndeadHero.UndeadHero import UndeadHero

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

        #self.screen_resolution = (1920, 1080)
        self.screen_resolution = (1366, 768)
        #self.screen_resolution = (800,600)

        # Creation of the screen display
        self.screen = pygame.display.set_mode(self.screen_resolution) # Resolution

        # Load grass tile
        self.grass_tile = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Terrain\\Grass.png").convert_alpha()
        self.grass_tile = pygame.transform.scale(self.grass_tile, (RADIUS*2, RADIUS*2))

        # Load dirt tile
        self.dirt_tile = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Terrain\\old_dirt.png").convert_alpha()
        self.dirt_tile = pygame.transform.scale(self.dirt_tile, (RADIUS*2, RADIUS*2))

        # Load structure tile
        self.structure_tile = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Structure\\Fortification.png").convert_alpha()
        self.structure_tile = pygame.transform.scale(self.structure_tile, (RADIUS*2, RADIUS*2))

        self.money_image = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\HexTileset\\Money.png").convert_alpha()
        self.money_image = pygame.transform.scale(self.money_image, (75,75))

        # Creation of the exit button
        self.exit_button = Button((10,10),self.screen, "exit_button.png", "exit_button_pressed.png")

        # Creation of the new unit button
        self.new_button = Button((100,10),self.screen, "new_button.png", "new_button_pressed.png")

        self.font = pygame.font.SysFont(None, 16)
        self.winning_font = pygame.font.SysFont(None, 96)

    

    def print_position(self, tile):
       
        img = self.font.render(str(tile.get_position()), False, BLACK)
        pixel_position = tile.get_pixel_position()
        pixel_position = (pixel_position[0], pixel_position[1] - 35)
        self.screen.blit(img, pixel_position)


    def print_winner_team(self, team):

        img = self.font.render("Wins team " + str(team), False, BLACK)
        pixel_position = (300, 25)
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



    # LOAD_GRASS
    # Paints the hex grass tile on the map
    def load_grass(self, center):
        self.screen.blit(self.grass_tile, (center[0] - RADIUS, center[1] - RADIUS + 5))


    # LOAD_DIRT
    # Paints the hex dirt tile on the map
    def load_dirt(self, center):
        self.screen.blit(self.dirt_tile, (center[0] - RADIUS, center[1] - RADIUS + 5))


    # LOAD_structure
    # Paints the hex structure tile on the map
    def load_structure(self, center):
        self.screen.blit(self.structure_tile, (center[0] - RADIUS, center[1] - RADIUS + 5))

  
    def print_money(self, money):
        self.screen.blit(self.money_image, (170, 25))

        img = self.font.render(str(money), False, BLACK)
        pixel_position = (205, 38)
        self.screen.blit(img, pixel_position)


    # PRINT_UNIT
    # Prints one unit in the map
    def print_unit(self, unit, tile_dictionary):
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

        if isinstance(unit, HumanHero) or isinstance(unit, UndeadHero):
            crown_image = unit.get_crown_image()
            self.screen.blit(crown_image, (center_pos[0] + 15, center_pos[1]-35))

    # PRINT_UNITS
    # Prints every unit on the map
    def print_units(self, team_units, tile_dictionary):

        for team in team_units[1:]:

            for unit in team.get_unit_array():

                self.print_unit(unit, tile_dictionary)



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
    def print_mouse_hexagon(self, mouse_position, color = GOLD):
        if mouse_position != None:
            self.draw_hexagon(mouse_position, color)



    # PRINT_UNIT_MOVEMENTS
    # Paint an hexagon for every movement position
    def print_unit_movements(self, unit_movements):
        for tile in unit_movements:
            self.paint_hexagon(tile.get_pixel_position(), pygame.Color(0, 255, 0, 80))
            self.draw_hexagon(tile.get_pixel_position())
        

    
    # PRINT_PATH
    # Draws lines between path positions
    def print_path(self, path, colour = GOLD):
        nodebase1 = path[0]
        for tile in path[1:]: 
            pygame.draw.line(self.screen, colour, nodebase1.get_pixel_position(), tile.get_pixel_position(), 4)
            nodebase1 = tile

    

    # CLEAR_SCREEN
    # Paints all screen with white
    def clear_screen(self):
        self.screen.fill(WHITE)



    # DRAW_MAP
    # Draws the GUI part of the map
    def draw_map(self, tiles_dictionary):

        self.clear_screen() # Paints background

        for value in tiles_dictionary.values():
            if value.get_terrain_id() == 1:
                self.load_grass(value.get_pixel_position()) # Loads every tile of 
            elif value.get_terrain_id() == 2:
                self.load_dirt(value.get_pixel_position())
            elif value.get_terrain_id() == 3:
                self.load_dirt(value.get_pixel_position())
                self.load_structure((value.get_pixel_position()))
            self.draw_hexagon(value.get_pixel_position())
            self.print_position(value)
  
        
                
        





