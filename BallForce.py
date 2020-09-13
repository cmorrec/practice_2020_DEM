from Ball import *


class BallForce(Ball):
    def __init__(self, x, y, radius, alpha, velocity, cn, cs, density, color, canvas):
        Ball.__init__(self, x, y, radius, alpha, velocity, cn, cs, density, color, canvas)
        self.accelerationBallX = 0
        self.accelerationBallY = 0
        self.accelerationBallAbsolute = 0
        self.accelerationBallAlpha = 0

    def drawPolygon(self):
        self.movePolygon()  # фактическое движение
        self.canvas.move(self.id,
                         self.velocityX * deltaTime - 0.5 * (accelerationX - self.accelerationBallX) * deltaTime ** 2,
                         self.velocityY * deltaTime - 0.5 * (
                                 accelerationY - self.accelerationBallY) * deltaTime ** 2)  # прорисовка движения

    def movePolygon(self):
        pos = self.canvas.coords(self.id)  # овал задается по 4-м коордиатам по которым
        self.x = (pos[0] + pos[2]) / 2  # можно найти координаты центра
        self.y = (pos[1] + pos[3]) / 2

        # Смена направления происходит в двух случаях(для обоих разные последствия):
        #   - Пересечения мячом линии стенки
        #   - Выхода за границы стенки(скорость больше радиуса * 2)
        if self.crossPolygon():
            self.toSpringForce(True)
        elif not self.isInsidePolygon():
            self.toSpringForce(False)
        # Обновление направлений скоростей
        self.addVelocity((self.accelerationX - self.accelerationBallX),
                         (self.accelerationY - self.accelerationBallY))

    def toSpringForce(self, isCrossLine):
        wall = MoveWall.getInstance()
        closestLine = None
        if isCrossLine:
            minDistance = wall.lines[0].distanceToLine(self.x, self.y)
            closestLine = wall.lines[0]
            for line in wall.lines:
                if minDistance > line.distanceToLine(self.x, self.y):
                    minDistance = line.distanceToLine(self.x, self.y)
                    closestLine = line
        else:
            for line in wall.lines:
                h = line.distanceToLine(self.x, self.y)
                if self.resetForLine(line):
                    xH = self.x + h * cos((-1) * self.alphaRadian)
                    yH = self.y - h * sin((-1) * self.alphaRadian)
                else:
                    xH = self.x + h * cos(self.alphaRadian)
                    yH = self.y - h * sin(self.alphaRadian)
                if line.isLine(xH, yH) or abs(line.x1 - line.x2) < eps \
                        or abs(line.y1 - line.y2) < eps:
                    closestLine = line
                    break

        alphaRadianLocal = self.alphaRadian - closestLine.alphaNorm
        if wall.flagMove:
            velocityXLocalWall = wall.velocityAbsolute * cos(alphaRadianLocal)
            velocityYLocalWall = wall.velocityAbsolute * sin(alphaRadianLocal)
        else:
            velocityXLocalWall = 0
            velocityYLocalWall = 0

        velocityXLocal = self.velocityAbsolute * cos(alphaRadianLocal)
        velocityYLocal = self.velocityAbsolute * sin(alphaRadianLocal)

        dampeningNormal = velocityXLocal * cn_wall
        dampeningTangent = velocityYLocal * cs_wall

        velocityXLocal = dampeningVelocity(dampeningNormal, velocityXLocal)
        velocityYLocal = dampeningVelocity(dampeningTangent, velocityYLocal)

        entryNormal = (velocityXLocal - velocityXLocalWall) * deltaTime
        entryTangent = (velocityYLocal - velocityYLocalWall - (
                self.velocityTheta * self.radius)) * deltaTime

        forceNormal = kn * entryNormal
        forceTangent = ks * entryTangent

        accelerationNormal = forceNormal / self.mass
        accelerationTangent = forceTangent / self.mass

        self.saveAcceleration(closestLine.alphaNorm, accelerationNormal, accelerationTangent)

    def saveAcceleration(self, alphaRadianLocal, accelerationNormal, accelerationTangent):
        accelerationBallAlpha = atan2(accelerationTangent, accelerationNormal + eps) + alphaRadianLocal
        accelerationBallAbsolute = sqrt(accelerationNormal ** 2 + accelerationTangent ** 2)
        self.accelerationBallX += accelerationBallAbsolute * cos(accelerationBallAlpha)
        self.accelerationBallY += accelerationBallAbsolute * sin(accelerationBallAlpha)
        self.accelerationBallAbsolute = sqrt(self.accelerationBallX ** 2 + self.accelerationBallY ** 2)
        self.accelerationBallAlpha = atan2(self.accelerationBallY, self.accelerationBallX + eps)

    def setAcceleration(self):
        if self.isCrossAnything:
            # self.removeAcceleration()
            return
        else:
            self.addAcceleration()
            if self.isInsidePolygon():
                self.removeAccelerationBall()

    def removeAccelerationBall(self):
        self.accelerationBallX = 0
        self.accelerationBallY = 0
        self.accelerationBallAbsolute = 0
        self.accelerationBallAlpha = 0

    # def resetPolygonForce(self):
    #     # Находим линию, которую пересекает шарик и изменяем угол шарика по известной формуле:
    #     # alpha = 2 * beta - alpha
    #     wall = MoveWall.getInstance()
    #     for line in wall.lines:
    #         if line.crossLine(self.x, self.y, self.radius):
    #             # Проверка на то двигается ли мячик к линии или от нее
    #             # (во втором случае менять направление не нужно)
    #             # if self.resetForLine(line):
    #             alphaRadianLocal = self.alphaRadian - line.alphaNorm
    #             if wall.flagMove:
    #                 velocityXLocalWall = wall.velocityAbsolute * cos(alphaRadianLocal)
    #                 velocityYLocalWall = wall.velocityAbsolute * sin(alphaRadianLocal)
    #             else:
    #                 velocityXLocalWall = 0
    #                 velocityYLocalWall = 0
    #
    #             velocityXLocal = self.velocityAbsolute * cos(alphaRadianLocal)
    #             velocityYLocal = self.velocityAbsolute * sin(alphaRadianLocal)
    #
    #             dampeningNormal = velocityXLocal * cn_wall
    #             dampeningTangent = velocityYLocal * cs_wall
    #
    #             velocityXLocal = dampeningVelocity(dampeningNormal, velocityXLocal)
    #             velocityYLocal = dampeningVelocity(dampeningTangent, velocityYLocal)
    #
    #             entryNormal = (velocityXLocal - velocityXLocalWall) * deltaTime
    #             entryTangent = (velocityYLocal - velocityYLocalWall - (
    #                     self.velocityTheta * self.radius)) * deltaTime
    #
    #             forceNormal = kn * entryNormal
    #             forceTangent = ks * entryTangent
    #
    #             accelerationNormal = forceNormal / self.mass
    #             accelerationTangent = forceTangent / self.mass
    #
    #             self.saveAcceleration(line.alphaNorm, accelerationNormal, accelerationTangent)
    #             break
