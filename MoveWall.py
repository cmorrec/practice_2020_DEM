from Wall import *


class MoveWall(Wall):
    __instance = None

    def __init__(self, canvas, color, coordinates=None, accelerationX=0, accelerationY=0, lines=None, velocityX=0,
                 velocityY=0, absX=0, absY=0):
        Wall.__init__(self, canvas, color, coordinates, accelerationX, accelerationY, lines)
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.velocityAbsolute = sqrt((velocityX ** 2) + (velocityY ** 2))
        self.velocityAlpha = atan2(velocityY, velocityX + eps)
        self.absX = absX
        self.absY = absY
        MoveWall.__instance = self
        self.flagMove = True
        self.canvas.bind_all('<KeyPress-u>', self.upVelocity)
        self.canvas.bind_all('<KeyPress-d>', self.downVelocity)
        self.canvas.bind_all('<KeyPress-l>', self.leftVelocity)
        self.canvas.bind_all('<KeyPress-r>', self.rightVelocity)
        self.canvas.bind_all('<KeyPress-s>', self.changeFlag)

    @staticmethod
    def getInstance():
        return MoveWall.__instance

    def move(self):
        if self.lines[0].x1 - self.lines[0].startX1 > self.absX or self.lines[0].x1 - self.lines[0].startX1 < 0:
            self.revertVelocityX()
        if self.lines[0].y1 - self.lines[0].startY1 > self.absY or self.lines[0].y1 - self.lines[0].startY1 < 0:
            self.revertVelocityY()
        if self.flagMove:
            for line in self.lines:
                self.canvas.move(line.id, self.velocityX, self.velocityY)  # прорисовка движения стенки
                line.setCoordinates(Coordinate(line.x1 + self.velocityX, line.y1 + self.velocityY),
                                    Coordinate(line.x2 + self.velocityX, line.y2 + self.velocityY))

    def revertVelocityX(self):
        self.velocityX *= -1
        self.changeAlpha()

    def revertVelocityY(self):
        self.velocityY *= -1
        self.changeAlpha()

    def changeAlpha(self):
        self.velocityAlpha = atan2(self.velocityY, self.velocityX + eps)

    def upVelocity(self, event):
        if self.velocityY >= 0:
            self.changeVelocityY(1)
        else:
            self.changeVelocityY(-1)

    def downVelocity(self, event):
        if self.velocityY >= 0:
            self.changeVelocityY(-1)
        else:
            self.changeVelocityY(1)

    def rightVelocity(self, event):
        if self.velocityX >= 0:
            self.changeVelocityX(1)
        else:
            self.changeVelocityX(-1)

    def leftVelocity(self, event):
        if self.velocityX >= 0:
            self.changeVelocityX(-1)
        else:
            self.changeVelocityX(1)

    def changeVelocityX(self, decrement):
        self.velocityX += decrement
        self.changeAlpha()
        self.changeVelocityAbsolute()

    def changeVelocityY(self, decrement):
        self.velocityY += decrement
        self.changeAlpha()
        self.changeVelocityAbsolute()

    def changeVelocityAbsolute(self):
        self.velocityAbsolute = sqrt(self.velocityX ** 2 + self.velocityY ** 2)

    def changeFlag(self, event):
        if self.flagMove:
            self.flagMove = False
        else:
            self.flagMove = True
