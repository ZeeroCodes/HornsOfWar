from Scripts.Units.Undead.Undead import Undead
from Scripts.Widgets.NodeBase import NodeBase
import random
import Constants

random.seed()

terrain_bonuses = {Constants.GRASS_TERRAIN:     60.0,
                   Constants.FOREST_TERRAIN:    50.0,
                   Constants.HILLS_TERRAIN:     50.0,
                   Constants.WATER_TERRAIN:     60.0,
                   Constants.MOUNTAIN_TERRAIN:  50.0,
                   Constants.SAND_TERRAIN:      60.0,
                   Constants.DIRT_TERRAIN:      60.0,
                   Constants.SWAMP_TERRAIN:     60.0}

class UndeadGhost(Undead):
    def __init__(self, position = NodeBase((0,0), (50,150)), team = 1, friendly = True, max_health = random.randint(40, 65), damage = random.randrange(10,20), movement = 3, level = 1):
        super().__init__("Ghost\\undead_ghost.png", position, team, friendly, max_health, damage, movement, terrain_bonuses)
        self.level = level

    def getID(self):
        return 210 + self.level





