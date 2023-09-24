from Scripts.Widgets.NodeBase import NodeBase

import pygame
import os

class Unit():

    def __init__(self, image_path, position = NodeBase((0,0), (50,150)), team = 1, friendly = True, max_health = 100, damage = 10, movement = 2):
        
        self.max_health = max_health
        self.health = max_health
        self.damage = damage
        self.movement = movement
        self.node_position = position
        self.alive = True
        self.moved = False
        self.friendly = friendly
        self.team = team
        self.warrior_image = pygame.image.load(os.path.abspath(os.getcwd()) + image_path)
        self.warrior_image = pygame.transform.scale(self.warrior_image, (60, 70))
    
    def set_moved(self, moved):
        self.moved = moved

    def get_moved(self):
        return self.moved

    def set_team(self, team):
        self.team = team

    def get_team(self):
        return self.team

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
        return self.node_position.get_position()

    def get_nodebase(self):
        return self.node_position

    def get_pixel_position(self):
        return self.node_position.get_pixel_position()

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

    def set_position(self, nodebase):
        self.node_position.set_position(nodebase.get_position())
        self.node_position.set_pixel_position(nodebase.get_pixel_position())

    def toString(self):
        print("Unit in team: " + str(self.team) + " on tile: " + str(self.node_position.get_position()) + " with " + str(self.health) + " of " + str(self.max_health) + " with " + str(self.damage) + " damage")



  



