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

    def __init__(self, position = NodeBase((0,0), (50,150)), group = 2, team = 2, friendly = True, max_health = None, damage = None, movement = 3, level = 1):
        
        self.max_health = max_health
        self.damage = damage

        if max_health == None:

            self.max_health = random.randint(Constants.MIN_UNDEAD_GHOST_MAX_HEALTH, Constants.MAX_UNDEAD_GHOST_MAX_HEALTH)

        if damage == None:
        
            self.damage = random.randrange(Constants.MIN_UNDEAD_GHOST_DAMAGE, Constants.MAX_UNDEAD_GHOST_DAMAGE)

        super().__init__("Ghost\\undead_ghost.png", position, group, team, friendly, self.max_health, self.damage, movement)
        self.level = level
        super().set_id("211")

    def getID(self):
        return 210 + self.level





