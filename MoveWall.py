from Wall import *


class MoveWall(Wall):
    __instance = None

    def __init__(self, canvas, color, coordinates=None, accelerationX=0, accelerationY=0, lines=None, velocityX=0,
                 velocityY=0, absX=0, absY=0):
        Wall.__init__(self, canvas, color, coordinates, accelerationX, accelerationY, lines)
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.absX = absX
        self.absY = absY
        MoveWall.__instance = self

    def move(self):
        if abs(self.lines[0].x1 - self.lines[0].startX1) > self.absX:
            self.changeVelocityX()
        if abs(self.lines[0].y1 - self.lines[0].startY1) > self.absY:
            self.changeVelocityY()
        for line in self.lines:
            self.canvas.move(line.id, self.velocityX, self.velocityY)  # прорисовка движения стенки
            line.setCoordinates(Coordinate(line.x1 + self.velocityX, line.y1 + self.velocityY),
                                Coordinate(line.x2 + self.velocityX, line.y2 + self.velocityY))

    def changeVelocityX(self):
        self.velocityX *= -1

    def changeVelocityY(self):
        self.velocityY *= -1

    @staticmethod
    def getInstance():
        return MoveWall.__instance
