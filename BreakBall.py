from BallForce import *
from EventBus import EventBus, destroyBall


class BreakBall(BallForce):
    def __init__(self, x, y, radius, radiusBegin, alpha, velocity, velocityTheta, cn, cs, density, Emod, nu, color,
                 canvas, eventBus: EventBus):
        BallForce.__init__(self, x, y, radius, alpha, velocity, velocityTheta, cn, cs, density, Emod, nu, color, canvas)
        self.strength = 0.1      # correct this
        self.minEnergy = 0.1    # correct this
        self.breakInteractions = []
        self.breakEnergy = 0
        self.probability = 0
        self.eventBus = eventBus
        self.radiusBegin = radiusBegin
        self.interactionCountFlag = False

    def move(self):
        self.wallInteract()
        self.transfer()

        if self.updateProps():
            if self.isDestruct():
                data = {
                    'newBalls': self.getNewBalls(),
                    'destroyingBall': self
                }
                self.canvas.delete(self.id)
                self.canvas.delete(self.id2)
                self.eventBus.emit(destroyBall, data)

    def updateProps(self):
        if len(self.breakInteractions) > 0:
            for interaction in self.breakInteractions:
                energy = interaction.maxEnergy
                if energy > self.minEnergy:
                    self.breakEnergy += energy - self.minEnergy
            self.probability = 1 - exp(-1 * self.strength * self.breakEnergy)
            self.breakInteractions.clear()
            return True
        return False

    def isDestruct(self) -> bool:
        if self.radius < self.radiusBegin:
            return False
        choice = [True, False]
        probability = [self.probability, 1 - self.probability]
        return rand.choice(choice, size=1, p=probability)

    def getNewBall(self, beta, newRadius):
        delta = self.radius - newRadius
        newBall = BreakBall(self.x + delta * cos(beta), self.y + delta * sin(beta), newRadius, self.radiusBegin,
                            self.alphaRadian / pi * 180, self.velocityAbsolute, self.velocityTheta, self.cn, self.cs,
                            self.density, self.Emod, self.nu, self.color, self.canvas, self.eventBus)
        newBall.addVelocity(self.velocityAbsolute * cos(beta) / deltaTime,
                            self.velocityAbsolute * sin(beta) / deltaTime, 0)

        return newBall

    def getNewBalls(self):
        numOfBalls = getBallsNum()
        newRadius = self.radius / (numOfBalls ** (1 / 3))
        deltaBeta = 2 * pi / numOfBalls
        beta = 0
        balls = []
        while numOfBalls > 0:
            balls.append(self.getNewBall(beta, newRadius))
            beta += deltaBeta
            numOfBalls -= 1

        return balls

    # использовать в момент удаления этого взаимодействия
    def addBreakInteraction(self, number, isBall):
        for interaction in self.interactionArray:
            if number == interaction.number and isBall == interaction.isBall:
                self.breakInteractions.append(interaction)
