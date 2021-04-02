from BallForce import *
from EventBus import EventBus, destroyBall


class BreakBall(BallForce):
    def __init__(self, x, y, radius, radiusBegin, alpha, velocity, velocityTheta, cn, cs, density, Emod, nu, color, canvas,
                 eventBus: EventBus):
        BallForce.__init__(self, x, y, radius, alpha, velocity, velocityTheta, cn, cs, density, Emod, nu, color, canvas)
        self.strength = 10     # correct this
        self.minEnergy = 0.1      # correct this
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
        # if len(self.interactionArray) > 0:
        #     self.info()

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
        if self.radius < self.radiusBegin / 2:
            return False
        choice = [True, False]
        probability = [self.probability, 1 - self.probability]
        return rand.choice(choice, size=1, p=probability)

    def getNewBalls(self):
        ball1 = BreakBall(self.x, self.y + self.radius * 0.4, self.radius * 0.4, self.radiusBegin,
                          self.alphaRadian / pi * 180, self.velocityAbsolute, self.velocityTheta, self.cn, self.cs,
                          self.density, self.Emod, self.nu, self.color, self.canvas, self.eventBus)
        ball2 = BreakBall(self.x, self.y - self.radius * 0.4, self.radius * 0.4, self.radiusBegin,
                          self.alphaRadian / pi * 180, self.velocityAbsolute, self.velocityTheta, self.cn, self.cs,
                          self.density, self.Emod, self.nu, self.color, self.canvas, self.eventBus)
        ball1.addVelocity(0, ball1.velocityY / deltaTime, 0)
        ball2.addVelocity(0, - ball2.velocityY / deltaTime, 0)
        balls = [ball1, ball2]
        return balls

    # использовать в момент удаления этого взаимодействия
    def addBreakInteraction(self, number, isBall):
        for interaction in self.interactionArray:
            if number == interaction.number and isBall == interaction.isBall:
                self.breakInteractions.append(interaction)