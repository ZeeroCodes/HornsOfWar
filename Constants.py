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

SAVEGAMES                       = True

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

MOVEMENT_SPEED                  = 3  # 1 = Fast   /   2 = Medium   /   3 = Slow

IA_MOVEMENT_VALUE               = 100
IA_STRUCTURE_MOVEMENT_VALUE     = 1000
IA_BONUS_FOR_TILE_PATH          = 5
IA_BONUS_FOR_DAMAGE_PERCENTAGE  = 20
IA_BONUS_PER_LEVEL              = 5
IA_BONUS_PER_CAN_ATTACK         = 10     
IA_BONUS_PER_CAN_KILL           = 20
IA_BONUS_PER_IS_HEROE           = 10     

MIN_HUMAN_HERO_MAX_HEALTH    = 100
MAX_HUMAN_HERO_MAX_HEALTH    = 150
MIN_HUMAN_HERO_DAMAGE        = 50
MAX_HUMAN_HERO_DAMAGE        = 75

MIN_HUMAN_WARRIOR_MAX_HEALTH    = 60
MAX_HUMAN_WARRIOR_MAX_HEALTH    = 80
MIN_HUMAN_WARRIOR_DAMAGE        = 30
MAX_HUMAN_WARRIOR_DAMAGE        = 40

MIN_UNDEAD_HERO_MAX_HEALTH    = 80
MAX_UNDEAD_HERO_MAX_HEALTH    = 100
MIN_UNDEAD_HERO_DAMAGE        = 40
MAX_UNDEAD_HERO_DAMAGE        = 50

MIN_UNDEAD_GHOST_MAX_HEALTH    = 30
MAX_UNDEAD_GHOST_MAX_HEALTH    = 60
MIN_UNDEAD_GHOST_DAMAGE        = 15
MAX_UNDEAD_GHOST_DAMAGE        = 30

