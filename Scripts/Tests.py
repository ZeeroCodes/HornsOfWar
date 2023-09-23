import os
from NodeBase import NodeBase

def load_map(map_name):
    rows = 0
    cols = 0
    dictionary = dict()
    with open(os.path.abspath(os.getcwd()) + "\\Maps\\" + map_name + ".txt", 'r') as f:
        lines = f.readlines()
        rows = int(lines[0])
        cols = int(lines[1])
        for line in lines[2:]:
            number = []
            char_number = ""
            for char in line:
                if char == " ":
                    number.append(int(char_number))
                    char_number = ""
                else:
                    char_number += char
            number.append(int(char_number))
            dictionary[(number[0], number[1])] = NodeBase((number[0], number[1]), (number[2], number[3]))

import pygame

bgcolor = 0, 0, 0
linecolor = 255, 255, 255
x = y = 0
running = 1
screen = pygame.display.set_mode((640, 400))

while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    elif event.type == pygame.MOUSEMOTION:
        x, y = event.pos

    screen.fill(bgcolor)
    pygame.draw.line(screen, linecolor, (x, 0), (x, 399))
    pygame.draw.line(screen, linecolor, (0, y), (639, y))
    pygame.display.flip()