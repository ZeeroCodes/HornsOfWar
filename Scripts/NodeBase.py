class NodeBase():
    def __init__(self, position, pixel_position):
        self.F = 0
        self.G = 0
        self.H = 0
        self.parent = None
        self.terrain_movement_cost = 1
        self.position = position
        self.pixel_position = pixel_position
    
    def get_terrain_movement_cost(self):
        return self.terrain_movement_cost

    def get_pixel_position(self):
        return self.pixel_position

    def set_pixel_position(self, pixel_position):
        self.pixel_position = pixel_position

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def getF(self):
        return self.F

    def getH(self):
        return self.H

    def getG(self):
        return self.G

    def setF(self, F = -1):
        if F == -1:
            self.F = self.H + self.G
        else:
            self.F = F

    def setG(self, G):
        self.G = G

    def setH(self, H):
        self.H = H

    def get_parent(self):
        return self.parent

    def set_parent(self,parent):
        self.parent = parent

    def toString(self):
        print("NodeBase: " + str(self.position) + " on " + str(self.pixel_position) + ", G = " + str(self.G) + ", H = " + str(self.H) + ", F = " + str(self.F)) # + ", parent = " + str(self.parent.get_position()))




