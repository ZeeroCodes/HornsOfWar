import pygame
import math
import os

from pygame.locals import *

class Button():

    # INIT
    def __init__(self, position, screen, image_name, image_pressed_name = "", size = (80, 60)):

        self.screen = screen

        # Loads normal button image
        self.image = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\Buttons\\" + image_name).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)

        # If theres button pressed image, loads it
        if image_pressed_name == "":
            self.pressed_image = pygame.image.load(os.path.abspath(os.getcwd()) + "\Images\\Buttons\\" + image_name).convert_alpha()
            self.pressed_image = pygame.transform.scale(self.pressed_image, size)
        else:
            self.pressed_image = pygame.image.load(os.path.abspath(os.getcwd())+"\Images\\Buttons\\" + image_pressed_name).convert_alpha()
            self.pressed_image = pygame.transform.scale(self.pressed_image, size)

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.clicked = False


    def get_rect(self):
        return self.rect


    def draw_button(self, pushed = False):
        if not pushed:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            self.screen.blit(self.pressed_image, (self.rect.x, self.rect.y))
    
    def is_pushed(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        return False

    # DRAW
    # draws button at the desired position
    def is_pushed2(self):
        pos = pygame.mouse.get_pos()
        running = False

        if self.rect.collidepoint(pos): # Proofs that the mouse pointer is on the sprite
            if pygame.mouse.get_pressed()[0] == 1:
                self.screen.blit(self.pressed_image, (self.rect.x, self.rect.y)) # Draws button
            else:
                self.screen.blit(self.image, (self.rect.x, self.rect.y)) # Draws button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # If the mouse is clicked and it is the first loop
                self.clicked = True
                running = True # Changes variable to close the game              
        else:
            self.screen.blit(self.image, (self.rect.x, self.rect.y)) # Draws button

        # This variable functionality is to avoid different true values of the mouse clicked during the 
        # loops of the game, because when the button is clicked, as the loops are so fast, it is posible that
        # the program reads true values during some loops, so this variable avoid that problem
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False   

        return running
