from Wall import *

deltaVelocityWall = 1


class MoveWall(Wall):
    __instance = None

    def __init__(self, canvas, color, coordinates=None, accelerationX=0, accelerationY=0, lines=None, velocityX=0,
                 velocityY=0, velocityTheta=0, absX=0, absY=0, centerX=0, centerY=0):
        Wall.__init__(self, canvas, color, coordinates, accelerationX, accelerationY, lines)
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.velocityAbsolute = sqrt((self.velocityX ** 2) + (self.velocityY ** 2))
        self.velocityAlpha = atan2(self.velocityY, self.velocityX + eps)
        self.velocityTheta = velocityTheta
        self.absX = absX
        self.absY = absY
        self.freqX = 0
        self.freqY = 70 * pi
        self.ArgX = 0
        self.ArgY = 0
        MoveWall.__instance = self
        self.flagMove = True

        # Для потенциальной энергии
        self.maxY = self.lines[0].y1
        for line in self.lines:
            if line.y1 > self.maxY:
                self.maxY = line.y1
            if line.y2 > self.maxY:
                self.maxY = line.y2
        self.maxY += absY

        self.centerX = centerX
        self.centerY = centerY
        self.canvas.bind_all('<KeyPress-u>', self.upVelocity)
        self.canvas.bind_all('<KeyPress-d>', self.downVelocity)
        self.canvas.bind_all('<KeyPress-l>', self.leftVelocity)
        self.canvas.bind_all('<KeyPress-r>', self.rightVelocity)
        self.canvas.bind_all('<KeyPress-s>', self.changeFlag)

    @staticmethod
    def getInstance():
        return MoveWall.__instance

    def draw(self):
        for line in self.lines:
            self.canvas.coords(line.id,
                               displayRatio * line.x1,
                               displayRatio * line.y1,
                               displayRatio * line.x2,
                               displayRatio * line.y2)

    def getVelocityAlpha(self):
        return atan2(self.getVelocityY(), self.getVelocityX() + eps)

    def getVelocityX(self):
        if not self.flagMove:
            return 0
        return self.absX * self.freqX * cos(self.ArgX)

    def getVelocityY(self):
        if not self.flagMove:
            return 0
        return self.absY * self.freqY * cos(self.ArgY)

    def getAccelerationX(self):
        if not self.flagMove:
            return 0
        return - self.absX * self.freqX**2 * sin(self.ArgX)

    def getAccelerationY(self):
        if not self.flagMove:
            return 0
        return - self.absY * self.freqY**2 * sin(self.ArgY)

    def thetaMove(self):
        if abs(self.velocityTheta) < eps:
            return
        littleTheta = self.velocityTheta * deltaTime
        for line in self.lines:
            # Определение радиуса и угла изначальных для каждой точки
            R_1 = distanceNow(Coordinate(line.x1, line.y1), Coordinate(self.centerX, self.centerY))
            R_2 = distanceNow(Coordinate(line.x2, line.y2), Coordinate(self.centerX, self.centerY))
            alpha_1 = atan2(line.y1 - self.centerY, line.x1 - self.centerX + eps)
            alpha_2 = atan2(line.y2 - self.centerY, line.x2 - self.centerX + eps)

            # Определение нового угла
            alpha_1 += littleTheta
            alpha_2 += littleTheta

            # Нахождение новых координат
            x_1 = self.centerX + R_1 * cos(alpha_1)
            x_2 = self.centerX + R_2 * cos(alpha_2)
            y_1 = self.centerY + R_1 * sin(alpha_1)
            y_2 = self.centerY + R_2 * sin(alpha_2)

            # Сохраняем
            line.setCoordinates(Coordinate(x_1, y_1), Coordinate(x_2, y_2))

    # def linearMove(self):
    #     if abs(self.velocityX) < eps and abs(self.velocityY) < eps:
    #         return
    #     littleX = self.velocityX * deltaTime
    #     littleY = self.velocityY * deltaTime
    #     # Перемещение центра
    #     self.centerX += littleX
    #     self.centerY += littleY
    #
    #     for i, line in enumerate(self.lines):
    #         # Нахождение новых координат
    #         x_1 = line.x1 + littleX
    #         x_2 = line.x2 + littleX
    #         y_1 = line.y1 + littleY
    #         y_2 = line.y2 + littleY
    #
    #         # Сохраняем
    #         line.setCoordinates(Coordinate(x_1, y_1), Coordinate(x_2, y_2))

    def linearMove(self):
        if abs(self.freqX) < eps and abs(self.freqY) < eps:
            return
        NextArgX = self.ArgX + self.freqX * deltaTime
        NextArgY = self.ArgY + self.freqY * deltaTime
        littleX = self.absX * (sin(NextArgX) - sin(self.ArgX))
        littleY = self.absY * (sin(NextArgY) - sin(self.ArgY))
        self.ArgX = NextArgX
        self.ArgY = NextArgY
        # Перемещение центра
        self.centerX += littleX
        self.centerY += littleY

        for i, line in enumerate(self.lines):
            # Нахождение новых координат
            x_1 = line.x1 + littleX
            x_2 = line.x2 + littleX
            y_1 = line.y1 + littleY
            y_2 = line.y2 + littleY

            # Сохраняем
            line.setCoordinates(Coordinate(x_1, y_1), Coordinate(x_2, y_2))

    def move(self):
        if self.lines[0].x1 - self.lines[0].startX1 > self.absX or self.lines[0].x1 - self.lines[0].startX1 < 0:
            self.revertVelocityX()
        if self.lines[0].y1 - self.lines[0].startY1 > self.absY or self.lines[0].y1 - self.lines[0].startY1 < 0:
            self.revertVelocityY()
        if self.flagMove:
            self.thetaMove()
            self.linearMove()

    def revertVelocityX(self):
        self.velocityX *= -1
        self.changeAlpha()

    def revertVelocityY(self):
        self.velocityY *= -1
        self.changeAlpha()

    def changeAlpha(self):
        self.velocityAlpha = atan2(self.velocityY, self.velocityX + eps)

    def upVelocity(self, event):
        if self.velocityY > 0:
            self.changeVelocityY(deltaVelocityWall)
        else:
            self.changeVelocityY(-deltaVelocityWall)

    def downVelocity(self, event):
        if self.velocityY >= 0:
            self.changeVelocityY(-deltaVelocityWall)
        else:
            self.changeVelocityY(deltaVelocityWall)

    def rightVelocity(self, event):
        if self.velocityX > 0:
            self.changeVelocityX(deltaVelocityWall)
        else:
            self.changeVelocityX(-deltaVelocityWall)

    def leftVelocity(self, event):
        if self.velocityX >= 0:
            self.changeVelocityX(-deltaVelocityWall)
        else:
            self.changeVelocityX(deltaVelocityWall)

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
