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
    def __init__(self, position = NodeBase((0,0), (50,150)), group = 1, team = 1 ,friendly = True, max_health = None, damage = None, movement = 2, level = 1):
        
        random.seed()

        self.max_health = max_health
        self.damage = damage

        if max_health == None:

            self.max_health = random.randint(Constants.MIN_HUMAN_WARRIOR_MAX_HEALTH, Constants.MAX_HUMAN_WARRIOR_MAX_HEALTH)

        if damage == None:
        
            self.damage = random.randrange(Constants.MIN_HUMAN_WARRIOR_DAMAGE, Constants.MAX_HUMAN_WARRIOR_DAMAGE)

        super().__init__("Warrior\\human_warrior.png", position, group, team, friendly, self.max_health, self.damage, movement, terrain_bonuses)
        self.level = level
        super().set_id("111")

    def getID(self):
        return 110 + self.level




