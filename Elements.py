from HashTable import *


# Класс Elements содержит в себе массив шаров и координирует их движение между собой,
# в частности отслеживает и регулирует столкновение шаров

# В будущем нужно реализовать  проверку о ненакладывании мячей один на другой


def distanceNext(i, j):
    # Расстояние между двумя шарами в следующий момент времени
    return sqrt(((i.x + i.velocityX * deltaTime) - (j.x + j.velocityX * deltaTime)) ** 2 + (
            (i.y + i.velocityY * deltaTime) - (j.y + j.velocityY * deltaTime)) ** 2)


def isCross(i, j):
    # проверяем столкнулись ли шары  и если да -- двигаются ли они навстречу друг другу
    if distanceNext(i, j) < distanceNow(i, j) < (i.radius + j.radius):
        return True
    return False


def rotationBallHerz(i, j, velocityThetaI, velocityThetaJ, velocity1YLocal, velocity2YLocal, velocity1XLocal,
                     velocity2XLocal):
    n = sqrt((16 * i.radius * j.radius) / (9 * pi ** 2 * kn ** 2 * (i.radius + j.radius)))
    mu = 2000
    force = mu * n * sqrt(abs(velocity1XLocal - velocity2XLocal)) ** 3
    i.velocityTheta += force / (i.radius * i.mass) * (1 - i.cs) * (velocity1YLocal - velocity2YLocal)


def rotationHerz(i, j, velocity1YLocal, velocity2YLocal, velocity1XLocal, velocity2XLocal):
    velocityThetaI = i.velocityTheta
    velocityThetaJ = j.velocityTheta
    rotationBallHerz(i, j, velocityThetaI, velocityThetaJ, velocity1YLocal, velocity2YLocal, velocity1XLocal,
                     velocity2XLocal)
    rotationBallHerz(j, i, velocityThetaI, velocityThetaJ, velocity2YLocal, velocity1YLocal, velocity1XLocal,
                     velocity2XLocal)
    velocity1YLocal -= sqrt(i.momentInertial * i.velocityTheta ** 2 / i.mass)
    velocity2YLocal -= sqrt(j.momentInertial * j.velocityTheta ** 2 / j.mass)


def method(i, j):
    # Решение задачи о нецентральном упругом ударе двух дисков, путём приведения к задаче о
    # столкновении шаров по оси Х(линия столкновения становится горизонтальной, происходит
    # переход в локальную систему координат)
    # Также учет диссипации при каждом столкновении шаров

    # Угол между линией удара и горизонталью
    gama = atan2((i.y - j.y), (i.x - j.x))
    # Углы направления шаров в локальной системе координат
    alphaRadian1Local = i.alphaRadian - gama
    alphaRadian2Local = j.alphaRadian - gama
    # Скорости шаров в локальной системе координат
    velocity1XLocal = i.velocityAbsolute * cos(alphaRadian1Local)
    velocity1YLocal = i.velocityAbsolute * sin(alphaRadian1Local)
    velocity2XLocal = j.velocityAbsolute * cos(alphaRadian2Local)
    velocity2YLocal = j.velocityAbsolute * sin(alphaRadian2Local)

    # Непосредственно решение задачи о нецентральном упругом ударе двух дисков
    velocity1XLocalNew = ((i.mass - j.mass) * velocity1XLocal + 2 * j.mass * velocity2XLocal) / (i.mass + j.mass)
    velocity2XLocalNew = (2 * i.mass * velocity1XLocal + (j.mass - i.mass) * velocity2XLocal) / (i.mass + j.mass)
    # Демпфирование
    dampeningNormalI = (velocity1XLocalNew - velocity2XLocalNew) * i.cn
    dampeningNormalJ = (velocity2XLocalNew - velocity1XLocalNew) * j.cn
    dampeningTangentI = (velocity1YLocal - velocity2YLocal - (
            i.velocityTheta * i.radius + j.velocityTheta * j.radius)) * i.cs
    dampeningTangentJ = (velocity2YLocal - velocity1YLocal - (
            i.velocityTheta * i.radius + j.velocityTheta * j.radius)) * j.cs
    # # Учет демпфирования
    velocity1XLocalNew = dampeningVelocity(dampeningNormalI, velocity1XLocalNew)
    velocity2XLocalNew = dampeningVelocity(dampeningNormalJ, velocity2XLocalNew)
    # velocity1YLocal = dampeningVelocity(dampeningTangentI, velocity1YLocal)
    # velocity2YLocal = dampeningVelocity(dampeningTangentJ, velocity2YLocal)
    # Задание новой угловой скорости дисков
    # rotationHerz(i, j, velocity1YLocal, velocity2YLocal, velocity1XLocal, velocity2XLocal)
    # Возвращение к глобальной системе координат
    newAlphaI = atan2(velocity1YLocal, velocity1XLocalNew + eps) + gama
    newAlphaJ = atan2(velocity2YLocal, velocity2XLocalNew + eps) + gama
    newVelocityAbsoluteI = sqrt(velocity1XLocalNew ** 2 + velocity1YLocal ** 2)
    newVelocityAbsoluteJ = sqrt(velocity2XLocalNew ** 2 + velocity2YLocal ** 2)
    # Задание нового вектора скорости
    i.changeVelocity(newAlphaI, newVelocityAbsoluteI)
    j.changeVelocity(newAlphaJ, newVelocityAbsoluteJ)


