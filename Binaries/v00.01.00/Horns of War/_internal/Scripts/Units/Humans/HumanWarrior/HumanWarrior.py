from Scripts.Units.Humans.Human import Human
from Scripts.Widgets.NodeBase import NodeBase
import random

class HumanWarrior(Human):
    def __init__(self, position = NodeBase((0,0), (50,150)), team = 1 ,friendly = True, max_health = random.randint(60, 80), damage = random.randrange(15,30), movement = 2, level = 1):
        super().__init__("Warrior\\human_warrior.png", position, team, friendly, max_health, damage, movement)
        self.level = level

    def getID(self):
        return 110 + self.level




