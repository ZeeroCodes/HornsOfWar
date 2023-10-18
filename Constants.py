import pygame

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)
YELLOW = pygame.Color(255, 255, 0)
GREY = pygame.Color(80, 80, 80)
GOLD = pygame.Color(204, 204, 0)

UNIT_DICTIONARY =   {   '110': 'HumanHero',
                        '111': 'HumanWarrior',
                        
                        '210': 'UndeadHero',
                        '211': 'UndeadGhost'
                    }

SAVEGAMES                       = False

RADIUS                          = 50

GRASS_TERRAIN                   = 0
FOREST_TERRAIN                  = 1
HILLS_TERRAIN                   = 2
WATER_TERRAIN                   = 3
MOUNTAIN_TERRAIN                = 4
SAND_TERRAIN                    = 5
DIRT_TERRAIN                    = 6
SWAMP_TERRAIN                   = 7
STRUCTURE_TERRAIN               = 20

SPAWNPOINT                      = DIRT_TERRAIN

PLAYER_INITIAL_MONEY            = 100
IA_INITIAL_MONEY                = 100

HUMAN_WARRIOR_COST              = 20
UNDEAD_GHOST_COST               = 10

MOVEMENT_SPEED                  = 2  # 1 = Fast   /   2 = Medium   /   3 = Slow

IA_MOVEMENT_VALUE               = 100
IA_STRUCTURE_MOVEMENT_VALUE     = 1000
IA_BONUS_FOR_TILE_PATH          = 5
IA_BONUS_FOR_DAMAGE_PERCENTAGE  = 20
IA_BONUS_PER_LEVEL              = 5
IA_BONUS_PER_CAN_ATTACK         = 10     
IA_BONUS_PER_CAN_KILL           = 20
IA_BONUS_PER_IS_HEROE           = 10         
