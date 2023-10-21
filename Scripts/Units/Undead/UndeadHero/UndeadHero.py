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
                   Constants.SWAMP_TERRAIN:     60.0,
                   Constants.STRUCTURE_TERRAIN: 80.0}

class UndeadHero(Undead):
    def __init__(self, position = NodeBase((0,0), (50,150)), group = 1, team = 1, friendly = True, max_health = None, damage = None, movement = 4, level = 1):
        
        self.max_health = max_health
        self.damage = damage

        if max_health == None:

            self.max_health = random.randint(Constants.MIN_UNDEAD_HERO_MAX_HEALTH, Constants.MIN_UNDEAD_HERO_MAX_HEALTH)

        if damage == None:
        
            self.damage = random.randrange(Constants.MIN_UNDEAD_HERO_DAMAGE, Constants.MAX_UNDEAD_HERO_DAMAGE)
        
        super().__init__("Ghost\\undead_ghost.png", position, group, team, friendly, max_health, damage, movement, terrain_bonuses)
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




