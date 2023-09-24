from MapEditor.Units.Undead import Undead
from MapEditor.Widgets.NodeBase import NodeBase
import random

class UndeadGhost(Undead):
    def __init__(self, position = NodeBase((0,0), (50,150)), group = 1, team = 1, max_health = random.randint(40, 65), damage = random.randrange(10,20), movement = 2):
        super().__init__("Ghost\\undead_ghost.png", position, group, team, max_health, damage, movement)




