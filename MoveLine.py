from Line import *


class MoveLine(Line):
    def __init__(self, coordinate1, coordinate2):
        Line.__init__(self, coordinate1, coordinate2)
        self.startX1 = coordinate1.x
        self.startY1 = coordinate1.y
        self.startX2 = coordinate2.x
        self.startY2 = coordinate2.y
        self.id = 0

    def setID(self, idx):
        self.id = idx

    def setCoordinates(self, coordinate1, coordinate2):
        self.x1 = coordinate1.x
        self.x2 = coordinate2.x
        self.y1 = coordinate1.y
        self.y2 = coordinate2.y
        self.abs = self.findAbs()
        self.alphaTau = self.findTau()
        self.alphaNorm = self.alphaTau + (pi / 2)
