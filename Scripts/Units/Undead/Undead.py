from Scripts.Units.Unit import Unit
from Scripts.Widgets.NodeBase import NodeBase

class Undead(Unit):
    def __init__(self, image, position = NodeBase((0,0), (50,150)), team = 1, friendly = True, max_health = 100, damage = 10, movement = 2, terrain_bonuses = dict()):
        super().__init__("\\Images\\Units\\Undead\\" + image, position, team, friendly, max_health, damage, movement, terrain_bonuses)




