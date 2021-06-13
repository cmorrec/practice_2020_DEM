class Interaction:
    def __init__(self, isBall, number,
                 accelerationX,
                 accelerationY,
                 jerkX, jerkY, jerkTheta,
                 entryNormal,
                 accelerationAngular,
                 stiffness,
                 isCount):
        self.isBall = isBall
        self.number = number
        self.isCount = isCount
        if isCount or not isBall:
            self.entryNormal = entryNormal
            self.accelerationX = accelerationX
            self.accelerationY = accelerationY
            self.jerkX = jerkX
            self.jerkY = jerkY
            self.jerkTheta = jerkTheta
            self.accelerationAngular = accelerationAngular
            self.stiffness = stiffness
            self.n = 1
            self.maxEnergy = (stiffness * (entryNormal ** 2)) / 2
        else:
            self.entryNormal = 0
            self.accelerationX = 0
            self.accelerationY = 0
            self.jerkX = 0
            self.jerkY = 0
            self.jerkTheta = 0
            self.accelerationAngular = 0
            self.stiffness = 0
            self.n = 0
            self.maxEnergy = 0

    def changeAcceleration(self,
                           accelerationX,
                           accelerationY,
                           jerkX, jerkY, jerkTheta,
                           entryNormal,
                           accelerationAngular,
                           stiffness):
        if self.isCount or not self.isBall:
            self.accelerationX = accelerationX
            self.accelerationY = accelerationY
            self.jerkX = jerkX
            self.jerkY = jerkY
            self.jerkTheta = jerkTheta
            self.entryNormal = entryNormal
            self.accelerationAngular = accelerationAngular
            self.stiffness = stiffness
            self.n += 1
            energy = (stiffness * (entryNormal ** 2)) / 2
            if energy > self.maxEnergy:
                self.maxEnergy = energy
