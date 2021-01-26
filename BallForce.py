from Ball import *
from Interaction import *


def getAccelerationFieldNormal(alpha):
    alphaAccelerationXRadianLocal = -alpha
    alphaAccelerationYRadianLocal = pi / 2 - alpha
    accelerationFieldNormal = MoveWall.getInstance().accelerationX * cos(
        alphaAccelerationXRadianLocal) + MoveWall.getInstance().accelerationY * cos(alphaAccelerationYRadianLocal)
    return accelerationFieldNormal


class BallForce(Ball):
    def __init__(self, x, y, radius, alpha, velocity, velocityTheta, cn, cs, density, Emod, nu, color, canvas):
        Ball.__init__(self, x, y, radius, alpha, velocity, velocityTheta, cn, cs, density, Emod, nu, color, canvas)
        self.accelerationInteractionX = 0
        self.accelerationInteractionY = 0
        self.Gmod = self.Emod / (2 * (1 + self.nu))
        self.jerkX = 0
        self.jerkY = 0
        self.jerkTheta = 0
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
        self.theta += (self.velocityTheta * deltaTime - 0.5 * self.accelerationTheta * (
                deltaTime ** 2) - self.jerkTheta * (deltaTime ** 3) / 3) % (2 * pi)

    def addVelocityMethod(self):
        self.accelerationInteractionX = 0
        self.accelerationInteractionY = 0
        self.jerkX = 0
        self.jerkY = 0
        self.jerkTheta = 0
        self.accelerationTheta = 0
        for interaction in self.interactionArray:
            self.accelerationInteractionX += interaction.accelerationX
            self.accelerationInteractionY += interaction.accelerationY
            self.jerkX += interaction.jerkX
            self.jerkY += interaction.jerkY
            self.jerkTheta += interaction.jerkTheta
            self.accelerationTheta += interaction.accelerationAngular

        self.addVelocity(
            (self.accelerationX + self.accelerationInteractionX - self.jerkX * deltaTime / 2),
            (self.accelerationY + self.accelerationInteractionY - self.jerkY * deltaTime / 2))

        self.addVelocityAngular(self.accelerationTheta - self.jerkTheta * deltaTime / 2)

    def expandForce(self, line, numberOfLine):
        alphaRadianLocal = self.alphaRadian - line.alphaNorm
        radius = self.radius
        mass = self.mass

        wall = MoveWall.getInstance()
        alphaRadianLocalWall = wall.getVelocityAlpha() - line.alphaNorm
        E_eff = ((1 - (self.nu ** 2)) / self.Emod + (1 - (nu_wall ** 2)) / Emod_wall) ** (-1)
        G_eff = ((2 - self.nu) / self.Gmod + (2 - nu_wall) / Gmod_wall) ** (-1)

        velocityXLocalWall = wall.getVelocityX() * cos(alphaRadianLocalWall) + wall.getVelocityY() * sin(
            alphaRadianLocalWall)
        velocityYLocalWall = wall.getVelocityX() * cos(alphaRadianLocalWall) - wall.getVelocityY() * sin(
            alphaRadianLocalWall)
        accelerationXLocalWall = wall.getAccelerationX() * cos(alphaRadianLocalWall) + wall.getAccelerationY() * sin(
            alphaRadianLocalWall)
        accelerationYLocalWall = wall.getAccelerationX() * cos(alphaRadianLocalWall) - wall.getAccelerationY() * sin(
            alphaRadianLocalWall)

        velocityXLocal = self.velocityAbsolute * cos(alphaRadianLocal)
        velocityYLocal = self.velocityAbsolute * sin(alphaRadianLocal)

        k = 1
        if not self.isInsidePolygon():
            k = -1

        entryNormal = radius - k * line.distanceToLine(self.x, self.y)
        stiffness = getStiffness(radius, abs(entryNormal), E_eff)
        forceNormal = stiffness * entryNormal
        accelerationNormal = forceNormal / mass

        radiusOfWallInContactDot = distanceNow(Coordinate(self.x, self.y),
                                               Coordinate(wall.centerX, wall.centerY)) + radius - entryNormal
        velocityRelativeNormal = velocityXLocal - velocityXLocalWall

        velocityRelativeTangent = velocityYLocal - velocityYLocalWall - (
                self.velocityTheta * radius - wall.velocityTheta * radiusOfWallInContactDot)

        signVelocityTangent = customSign(velocityRelativeTangent)
        signVelocityAngular = customSign(self.velocityTheta - wall.velocityTheta)

        # если вылетит из коробки могут быть проблемы со знаками forceNormal
        accelerationAngular, accelerationTangent = self.findAccelerationAngular(signVelocityTangent, forceNormal, 1,
                                                                                radius, signVelocityAngular)

        # ----------------------------- Damping part -----------------------------
        accelerationDampeningNormal = velocityRelativeNormal * getDampingNormal(radius, entryNormal,
                                                                                mass, cn_wall,
                                                                                E_eff) / mass * (-1)
        accelerationDampeningTangent = velocityRelativeTangent * getDampingTangent(radius, entryNormal,
                                                                                   mass, cs_wall,
                                                                                   G_eff) / mass

        accelerationNormal += accelerationDampeningNormal
        accelerationTangent += accelerationDampeningTangent
        # ----------------------------- End damping part -----------------------------

        accelerationRelativeNormal = accelerationNormal - accelerationXLocalWall
        accelerationRelativeTangent = accelerationTangent - accelerationYLocalWall

        jerkNormal, jerkTangent, jerkAngular = self.getJerk(entryNormal, velocityRelativeNormal,
                                                            accelerationRelativeNormal, signVelocityTangent, 1,
                                                            radius, signVelocityAngular, accelerationAngular,
                                                            accelerationRelativeTangent, E_eff)
        accelerationNormal += jerkNormal * deltaTime
        accelerationTangent += jerkTangent * deltaTime
        accelerationAngular += jerkAngular * deltaTime

        self.saveAccelerationLength(line.alphaNorm, accelerationNormal, accelerationTangent, jerkNormal, jerkTangent,
                                    jerkAngular, entryNormal, accelerationAngular, isBall=False, number=numberOfLine,
                                    stiffness=stiffness)

    def findAccelerationAngular(self,
                                signVelocityRelativeTangent,
                                forceNormal,
                                signVelocityTangentRelativeAngular,
                                radiusEffective,
                                signVelocityRelativeAngular):
        forceSliding = coefficientOfFrictionSliding * forceNormal * signVelocityRelativeTangent
        momentSliding = forceSliding * radiusEffective * signVelocityTangentRelativeAngular

        momentRolling = coefficientOfFrictionRolling * forceNormal * radiusEffective * signVelocityRelativeAngular * (
            -1)

        accelerationAngular = (momentSliding + momentRolling) / self.momentInertial
        accelerationTangent = forceSliding / self.mass

        return accelerationAngular, accelerationTangent

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
                wallInteraction.append(interaction.n)
                self.interactionArray.remove(interaction)
                break

    def saveAccelerationLength(self, alphaRadianLocal,
                               accelerationNormal,
                               accelerationTangent,
                               jerkNormal,
                               jerkTangent,
                               jerkAngular,
                               entryNormal,
                               accelerationAngular,
                               isBall, number, stiffness):
        accelerationInteractionX = accelerationNormal * cos(alphaRadianLocal) + accelerationTangent * sin(
            alphaRadianLocal)

        accelerationInteractionY = accelerationNormal * sin(alphaRadianLocal) - accelerationTangent * cos(
            alphaRadianLocal)

        jerkX = jerkNormal * cos(alphaRadianLocal) + jerkTangent * sin(alphaRadianLocal)
        jerkY = jerkNormal * sin(alphaRadianLocal) - jerkTangent * cos(alphaRadianLocal)
        for interaction in self.interactionArray:
            if interaction.number == number and interaction.isBall == isBall:
                interaction.changeAcceleration(accelerationInteractionX, accelerationInteractionY, jerkX, jerkY,
                                               jerkAngular,
                                               entryNormal, accelerationAngular, stiffness)
                return
        self.addInteraction(Interaction(isBall, number, accelerationInteractionX, accelerationInteractionY,
                                        jerkX, jerkY, jerkAngular, entryNormal, accelerationAngular, stiffness))

    def addInteraction(self, interaction):
        self.interactionArray.append(interaction)

    def rotationCS(self, velocityYLocal, dampeningTangentVelocity):
        self.velocityTheta += - velocityYLocal / abs(velocityYLocal + eps) * sqrt(
            self.mass * abs(dampeningTangentVelocity ** 2 / self.momentInertial))

    def iterJerk(self,
                 entryNormal,
                 velocityNormal,
                 accelerationFirstNormal,
                 jerkNormal,
                 signVelocityRelativeTangent,
                 signVelocityTangentRelativeAngular,
                 radiusEffective,
                 signVelocityRelativeAngular,
                 accelerationFirstAngular,
                 jerkAngular,
                 accelerationFirstTangent,
                 jerkTangent, E_eff):
        mass = self.mass
        deltaEntryNormal = velocityNormal * deltaTime + (accelerationFirstNormal * (deltaTime ** 2)) / 2 + (
                jerkNormal * (deltaTime ** 3)) / 6
        entryNextNormal = entryNormal + deltaEntryNormal
        stiffness = getStiffness(radiusEffective, abs(entryNextNormal), E_eff)
        forceNextNormal = stiffness * entryNextNormal * customSign(accelerationFirstNormal)
        deltaForceNormal = forceNextNormal - (accelerationFirstNormal * mass)
        accelerationNextNormal = forceNextNormal / mass
        jerkNormal = (accelerationNextNormal - accelerationFirstNormal) / deltaTime

        deltaForceSliding = coefficientOfFrictionSliding * deltaForceNormal * signVelocityRelativeTangent
        deltaMomentSliding = deltaForceSliding * radiusEffective * signVelocityTangentRelativeAngular
        deltaMomentRolling = coefficientOfFrictionRolling * deltaForceNormal * radiusEffective * (
                signVelocityRelativeAngular * (-1))

        accelerationNextAngular = accelerationFirstAngular + (
                deltaMomentSliding + deltaMomentRolling) / self.momentInertial + jerkAngular * deltaTime
        accelerationNextTangent = accelerationFirstTangent + deltaForceSliding / mass + jerkTangent * deltaTime

        jerkAngular = (accelerationNextAngular - accelerationFirstAngular) / deltaTime
        jerkTangent = (accelerationNextTangent - accelerationFirstTangent) / deltaTime

        #######################################################################

        return jerkNormal, accelerationNextNormal, \
               jerkTangent, accelerationNextTangent, \
               jerkAngular, accelerationNextAngular

    def getJerk(self, entry,
                velocityNormal,
                accelerationNormal,
                signVelocityRelativeTangent,
                signVelocityTangentRelativeAngular,
                radiusEffective,
                signVelocityRelativeAngular,
                accelerationAngular,
                accelerationTangent, E_eff):
        accelerationFirstNormal = accelerationNormal
        accelerationFirstAngular = accelerationAngular
        accelerationFirstTangent = accelerationTangent
        jerkNormal, accelerationNextNormal, \
        jerkTangent, accelerationNextTangent, \
        jerkAngular, accelerationNextAngular = self.iterJerk(entry, velocityNormal, accelerationFirstNormal, 0,
                                                             signVelocityRelativeTangent,
                                                             signVelocityTangentRelativeAngular,
                                                             radiusEffective,
                                                             signVelocityRelativeAngular,
                                                             accelerationFirstAngular, 0,
                                                             accelerationFirstTangent, 0, E_eff)
        # i = 1
        while abs((accelerationNextNormal - accelerationNormal) / (accelerationNormal + eps)) > epsAcceleration and \
                abs((accelerationNextAngular - accelerationAngular) / (accelerationAngular + eps)) > epsAcceleration and \
                abs((accelerationNextTangent - accelerationTangent) / (accelerationTangent + eps)) > epsAcceleration:
            accelerationNormal = accelerationNextNormal
            accelerationAngular = accelerationNextAngular
            accelerationTangent = accelerationNextTangent

            jerkNormal, accelerationNextNormal, \
            jerkTangent, accelerationNextTangent, \
            jerkAngular, accelerationNextAngular = self.iterJerk(entry, velocityNormal, accelerationFirstNormal,
                                                                 jerkNormal,
                                                                 signVelocityRelativeTangent,
                                                                 signVelocityTangentRelativeAngular,
                                                                 radiusEffective,
                                                                 signVelocityRelativeAngular,
                                                                 accelerationFirstAngular, jerkAngular,
                                                                 accelerationFirstTangent, jerkTangent, E_eff)
            # i += 1
        # print(i)
        return jerkNormal, jerkTangent, jerkAngular

    # def info(self):
    #     print('velocityAlpha', self.alphaRadian, 'velocityAbs', self.velocityAbsolute)
    #     print('velocityX', self.velocityX, 'velocityY', self.velocityY)
    #     print('accelerationX =', self.accelerationX, 'accelerationY =', self.accelerationY)
    #     print('accelerationInteractionX =', self.accelerationInteractionX, '\taccelerationInteractionY =',
    #     self.accelerationInteractionY)
    #     print('jerkX =', self.jerkX, 'jerkY =', self.jerkY)
    #     for i, interaction in enumerate(self.interactionArray):
    #         print('interaction = ', i, '\tisBall =', interaction.isBall, '\tnumber =', interaction.number)
    #         print('\taccelerationX =', interaction.accelerationX, '\taccelerationY =', interaction.accelerationY)
    #         print('\tjerkX =', interaction.jerkX, '\tjerkY =', interaction.jerkY)
    #     print()
