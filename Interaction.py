class Interaction:
    def __init__(self, isBall, number, accelerationX, accelerationY, jerkX, jerkY, entryNormal):
        self.isBall = isBall
        self.number = number
        self.entryNormal = entryNormal
        self.accelerationX = accelerationX
        self.accelerationY = accelerationY
        self.jerkX = jerkX
        self.jerkY = jerkY

    def changeAcceleration(self, accelerationX, accelerationY, jerkX, jerkY,  entryNormal):
        self.accelerationX = accelerationX
        self.accelerationY = accelerationY
        self.jerkX = jerkX
        self.jerkY = jerkY
        self.entryNormal = entryNormal
