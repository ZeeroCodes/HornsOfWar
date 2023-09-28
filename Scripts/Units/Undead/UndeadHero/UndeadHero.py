from Scripts.Units.Undead.Undead import Undead
from Scripts.Widgets.NodeBase import NodeBase
import random
import pygame
import os

class UndeadHero(Undead):
    def __init__(self, position = NodeBase((0,0), (50,150)), team = 1, friendly = True, max_health = random.randint(80, 100), damage = random.randrange(15,25), movement = 4, level = 1):
        super().__init__("Ghost\\undead_ghost.png", position, team, friendly, max_health, damage, movement)
        self.level = level
        self.crown_image = pygame.image.load(os.path.abspath(os.getcwd()) + '\Images\Crown.png')
        self.crown_image = pygame.transform.scale(self.crown_image, (15, 10))

    def getID(self):
        return 210 + self.level
    
    def get_crown_image(self):
        return self.crown_image




