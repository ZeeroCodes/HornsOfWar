import pygame

GRASS_TERRAIN = 0
FOREST_TERRAIN = 1
HILLS_TERRAIN = 2
WATER_TERRAIN = 3
MOUNTAIN_TERRAIN = 4
SAND_TERRAIN = 5
DIRT_TERRAIN = 6
SWAMP_TERRAIN = 7
STRUCTURE_TERRAIN = 20

SPAWNPOINT = DIRT_TERRAIN

HUMAN_WARRIOR_COST = 20
UNDEAD_GHOST_COST = 10

RADIUS = 50

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)
YELLOW = pygame.Color(255, 255, 0)
GREY = pygame.Color(80, 80, 80)
GOLD = pygame.Color(204, 204, 0)

MOVEMENT_SPEED = 1  # 1 = Fast
                    # 2 = Medium
                    # 3 = Slow