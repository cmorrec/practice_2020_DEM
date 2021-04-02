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
        self.delta = 3 * radius
        self.elementsOfX = int(ceil(self.width / self.delta))
        self.elementsOfY = int(ceil(self.height / self.delta))
        self.numOfElements = self.elementsOfX * self.elementsOfY
        self.table = [[] * 1 for _ in range(self.numOfElements)]

    def hashBall(self, ball):
        elementOfX = int(floor(ball.x / self.delta))
        elementOfY = int(floor(ball.y / self.delta))
        resultElement = (self.elementsOfX * elementOfY) + elementOfX
        return resultElement

    def update(self, balls):
        for i in range(self.numOfElements):
            self.table[i].clear()

        for i in range(len(balls)):
            index = self.hashBall(balls[i])
            self.table[index].append(HashObject(isBall=True, number=i))

    def getPairs(self, balls):
        self.update(balls)

        pairs = []
        for i in range(self.numOfElements):
            isDiagonalRight = True
            isDiagonalLeft = True
            elements1 = self.table[i]
            # -------- Right block --------------
            for j in range(len(elements1)):
                for k in range(j + 1, len(elements1)):
                    pairs.append(Pair(elements1[j], elements1[k]))
            # -----------------------------------

            if (i % self.elementsOfX) != (self.elementsOfX - 1):
                elements2 = self.table[i + 1]
                for j in range(len(elements1)):
                    for k in range(len(elements2)):
                        pairs.append(Pair(elements1[j], elements2[k]))
            else:
                isDiagonalRight = False

            if floor(i / self.elementsOfX) != (self.elementsOfY - 1):
                elements3 = self.table[i + self.elementsOfX]
                for j in range(len(elements1)):
                    for k in range(len(elements3)):
                        pairs.append(Pair(elements1[j], elements3[k]))
            else:
                isDiagonalRight = False
                isDiagonalLeft = False

            if isDiagonalRight:
                elements4 = self.table[i + self.elementsOfX + 1]
                for j in range(len(elements1)):
                    for k in range(len(elements4)):
                        pairs.append(Pair(elements1[j], elements4[k]))

            if isDiagonalLeft and ((i % self.elementsOfX) != 0):
                elements5 = self.table[i + self.elementsOfX - 1]
                for j in range(len(elements1)):
                    for k in range(len(elements5)):
                        pairs.append(Pair(elements1[j], elements5[k]))

        return pairs

    # def updateDelta(self, balls):
    #     radius = 0
    #     for ball in balls:
    #         if ball.radius > radius:
    #             radius = ball.radius
    #     self.delta = 3 * radius
    #     self.elementsOfX = int(ceil(self.width / self.delta))
    #     self.elementsOfY = int(ceil(self.height / self.delta))
    #     self.numOfElements = self.elementsOfX * self.elementsOfY
    #     self.table = [[] * 1 for _ in range(self.numOfElements)]
    #     print('new delta ', self.delta, '\n',
    #           'new elements of x', self.elementsOfX, '\n',
    #           'new elements of y', self.elementsOfY, '\n',
    #           'new elements num', self.numOfElements, '\n\n')
    #
