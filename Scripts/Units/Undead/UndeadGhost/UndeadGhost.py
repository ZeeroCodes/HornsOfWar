from Scripts.Units.Undead.Undead import Undead
from Scripts.Widgets.NodeBase import NodeBase
import random


class UndeadGhost(Undead):
    def __init__(self, position = NodeBase((0,0), (50,150)), team = 1, friendly = True, max_health = random.randint(40, 65), damage = random.randrange(10,20), movement = 2, level = 1):
        super().__init__("Ghost\\undead_ghost.png", position, team, friendly, max_health, damage, movement)
        self.level = level
        super().set_id("211")

    def getID(self):
        return 210 + self.level





