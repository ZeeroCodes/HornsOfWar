from Scripts.Units.Humans.Human import Human
from Scripts.Widgets.NodeBase import NodeBase
import random
import Constants

random.seed()

terrain_bonuses = {Constants.GRASS_TERRAIN:     60.0,
                   Constants.FOREST_TERRAIN:    50.0,
                   Constants.HILLS_TERRAIN:     60.0,
                   Constants.WATER_TERRAIN:     30.0,
                   Constants.MOUNTAIN_TERRAIN:  40.0,
                   Constants.SAND_TERRAIN:      50.0,
                   Constants.DIRT_TERRAIN:      60.0,
                   Constants.SWAMP_TERRAIN:     30.0}

class HumanWarrior(Human):
    def __init__(self, position = NodeBase((0,0), (50,150)), group = 1, team = 1 ,friendly = True, max_health = random.randint(60, 80), damage = random.randrange(15,30), movement = 2, level = 1):
        super().__init__("Warrior\\human_warrior.png", position, group, team, friendly, max_health, damage, movement)
        self.level = level
        super().set_id("111")

    def getID(self):
        return 110 + self.level




