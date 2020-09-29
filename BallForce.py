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
                         self.velocityX * deltaTime + 0.5 * (accelerationX - self.accelerationBallX) * (deltaTime ** 2),
                         self.velocityY * deltaTime + 0.5 * (
                                 self.accelerationY - self.accelerationBallY) * (deltaTime ** 2))  # прорисовка движения

    def movePolygon(self):
        pos = self.canvas.coords(self.id)  # овал задается по 4-м коордиатам по которым
        self.x = (pos[0] + pos[2]) / 2  # можно найти координаты центра
        self.y = (pos[1] + pos[3]) / 2

        # Смена направления происходит в двух случаях(для обоих разные последствия):
        #   - Пересечения мячом линии стенки
        #   - Выхода за границы стенки(скорость больше радиуса * 2)
        if self.crossPolygon():
            self.toSpringForceLength()
        elif not self.isInsidePolygon():
            self.comeBack()
        # Обновление направлений скоростей
        self.addVelocity((self.accelerationX - self.accelerationBallX),
                         (self.accelerationY - self.accelerationBallY))

    def getCrossingLine(self):
        wall = MoveWall.getInstance()
        minDistance = wall.lines[0].distanceToLine(self.x, self.y)
        crossingLine = wall.lines[0]
        for line in wall.lines:
            if minDistance > line.distanceToLine(self.x, self.y):
                minDistance = line.distanceToLine(self.x, self.y)
                crossingLine = line
        return crossingLine

    def toSpringForce(self):
        wall = MoveWall.getInstance()

        closestLine = self.getCrossingLine()

        isToLine = self.resetForLine(closestLine)

        alphaRadianLocal = self.alphaRadian - closestLine.alphaNorm

        velocityXLocal = self.velocityAbsolute * cos(alphaRadianLocal)
        velocityYLocal = self.velocityAbsolute * sin(alphaRadianLocal)

        dampeningNormal = velocityXLocal * cn_wall
        dampeningTangent = velocityYLocal * cs_wall

        velocityXLocal = dampeningVelocity(dampeningNormal, velocityXLocal)
        velocityYLocal = dampeningVelocity(dampeningTangent, velocityYLocal)

        if wall.flagMove:
            # velocityNormal = wall.velocityAbsolute * cos(pi / 2 - closestLine.alphaNorm)
            velocityXLocalWall = wall.velocityAbsolute * cos(alphaRadianLocal)
            # velocityTangent = wall.velocityAbsolute * sin(pi / 2 - closestLine.alphaNorm)
            velocityYLocalWall = wall.velocityAbsolute * sin(alphaRadianLocal)
            if velocityXLocalWall * velocityXLocal >= 0:
                velocityXLocalWall *= 0
            if velocityYLocalWall * velocityYLocal >= 0:
                velocityYLocalWall *= 0
        else:
            velocityXLocalWall = 0
            velocityYLocalWall = 0

        self.changeVelocity(atan2(velocityYLocal, velocityXLocal + eps) + closestLine.alphaNorm,
                            sqrt(velocityXLocal ** 2 + velocityYLocal ** 2))

        if not isToLine:
            velocityXLocal *= -1
            velocityYLocal *= -1

        entryNormal = (velocityXLocal - velocityXLocalWall) * deltaTime
        entryTangent = (velocityYLocal - velocityYLocalWall - (
                self.velocityTheta * self.radius)) * deltaTime

        forceNormal = kn * entryNormal
        forceTangent = ks * entryTangent

        accelerationNormal = forceNormal / self.mass
        accelerationTangent = forceTangent / self.mass

        self.saveAcceleration(closestLine.alphaNorm, accelerationNormal, 0)

    def comeBack(self):
        self.alphaRadian += pi
        # wall = MoveWall.getInstance()
        # minX = wall.lines[0].x1
        # minY = wall.lines[0].y1
        # maxX = wall.lines[0].x1
        # maxY = wall.lines[0].y1
        # for line in wall.lines:
        #     if line.x1 > maxX:
        #         maxX = line.x1
        #     if line.x2 > maxX:
        #         maxX = line.x2
        #     if line.x1 < minX:
        #         minX = line.x1
        #     if line.x2 < minX:
        #         minX = line.x2
        #     if line.y1 > maxY:
        #         maxY = line.y1
        #     if line.y2 > maxY:
        #         maxY = line.y2
        #     if line.y1 < minY:
        #         minY = line.y1
        #     if line.y2 < minY:
        #         minY = line.y2
        # x0 = (maxX - minX) / 2 + minX
        # y0 = (maxY - minY) / 2 + minY
        #
        # entryNormal = sqrt((x0 - self.x) ** 2 + (y0 - self.y) ** 2)
        # forceNormal = (-1) * 1e3 * entryNormal
        # accelerationNormal = forceNormal / self.mass
        # alpha = atan2((1) * (y0 - self.y), (1) * (x0 - self.x) + eps)
        #
        # self.saveAcceleration(alpha, accelerationNormal, 0)

    def toSpringForceLength(self):
        wall = MoveWall.getInstance()

        closestLine = self.getCrossingLine()

        isToLine = self.resetForLine(closestLine)

        alphaRadianLocal = self.alphaRadian - closestLine.alphaNorm

        velocityXLocal = self.velocityAbsolute * cos(alphaRadianLocal)
        velocityYLocal = self.velocityAbsolute * sin(alphaRadianLocal)

        dampeningNormal = velocityXLocal * cn_wall
        dampeningTangent = velocityYLocal * cs_wall

        velocityXLocal = dampeningVelocity(dampeningNormal, velocityXLocal)
        velocityYLocal = dampeningVelocity(dampeningTangent, velocityYLocal)

        if wall.flagMove:
            # velocityNormal = wall.velocityAbsolute * cos(pi / 2 - closestLine.alphaNorm)
            velocityXLocalWall = wall.velocityAbsolute * cos(alphaRadianLocal)
            # velocityTangent = wall.velocityAbsolute * sin(pi / 2 - closestLine.alphaNorm)
            velocityYLocalWall = wall.velocityAbsolute * sin(alphaRadianLocal)
            if velocityXLocalWall * velocityXLocal >= 0:
                velocityXLocalWall *= 0
            if velocityYLocalWall * velocityYLocal >= 0:
                velocityYLocalWall *= 0
        else:
            velocityXLocalWall = 0
            velocityYLocalWall = 0

        self.changeVelocity(atan2(velocityYLocal, velocityXLocal + eps) + closestLine.alphaNorm,
                            sqrt(velocityXLocal ** 2 + velocityYLocal ** 2))

        if not isToLine:
            velocityXLocal *= -1
            velocityYLocal *= -1

        k = 1
        if not self.isInsidePolygon():
            k = -1

        entryNormal = self.radius - k * closestLine.distanceToLine(self.x, self.y)
        forceNormal = (-1) * kn * entryNormal

        accelerationNormal = forceNormal / self.mass
        entryTangent = 2 * sqrt(2 * self.radius * entryNormal - entryNormal ** 2) - (
                self.velocityTheta * self.radius) * deltaTime

        forceTangent = ks * entryTangent
        accelerationTangent = forceTangent / self.mass

        self.saveAccelerationLength(closestLine.alphaNorm, accelerationNormal, 0)

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

    def saveAccelerationLength(self, alphaRadianLocal, accelerationNormal, accelerationTangent):
        accelerationBallAlpha = atan2(accelerationTangent, accelerationNormal + eps) + alphaRadianLocal
        accelerationBallAbsolute = sqrt(accelerationNormal ** 2 + accelerationTangent ** 2)
        self.accelerationBallX = accelerationBallAbsolute * cos(accelerationBallAlpha)
        self.accelerationBallY = accelerationBallAbsolute * sin(accelerationBallAlpha)
        self.accelerationBallAbsolute = sqrt(self.accelerationBallX ** 2 + self.accelerationBallY ** 2)
        self.accelerationBallAlpha = atan2(self.accelerationBallY, self.accelerationBallX + eps)
    # def isInsideThatPolygon(self, lines):
    #     # Направляем луч из центра шарика вертикально вверх и считаем количество пересечений с линиями стенки
    #     # Если количество пересечений кратно двум, значит мяч вышел за границу стенки
    #     summary = 0
    #     for line in lines:
    #         if line.crossVerticalUp(self.x, self.y):
    #             summary += 1
    #     if summary % 2 == 1:
    #         return True
    #     else:
    #         return False
    #
    # def getNeededLine(self):
    #     wall = MoveWall.getInstance()
    #     lastLine = wall.lines[len(wall.lines) - 1]
    #     xB = lastLine.x2 + inf * cos(lastLine.alphaNorm)
    #     yB = lastLine.y2 - inf * sin(lastLine.alphaNorm)
    #     for line in wall.lines:
    #         xA = line.x2 + inf * cos(line.alphaNorm)
    #         yA = line.y2 - inf * sin(line.alphaNorm)
    #         lines = [Line(Coordinate(line.x1, line.y1), Coordinate(line.x2, line.y2)),
    #                  Line(Coordinate(line.x2, line.y2), Coordinate(xA, yA)),
    #                  Line(Coordinate(xA, yA), Coordinate(xB, yB)),
    #                  Line(Coordinate(xB, yB), Coordinate(line.x1, line.y1))]
    #         if self.isInsideThatPolygon(lines):
    #             return line
    #         xB = xA
    #         yB = yA
    #     return wall.lines[0]
