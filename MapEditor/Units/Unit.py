import string
from MapEditor.Widgets.NodeBase import NodeBase

import pygame
import os

class Unit():

    def __init__(self, image_path, position = NodeBase((0,0), (50,150)), group = 1, team = 1, max_health = 100, damage = 10, movement = 2):
        
        self.id = None
        self.max_health = max_health
        self.health = max_health
        self.damage = damage
        self.movement = movement
        self.node_position = position
        self.alive = True
        self.moved = True
        self.team = team
        self.group = group
        self.warrior_image = pygame.image.load(os.path.abspath(os.getcwd()) + image_path)
        self.warrior_image = pygame.transform.scale(self.warrior_image, (60, 70))
    


    # ID
    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id



    # MAX_HEALTH
    def set_max_health(self, max_health):
        self.max_health = max_health

        if self.health > max_health:

            self.health = max_health

    def get_max_health(self):
        return self.max_health



    # HEALTH
    def set_health(self, health):
        self.health = health

    def get_health(self):
        return self.health

    def hurt(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False

    def heal(self, life):
        if self.health + life > self.max_health:
            self.health = self.max_health
        else:
            self.health += life



    # DAMAGE
    def set_damage(self, damage):
        self.damage = damage

    def get_damage(self):
        return self.damage



    # MOVEMENT
    def set_movement(self, movement):
        self.movement = movement

    def get_movement(self):
        return self.movement



    # NODE_POSITION
    def set_nodebase(self, nodebase):
        self.node_position = nodebase

    def get_nodebase(self):
        return self.node_position

    def set_position(self, nodebase):
        self.node_position.set_position(nodebase.get_position())
        self.node_position.set_pixel_position(nodebase.get_pixel_position())

    def get_position(self):
        return self.node_position.get_position()


    def set_pixel_position(self, pixel_position):
        self.node_position.set_pixel_position(pixel_position)

    def get_pixel_position(self):
        return self.node_position.get_pixel_position()



    # ALIVE
    def set_alive(self, alive):
        self.alive = alive

    def get_alive(self):
        return self.alive



    # MOVED
    def set_moved(self, moved):
        self.moved = moved

    def get_moved(self):
        return self.moved



    # FRIENDLY
    def set_friendly(self, friendly):
        self.friendly = friendly

    def get_friendly(self):
        return self.friendly



    # TEAM
    def set_team(self, team):
        self.team = team

    def get_team(self):
        return self.team



    # GROUP
    def set_group(self, group):
        self.group = group

    def get_group(self):
        return self.group



    # IMAGE
    def set_image(self, name = None):
        if name == None:
            self.warrior_image = None
        elif isinstance(name, str):
            self.warrior_image = pygame.image.load(os.path.abspath(os.getcwd()) + name)
            self.warrior_image = pygame.transform.scale(self.warrior_image, (60, 70))
        else:
            self.warrior_image = name

    def get_image(self): 
        return self.warrior_image



    # TO_STRING

    def toString(self):
        print("Unit in group: " + str(self.group) + " in team: " + str(self.team) + " on tile: " + str(self.node_position.get_position()) + " " + str(self.node_position.get_pixel_position()) + " with " + str(self.health) + " of " + str(self.max_health) + " with " + str(self.damage) + " damage")



  



