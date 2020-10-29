from Ball import *
from Interaction import *


def getJerk(velocity, acceleration, k, mass):
    accelerationFirst = acceleration
    deltaEntry = velocity * deltaTime + acceleration / 2 * deltaTime ** 2
    deltaForce = k * deltaEntry
    accelerationNext = acceleration + deltaForce / mass
    jerk = (accelerationNext - accelerationFirst) / deltaTime
    while abs((accelerationNext - acceleration) / (acceleration + eps)) > epsAcceleration:
        acceleration = accelerationNext
        deltaEntry = velocity * deltaTime + accelerationNext / 2 * deltaTime ** 2 + jerk / 6 * deltaTime ** 3
        deltaForce = k * deltaEntry
        accelerationNext = acceleration + deltaForce / mass
        jerk = (accelerationNext - accelerationFirst) / deltaTime
    return jerk


def getAccelerationFieldNormal(alpha):
    alphaAccelerationXRadianLocal = -alpha
    alphaAccelerationYRadianLocal = pi / 2 - alpha
    accelerationFieldNormal = MoveWall.getInstance().accelerationX * cos(
        alphaAccelerationXRadianLocal) + MoveWall.getInstance().accelerationY * cos(alphaAccelerationYRadianLocal)
    return accelerationFieldNormal


class BallForce(Ball):
    def __init__(self, x, y, radius, alpha, velocity, cn, cs, density, color, canvas):
        cnForce = getForceDamping(cn)
        # print(cnForce)
        csForce = getForceDamping(cs)
        Ball.__init__(self, x, y, radius, alpha, velocity, cnForce, csForce, density, color, canvas)
        self.accelerationInteractionX = 0
        self.accelerationInteractionY = 0
        self.jerkX = 0
        self.jerkY = 0
        self.interactionArray = []

    def move(self):
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
        self.x += self.velocityX * deltaTime - 0.5 * (self.accelerationX + self.accelerationInteractionX) * (
                deltaTime ** 2) - self.jerkX * (deltaTime ** 3) / 3
        self.y += self.velocityY * deltaTime - 0.5 * (self.accelerationY + self.accelerationInteractionY) * (
                deltaTime ** 2) - self.jerkY * (deltaTime ** 3) / 3
        self.theta += self.velocityTheta % (2 * pi)

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

    def expandForce(self, line, numberOfLine):
        alphaRadianLocal = self.alphaRadian - line.alphaNorm

        velocityXLocal = self.velocityAbsolute * cos(alphaRadianLocal)
        velocityYLocal = self.velocityAbsolute * sin(alphaRadianLocal)

        dampeningNormal = velocityXLocal * cn_wall
        dampeningTangent = velocityYLocal * cs_wall

        velocityXLocal = dampeningVelocity(dampeningNormal, velocityXLocal)
        velocityYLocal = dampeningVelocity(dampeningTangent, velocityYLocal)

        self.changeVelocity(atan2(velocityYLocal, velocityXLocal + eps) + line.alphaNorm,
                            sqrt(velocityXLocal ** 2 + velocityYLocal ** 2))
        # self.rotationCSWall(velocityYLocal, dampeningTangent)

        k = 1
        if not self.isInsidePolygon():
            k = -1

        entryNormal = self.radius - k * line.distanceToLine(self.x, self.y)
        forceNormal = (1) * kn * entryNormal
        accelerationNormal = forceNormal / self.mass
        print(accelerationNormal)
        jerk = getJerk(velocityXLocal, accelerationNormal + getAccelerationFieldNormal(line.alphaNorm), kn, self.mass)
        accelerationNormal += self.jerk * deltaTime

        self.saveAccelerationLength(line.alphaNorm, accelerationNormal, jerk, entryNormal, isBall=False,
                                    number=numberOfLine)

    def rotationCSWall(self, velocityYLocal, dampeningTangent):
        self.velocityTheta += - velocityYLocal / abs(velocityYLocal + eps) * sqrt(
            abs(dampeningTangent * 2 / self.momentInertial))

    def isCrossLineBefore(self, numberOfLine):
        for interaction in self.interactionArray:
            if (not interaction.isBall) and interaction.number == numberOfLine:
                return True
        return False

    def deleteInteractionLine(self, numberOfLine):
        for interaction in self.interactionArray:
            if (not interaction.isBall) and interaction.number == numberOfLine:
                # print('wall', interaction.n)
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

    def saveAccelerationLength(self, alphaRadianLocal, accelerationNormal, jerkNormal, entryNormal, isBall, number):
        accelerationInteractionX = accelerationNormal * cos(alphaRadianLocal)
        accelerationInteractionY = accelerationNormal * sin(alphaRadianLocal)
        jerkX = jerkNormal * cos(alphaRadianLocal)
        jerkY = jerkNormal * sin(alphaRadianLocal)
        for interaction in self.interactionArray:
            if interaction.number == number and interaction.isBall == isBall:
                interaction.changeAcceleration(accelerationInteractionX, accelerationInteractionY, jerkX, jerkY,
                                               entryNormal)
                return
        self.addInteraction(
            Interaction(isBall, number, accelerationInteractionX, accelerationInteractionY, jerkX, jerkY, entryNormal))

    def addInteraction(self, interaction):
        self.interactionArray.append(interaction)

    def rotationCS(self, velocityYLocal, dampeningTangentVelocity):
        self.velocityTheta += - velocityYLocal / abs(velocityYLocal + eps) * sqrt(
            self.mass * abs(dampeningTangentVelocity ** 2 / self.momentInertial))

    # def info(self):
    #     print('velocityAlpha', self.alphaRadian, 'velocityAbs', self.velocityAbsolute)
    #     print('velocityX', self.velocityX, 'velocityY', self.velocityY)
    #     print('accelerationX =', self.accelerationX, 'accelerationY =', self.accelerationY)
    #     print('accelerationInteractionX =', self.accelerationInteractionX, '\taccelerationInteractionY =', self.accelerationInteractionY)
    #     print('jerkX =', self.jerkX, 'jerkY =', self.jerkY)
    #     for i, interaction in enumerate(self.interactionArray):
    #         print('interaction = ', i, '\tisBall =', interaction.isBall, '\tnumber =', interaction.number)
    #         print('\taccelerationX =', interaction.accelerationX, '\taccelerationY =', interaction.accelerationY)
    #         print('\tjerkX =', interaction.jerkX, '\tjerkY =', interaction.jerkY)
    #     print()
