from Scripts.Units.Unit import Unit
from Scripts.Widgets.NodeBase import NodeBase

class Human(Unit):
    def __init__(self, image, position = NodeBase((0,0), (50,150)), group = 1,  team = 1, friendly = True, max_health = 100, damage = 10, movement = 2):
        super().__init__("\\Images\\Units\\Human\\" + image, position, group, team, friendly, max_health, damage, movement)





