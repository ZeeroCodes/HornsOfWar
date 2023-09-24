from MapEditor.Units.Human import Human
from MapEditor.Widgets.NodeBase import NodeBase
import random

class HumanWarrior(Human):
    def __init__(self, position = NodeBase((0,0), (50,150)), group = 1, team = 1, max_health = random.randint(60, 80), damage = random.randrange(15,30), movement = 2):
        super().__init__("Warrior\\human_warrior.png", position, group, team, max_health, damage, movement)




