import pygame
import os

class Unit():

    def __init__(self, image_path, position = (0,0), max_health = 100, damage = 10, movement = 2, friendly = True):
        
        self.max_health = max_health
        self.health = max_health
        self.damage = damage
        self.movement = movement
        self.position = position
        self.alive = True
        self.friendly = friendly
        self.warrior_image = pygame.image.load(os.path.abspath(os.getcwd()) + image_path)
        self.warrior_image = pygame.transform.scale(self.warrior_image, (60, 70))

    def get_friendly(self):
        return self.friendly

    def set_friendly(self, friendly):
        self.friendly = friendly

    def get_image(self): 
        return self.warrior_image

    def get_alive(self):
        return self.alive

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_damage(self):
        return self.damage

    def get_movement(self):
        return self.movement

    def get_position(self):
        return self.position

    def set_damage(self, damage):
        self.damage = damage

    def set_health(self, health):
        self.health = health

    def hurt(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False

    def heal(self, life):
        if self.health + life > self.max_health:
            self.health = self.max_health
        else:
            self.health += life

    def set_movement(self, movement):
        self.movement = movement

    def set_position(self, position):
        self.position = position
  



