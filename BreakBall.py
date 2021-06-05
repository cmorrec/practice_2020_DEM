from BallForce import *
from EventBus import EventBus, destroyBall, draw


class BreakBall(BallForce):
    def __init__(self, x, y, radius, radiusBegin, alpha, velocity, velocityTheta, cn, cs, density, Emod, nu, color,
                 canvas, eventBus: EventBus):
        BallForce.__init__(self, x, y, radius, alpha, velocity, velocityTheta, cn, cs, density, Emod, nu, color, canvas)
        # self.strength = 0.01  # correct this
        # self.minEnergy = 0.3  # correct this
        self.strength = 0.01     # correct this
        self.minEnergy = 35 * radius / radiusBegin   # correct this
        self.breakEnergy = 0
        self.probability = 0
        self.eventBus = eventBus
        self.radiusBegin = radiusBegin
        self.interactionCountFlag = False

    def move(self):
        self.wallInteract()
        self.transfer()
        self.interactionCountFlag = True

        wall = MoveWall.getInstance()
        if self.radius <= wall.throughput:
            if wall.inDeleteCell(self):
                self.destruct(isNewBalls=False)

    def reactForEndInteraction(self, maxEnergy):
        if maxEnergy > self.minEnergy:
            print('maxEnergy',maxEnergy)
        if maxEnergy > self.minEnergy:
            self.breakEnergy += maxEnergy - self.minEnergy
            self.probability = 1 - exp(-1 * self.strength * self.breakEnergy)
            if self.probability > eps:
                print('probability', self.probability)
            if self.isDestruct():
                self.destruct()

    def isDestruct(self) -> bool:
        if self.radius < 0.5 * self.radiusBegin:
            return False
        for interaction in self.interactionArray:
            if not interaction.isBall:
                return False
        choice = [True, False]
        probability = [self.probability, 1 - self.probability]
        return rand.choice(choice, size=1, p=probability)

    def destruct(self, isNewBalls=True):
        newBalls = []
        if isNewBalls:
            newBalls = self.getNewBalls()
        data = {
            'newBalls': newBalls,
            'destroyingBall': self
        }
        self.canvas.delete(self.id)
        self.canvas.delete(self.id2)
        self.eventBus.emit(destroyBall, data)

    def getNewBall(self, beta, newRadius):
        delta = self.radius - newRadius
        newBall = BreakBall(self.x + delta * cos(beta), self.y + delta * sin(beta), newRadius, self.radiusBegin,
                            self.alphaRadian / pi * 180, self.velocityAbsolute, self.velocityTheta, self.cn, self.cs,
                            self.density, self.Emod, self.nu, self.color, self.canvas, self.eventBus)
        newBall.addVelocity(self.velocityAbsolute * cos(beta) / deltaTime / 5,
                            self.velocityAbsolute * sin(beta) / deltaTime / 5, 0)

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
