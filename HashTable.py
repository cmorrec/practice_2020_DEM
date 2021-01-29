from GlobalUtils import *
from MoveWall import *


class HashObject:
    def __init__(self, isBall, number):
        self.isBall = isBall
        self.number = number


class Pair:
    def __init__(self, i, j):
        self.i = i
        self.j = j


class HashTable:

    def __init__(self, balls):
        wall = MoveWall.getInstance()
        self.width = wall.width
        self.height = wall.height
        radius = 0
        for ball in balls:
            if ball.radius > radius:
                radius = ball.radius
        self.delta = 3 * radius  # elements.fastest_ball.velocity * deltaTime * 100
        self.elementsOfX = int(ceil(self.width / self.delta))
        self.elementsOfY = int(ceil(self.height / self.delta))
        self.numOfElements = self.elementsOfX * self.elementsOfY
        self.table = [[] * 1 for i in range(self.numOfElements)]

    def hashBall(self, ball):
        elementOfX = floor(ball.x / self.delta)
        elementOfY = floor(ball.y / self.delta)
        return self.elementsOfX * elementOfY + elementOfX

    # def hashLine(self, line):
    # int deltax := abs(x1 - x0)
    # int deltay := abs(y1 - y0)
    # real error := 0
    # real deltaerr := (deltay + 1) / (deltax + 1)
    # int y := y0
    # int diry := y1 - y0
    # if diry > 0
    #     diry = 1
    # if diry < 0
    #     diry = -1
    # for x from x0 to x1
    #     plot(x, y)
    #     error := error + deltaerr
    #     if error >= 1.0
    #         y := y + diry
    #         error := error - 1.0
    #
    # deltaX = abs(line.x1 - line.x2)
    # deltaY = abs(line.y1 - line.y2)
    # error = float(0)
    # deltaError = (deltay + 1) / (deltax + 1)

    def update(self, balls):
        # print(self.table.shape)
        for i in range(self.numOfElements):
            self.table[i].clear()

        for i in range(len(balls)):
            self.table[self.hashBall(balls[i])].append(HashObject(isBall=True, number=i))

        # for i, line in enumerate(MoveWall.getInstance().lines):
        #     indexes = self.hashLine(line)
        #     for j in indexes:
        #         self.table[j].append(HashObject(isBall=False, number=i))

    def getPairs(self, balls):
        self.update(balls)

        pairs = []
        for i in range(self.numOfElements):
            isDiagonalRight = True
            isDiagonalLeft = True
            elements1 = self.table[i]
            for j in range(len(elements1)):
                for k in range(j + 1, len(elements1)):
                    pairs.append(Pair(elements1[j], elements1[k]))

            if i % self.elementsOfX != self.elementsOfX - 1:
                elements2 = self.table[i + 1]
                for element1 in elements1:
                    for element2 in elements2:
                        pairs.append(Pair(element1, element2))
            else:
                isDiagonalRight = False

            if floor(i / self.elementsOfX) != self.elementsOfY - 1:
                elements3 = self.table[i + self.elementsOfX]
                for element1 in elements1:
                    for element3 in elements3:
                        pairs.append(Pair(element1, element3))
            else:
                isDiagonalRight = False
                isDiagonalLeft = False

            if isDiagonalRight:
                elements4 = self.table[i + self.elementsOfX + 1]
                for element1 in elements1:
                    for element4 in elements4:
                        pairs.append(Pair(element1, element4))

            if isDiagonalLeft and i % self.elementsOfX != 0:
                elements5 = self.table[i + self.elementsOfX - 1]
                for element1 in elements1:
                    for element5 in elements5:
                        pairs.append(Pair(element1, element5))

        return pairs
