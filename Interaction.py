class Interaction:
    def __init__(self, isBall, number, accelerationX, accelerationY, jerkX, jerkY):
        self.isBall = isBall
        self.number = number
        self.accelerationX = accelerationX
        self.accelerationY = accelerationY
        self.jerkX = jerkX
        self.jerkY = jerkY

    def changeAcceleration(self, accelerationX, accelerationY, jerkX, jerkY):
        self.accelerationX = accelerationX
        self.accelerationY = accelerationY
        self.jerkX = jerkX
        self.jerkY = jerkY
