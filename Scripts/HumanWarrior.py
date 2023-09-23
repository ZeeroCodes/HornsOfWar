from Human import Human

class HumanWarrior(Human):
    def __init__(self, position = (0,0), max_health = 100, damage = 10, movement = 2, friendly = True):
        super().__init__("Warrior\\human_warrior.png", position, max_health, damage, movement, friendly)




