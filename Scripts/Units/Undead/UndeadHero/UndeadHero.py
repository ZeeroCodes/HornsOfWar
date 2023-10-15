from Scripts.Units.Undead.Undead import Undead
from Scripts.Widgets.NodeBase import NodeBase
import random
import pygame
import os
import Constants

random.seed()

terrain_bonuses = {Constants.GRASS_TERRAIN:     60.0,
                   Constants.FOREST_TERRAIN:    50.0,
                   Constants.HILLS_TERRAIN:     50.0,
                   Constants.WATER_TERRAIN:     60.0,
                   Constants.MOUNTAIN_TERRAIN:  50.0,
                   Constants.SAND_TERRAIN:      60.0,
                   Constants.DIRT_TERRAIN:      60.0,
                   Constants.SWAMP_TERRAIN:     60.0}

class UndeadHero(Undead):
    def __init__(self, position = NodeBase((0,0), (50,150)), group = 1, team = 1, friendly = True, max_health = random.randint(80, 100), damage = random.randrange(15,25), movement = 4, level = 1):
        super().__init__("Ghost\\undead_ghost.png", position, group, team, friendly, max_health, damage, movement)
        self.level = level
        self.crown_image = pygame.image.load(os.path.abspath(os.getcwd()) + '\Images\Crown.png')
        self.crown_image = pygame.transform.scale(self.crown_image, (15, 10))
        super().set_id("210")

    def getID(self):
        return 210 + self.level
    
    def get_crown_image(self):
        return self.crown_image
    
    def set_crown_image(self, image = None):
        self.crown_image = image