class Elements:
    def __init__(self, balls, canvas):
        self.balls = balls
        self.started = False
        self.canvas = canvas
        # self.startEnergy = self.energy()
        # self.step = 0
        print('start')
        self.hashTable = HashTable(self.balls)
        self.pairs = self.hashTable.getPairs(self.balls)
        # for i in range(self.hashTable.elementsOfX):
        #     canvas.create_line(displayRatio * i * self.hashTable.delta, 0, displayRatio * i * self.hashTable.delta,
        #                        displayRatio * self.hashTable.height)
        # for i in range(self.hashTable.elementsOfY):
        #     canvas.create_line(0, displayRatio * i * self.hashTable.delta, displayRatio * self.hashTable.width,
        #                        displayRatio * i * self.hashTable.delta)

    # def energyMonitoring(self):
    #     print("Количество энергии", self.energyToSee(), "\n")

    def start(self, event):
        self.started = True
        # self.energyMonitoring()

    def begin(self):
        self.started = True
        # self.energyMonitoring()

    def exit(self, event):
        self.started = False
        saveResults(self)
        # self.energyMonitoring()
        # plotter()

    # def energyToSee(self):
    #     energyCount = 0
    #     for ball in self.balls:
    #         energyCount += 0.5 * ball.mass * (ball.velocityAbsolute ** 2) + 0.5 * ball.momentInertial * (
    #                 ball.velocityTheta ** 2) + ball.mass * MoveWall.getInstance().accelerationY * (
    #                                MoveWall.getInstance().maxY - ball.y)
    #     return energyCount
    #
    # def energy(self):
    #     energyCount = self.energyKinetic() + self.energyPotential()
    #     # summaryPlot.append(energyCount)
    #     return energyCount

    # def energyKinetic(self):
    #     energyCount = 0
    #     for ball in self.balls:
    #         energyCount += 0.5 * ball.mass * (ball.velocityAbsolute ** 2) + 0.5 * ball.momentInertial * (
    #                 ball.velocityTheta ** 2)
    #     kineticPlot.append(energyCount)
    #     return energyCount

    # def energyPotential(self):
    #     energyCount = 0
    #     for ball in self.balls:
    #         energyCount += ball.mass * MoveWall.getInstance().accelerationY * (MoveWall.getInstance().maxY - ball.y)
    #         if isForce:
    #             for interaction in ball.interactionArray:
    #                 if interaction.isBall:
    #                     energyCount += (interaction.stiffness * interaction.entryNormal ** 2) / 4
    #                 else:
    #                     energyCount += (interaction.stiffness * interaction.entryNormal ** 2) / 2
    #
    #     potentialPlot.append(energyCount)
    #     return energyCount

    def draw(self):
        for ball in self.balls:
            ball.draw()
        MoveWall.getInstance().draw()

    def writeFile(self, file: TextIO):
        for i, ball in enumerate(self.balls):
            # ballInit: i x y theta radius color
            file.write(
                ballInitFlag + inLineDelimiter + str(i) + inLineDelimiter + str(ball.x) + inLineDelimiter + str(
                    ball.y) + inLineDelimiter + str(ball.theta) + inLineDelimiter + str(
                    ball.radius) + inLineDelimiter + ball.color + inLineDelimiter + '\n')
        lines = MoveWall.getInstance().lines
        for i, line in enumerate(lines):
            # wallInit: i x1 y1 x2 y2
            file.write(
                wallInitFlag + inLineDelimiter + str(i) + inLineDelimiter + str(line.x1) + inLineDelimiter + str(
                    line.y1) + inLineDelimiter + str(line.x2) + inLineDelimiter + str(line.y2) + inLineDelimiter + '\n')
        file.write(nextStepFlag + inLineDelimiter + '\n')
        self.pairs = self.hashTable.getPairs(self.balls)

    def printPairs(self):
        for pair in self.pairs:
            print(pair.i.number, pair.j.number)
        print('==========================================')

    def move(self):
        self.calculation()
        # self.energy()
        # self.step += 1
        # stepCount.append(self.step)
        MoveWall.getInstance().move()
        for ball in self.balls:
            ball.move()

    def calculation(self):
        # В случае касания шара с шаром или шара со стенкой -- отключается для этого шара поле ускорений
        # Дело в том что если этого не делать ускорение продавит шар за пределы стенки в какой-то момент,
        # а именно в тот момент, когда шары должны находиться в состоянии равновесия.
        # Это особенность только аналитического метода
        self.setAcceleration()

        # В случае столкновения шаров друг с другом решается задача о нецентральном неупругом ударе
        for pair in self.pairs:
            i = pair.i.number
            j = pair.j.number
            if isCross(self.balls[i], self.balls[j]):
                method(self.balls[i], self.balls[j])

    def setAcceleration(self):
        for ball in self.balls:
            ball.isCrossAnything = ball.crossPolygon()

        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if distanceNow(self.balls[i], self.balls[j]) < (self.balls[i].radius + self.balls[j].radius):
                    self.balls[i].isCrossAnything = True
                    self.balls[j].isCrossAnything = True

        for ball in self.balls:
            ball.setAcceleration()
