from Line import *


class MoveLine(Line):
    def __init__(self, coordinate1, coordinate2):
        Line.__init__(self, coordinate1)
        self.startX1 = coordinate1.x1
        self.startY1 = coordinate1.y1
        self.startX2 = coordinate2.x2
        self.startY2 = coordinate2.y2
        self.id = 0

    def setID(self, idx):
        self.id = idx

    def setCoordinates(self, coordinate1):
        self.x1 = coordinate1.x1
        self.x2 = coordinate1.x2
        self.y1 = coordinate1.y1
        self.y2 = coordinate1.y2
        self.abs = self.findAbs()
        self.alphaTau = self.findTau()
        self.alphaNorm = self.alphaTau + (pi / 2)
