from Scripts.Units.Humans.Human import Human
from Scripts.Widgets.NodeBase import NodeBase
import random
import pygame
import os

class HumanHero(Human):
    def __init__(self, position = NodeBase((0,0), (50,150)), team = 1 ,friendly = True, max_health = random.randint(100, 150), damage = random.randrange(25,40), movement = 3, level = 1):
        super().__init__("Warrior\\human_warrior.png", position, team, friendly, max_health, damage, movement)
        self.level = level
        self.crown_image = pygame.image.load(os.path.abspath(os.getcwd()) + '\Images\Crown.png')
        self.crown_image = pygame.transform.scale(self.crown_image, (15, 10))

    def getID(self):
        return 110 + self.level
    
    def get_crown_image(self):
        return self.crown_image




