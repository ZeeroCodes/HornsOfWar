import pygame
from pygame.locals import *

from MapEditor.Map import Map

class App:

    # INIT
    def __init__(self):
        #self.hex_map = Map("testMap",(1366, 768))
        self.hex_map = Map()
        self.running = 1
        self.update_app()

    # UPDATE_APP
    # main loop of the app
    def update_app(self):
        while self.running == 1:
            self.running = self.hex_map.update_map()
            # If quit button is pushed, hex_map.update_map() will return 0, so this will end the program
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = 0
                if self.running == 0:
                    pygame.quit()
            pygame.display.update()





