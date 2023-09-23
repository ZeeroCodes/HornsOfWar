from Unit import Unit

class Human(Unit):
    def __init__(self, image, position = (0,0), max_health = 100, damage = 10, movement = 2, friendly = True):
        super().__init__("\\Images\\Units\\Human\\" + image, position, max_health, damage, movement, friendly)





