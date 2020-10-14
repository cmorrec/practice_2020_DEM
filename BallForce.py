from Ball import *
from Interaction import *


class BallForce(Ball):
    def __init__(self, x, y, radius, alpha, velocity, cn, cs, density, color, canvas):
        Ball.__init__(self, x, y, radius, alpha, velocity, cn, cs, density, color, canvas)
        self.accelerationInteractionX = 0
        self.accelerationInteractionY = 0
        self.jerkX = 0
        self.jerkY = 0
        self.interactionArray = []

    def canvasMove(self):
        self.canvas.move(self.id,
                         self.velocityX * deltaTime - 0.5 * (self.accelerationX + self.accelerationInteractionX) * (
                                 deltaTime ** 2) - self.jerkX * (deltaTime ** 3) / 3,
                         self.velocityY * deltaTime - 0.5 * (
                                 self.accelerationY + self.accelerationInteractionY) * (
                                 deltaTime ** 2) - self.jerkY * (deltaTime ** 3) / 3)

    def move(self):
        pos = self.canvas.coords(self.id)  # овал задается по 4-м коордиатам по которым
        self.x = (pos[0] + pos[2]) / 2  # можно найти координаты центра
        self.y = (pos[1] + pos[3]) / 2

        # Смена направления происходит в двух случаях(для обоих разные последствия):
        #   - Пересечения мячом линии стенки
        #   - Выхода за границы стенки(скорость больше радиуса * 2)
        i = 0
        isCrossLine = False
        for line in MoveWall.getInstance().lines:
            if line.crossLine(self.x, self.y, self.radius):
                self.expandForce(line, i)
                isCrossLine = True
            elif self.isCrossLineBefore(i) and self.isInsidePolygon():
                self.deleteInteractionLine(i)
            i += 1

        if (not self.isInsidePolygon()) and (not isCrossLine):
            self.comeBack()

        # Обновление направлений скоростей
        self.addVelocityMethod()

    def addVelocityMethod(self):
        self.accelerationInteractionX = 0
        self.accelerationInteractionY = 0
        for interaction in self.interactionArray:
            self.accelerationInteractionX += interaction.accelerationX
            self.accelerationInteractionY += interaction.accelerationY

        self.jerkX = 0
        self.jerkY = 0
        for interaction in self.interactionArray:
            self.jerkX += interaction.jerkX
            self.jerkY += interaction.jerkY

        self.addVelocity(
            (self.accelerationX + self.accelerationInteractionX - self.jerkX * deltaTime / 2),
            (self.accelerationY + self.accelerationInteractionY - self.jerkY * deltaTime / 2))

    def getJerk(self, velocity, acceleration, k, mass):
        jerk = 0
        accelerationFirst = acceleration
        accelerationNext = 0
        while abs((accelerationNext - acceleration) / (acceleration + eps)) > epsAcceleration:
            if accelerationNext != 0:
                acceleration = accelerationNext
            deltaEntry = velocity * deltaTime + accelerationNext / 2 * deltaTime ** 2 + jerk / 6 * deltaTime ** 3
            deltaForce = k * deltaEntry
            accelerationNext = acceleration + deltaForce / mass
            jerk = (accelerationNext - accelerationFirst) / deltaTime
        return jerk

    def expandForce(self, line, numberOfLine):
        wall = MoveWall.getInstance()

        # closestLine, numberOfLine = self.getCrossingLine()

        isToLine = self.resetForLine(line)

        alphaRadianLocal = self.alphaRadian - line.alphaNorm
        accelerationYRadianLocal = pi/2 - line.alphaNorm

        velocityXLocal = self.velocityAbsolute * cos(alphaRadianLocal)
        velocityYLocal = self.velocityAbsolute * sin(alphaRadianLocal)

        dampeningNormal = velocityXLocal * cn_wall
        dampeningTangent = velocityYLocal * cs_wall

        velocityXLocal = dampeningVelocity(dampeningNormal, velocityXLocal)
        velocityYLocal = dampeningVelocity(dampeningTangent, velocityYLocal)

        if wall.flagMove:
            velocityXLocalWall = wall.velocityAbsolute * cos(alphaRadianLocal)
            velocityYLocalWall = wall.velocityAbsolute * sin(alphaRadianLocal)
            if velocityXLocalWall * velocityXLocal >= 0:
                velocityXLocalWall *= 0
            if velocityYLocalWall * velocityYLocal >= 0:
                velocityYLocalWall *= 0
        else:
            velocityXLocalWall = 0
            velocityYLocalWall = 0

        self.changeVelocity(atan2(velocityYLocal, velocityXLocal + eps) + line.alphaNorm,
                            sqrt(velocityXLocal ** 2 + velocityYLocal ** 2))

        if not isToLine:
            velocityXLocal *= -1
            velocityYLocal *= -1

        k = 1
        if not self.isInsidePolygon():
            k = -1

        entryNormal = self.radius - k * line.distanceToLine(self.x, self.y)
        forceNormal = (1) * kn * entryNormal
        accelerationNormal = forceNormal / self.mass
        jerk = self.getJerk(velocityXLocal, accelerationNormal+accelerationY*cos(accelerationYRadianLocal), kn, self.mass)
        accelerationNormal += self.jerk * deltaTime

        self.saveAccelerationLength(line.alphaNorm, accelerationNormal, jerk, isBall=False, number=numberOfLine)

    def isCrossLineBefore(self, numberOfLine):
        for interaction in self.interactionArray:
            if (not interaction.isBall) and interaction.number == numberOfLine:
                return True
        return False

    def deleteInteractionLine(self, numberOfLine):
        for interaction in self.interactionArray:
            if (not interaction.isBall) and interaction.number == numberOfLine:
                self.interactionArray.remove(interaction)
                break

    def setAcceleration(self):
        # В силовом методе мы не отключаем поле ускорений, в этом нет необходимости
        # Но необходимо отключать ускорение от взаимодействия в тот момент,
        # когда шар ни с кем не пересекается и находится внутри стенки
        if (not self.isCrossAnything) and self.isInsidePolygon():
            self.removeAccelerationBall()

    def removeAccelerationBall(self):
        self.accelerationInteractionX = 0
        self.accelerationInteractionY = 0
        self.jerkX = 0
        self.jerkY = 0

    def saveAccelerationLength(self, alphaRadianLocal, accelerationNormal, jerkNormal, isBall, number):
        accelerationInteractionX = accelerationNormal * cos(alphaRadianLocal)
        accelerationInteractionY = accelerationNormal * sin(alphaRadianLocal)
        jerkX = jerkNormal * cos(alphaRadianLocal)
        jerkY = jerkNormal * sin(alphaRadianLocal)
        for interaction in self.interactionArray:
            if interaction.number == number and interaction.isBall == isBall:
                interaction.changeAcceleration(accelerationInteractionX, accelerationInteractionY, jerkX, jerkY)
                return
        self.addInteraction(Interaction(isBall, number, accelerationInteractionX, accelerationInteractionY, jerkX, jerkY))

    def addInteraction(self, interaction):
        self.interactionArray.append(interaction)
