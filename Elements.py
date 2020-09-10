from Ball import *


# Класс Elements содержит в себе массив шаров и координирует их движение между собой,
# в частности отслеживает и регулирует столкновение шаров

# В будущем нужно реализовать  проверку о ненакладывании мячей один на другой

def distanceNow(i, j):
    # Расстояние между двумя шарами в данный момент времени
    return sqrt((i.x - j.x) ** 2 + (i.y - j.y) ** 2)


def distanceNext(i, j):
    # Расстояние между двумя шарами в следующий момент времени
    return sqrt(((i.x + i.velocityX * deltaTime) - (j.x + j.velocityX * deltaTime)) ** 2 + (
            (i.y + i.velocityY * deltaTime) - (j.y + j.velocityY * deltaTime)) ** 2)


def isCross(i, j):
    # проверяем столкнулись ли шары  и если да -- двигаются ли они навстречу друг другу
    if distanceNext(i, j) < distanceNow(i, j) < (i.radius + j.radius):
        return True
    return False


def rotation(i, j, velocity1YLocal, velocity2YLocal):
    velocityThetaI = i.velocityTheta
    velocityThetaJ = j.velocityTheta

    i.velocityTheta += (1 / (i.mass * i.radius)) * (1 - i.cs) * (
            velocity1YLocal - velocity2YLocal - (velocityThetaI * i.radius + velocityThetaJ * j.radius)) * (
                               deltaTime ** 2)
    j.velocityTheta += (1 / (j.mass * j.radius)) * (1 - j.cs) * (
            velocity2YLocal - velocity1YLocal - (velocityThetaI * i.radius + velocityThetaJ * j.radius)) * (
                               deltaTime ** 2)


def method(i, j):
    # Решение задачи о нецентральном упругом ударе двух дисков, путём приведения к задаче о
    # столкновении шаров по оси Х(линия столкновения становится горизонтальной, происходит
    # переход в локальную систему координат)
    # Также учет диссипации при каждом столкновении шаров

    # Угол между линией удара и горизонталью
    gamma = atan2((i.y - j.y), (i.x - j.x))
    # Углы направления шаров в локальной системе координат
    alphaRadian1Local = i.alphaRadian - gamma
    alphaRadian2Local = j.alphaRadian - gamma
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
    # Учет демпфирования
    velocity1XLocalNew = dampeningVelocity(dampeningNormalI, velocity1XLocalNew)
    velocity2XLocalNew = dampeningVelocity(dampeningNormalJ, velocity2XLocalNew)
    velocity1YLocal = dampeningVelocity(dampeningTangentI, velocity1YLocal)
    velocity2YLocal = dampeningVelocity(dampeningTangentJ, velocity2YLocal)
    # Задание новой угловой скорости дисков
    rotation(i, j, velocity1YLocal, velocity2YLocal)
    # Возвращение к глобальной системе координат
    newAlphaI = atan2(velocity1YLocal, velocity1XLocalNew + eps) + gamma
    newAlphaJ = atan2(velocity2YLocal, velocity2XLocalNew + eps) + gamma
    newVelocityAbsoluteI = sqrt(velocity1XLocalNew ** 2 + velocity1YLocal ** 2)
    newVelocityAbsoluteJ = sqrt(velocity2XLocalNew ** 2 + velocity2YLocal ** 2)
    # Задание нового вектора скорости
    i.changeVelocity(newAlphaI, newVelocityAbsoluteI)
    j.changeVelocity(newAlphaJ, newVelocityAbsoluteJ)


def methodForce(i, j):
    # Решение задачи о нецентральном упругом ударе двух дисков, путём приведения к задаче о
    # столкновении шаров по оси Х(линия столкновения становится горизонтальной, происходит
    # переход в локальную систему координат)
    # Также учет диссипации при каждом столкновении шаров

    # Угол между линией удара и горизонталью
    gamma = atan2((i.y - j.y), (i.x - j.x))
    # Углы направления шаров в локальной системе координат
    alphaRadian1Local = i.alphaRadian - gamma
    alphaRadian2Local = j.alphaRadian - gamma
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
    # Учет демпфирования
    velocity1XLocalNew = dampeningVelocity(dampeningNormalI, velocity1XLocalNew)
    velocity2XLocalNew = dampeningVelocity(dampeningNormalJ, velocity2XLocalNew)
    velocity1YLocal = dampeningVelocity(dampeningTangentI, velocity1YLocal)
    velocity2YLocal = dampeningVelocity(dampeningTangentJ, velocity2YLocal)
    # Задание новой угловой скорости дисков
    rotation(i, j, velocity1YLocal, velocity2YLocal)
    # Возвращение к глобальной системе координат
    newAlphaI = atan2(velocity1YLocal, velocity1XLocalNew + eps) + gamma
    newAlphaJ = atan2(velocity2YLocal, velocity2XLocalNew + eps) + gamma
    newVelocityAbsoluteI = sqrt(velocity1XLocalNew ** 2 + velocity1YLocal ** 2)
    newVelocityAbsoluteJ = sqrt(velocity2XLocalNew ** 2 + velocity2YLocal ** 2)
    # Задание нового вектора скорости
    i.changeVelocity(newAlphaI, newVelocityAbsoluteI)
    j.changeVelocity(newAlphaJ, newVelocityAbsoluteJ)


class Elements:
    def __init__(self, balls, canvas):
        self.balls = balls
        self.starts = False
        self.started = False
        self.canvas = canvas
        self.startEnergy = self.energy()

    def stopIfLowEnergy(self):
        if (self.energy() < self.startEnergy * 0.004) and (
                not MoveWall.getInstance().flagMove or MoveWall.getInstance().velocityAbsolute < eps):
            self.started = False
            saveResults(self)
            self.energyMonitoring()

    def energyMonitoring(self):
        print("Количество энергии", self.energy(), "\n")
        # if self.energy() < eps:
        #     self.starts = True

    def start(self, event):
        self.started = True
        self.energyMonitoring()

    def exit(self, event):
        self.started = False
        saveResults(self)
        self.energyMonitoring()

    def energy(self):
        energyCount = self.energyKinetic() + self.energyPotential()
        return energyCount

    def energyKinetic(self):
        energyCount = 0
        for ball in self.balls:
            energyCount += 0.5 * ball.mass * (ball.velocityAbsolute ** 2) + 0.5 * ball.momentInertial * (
                        ball.velocityTheta ** 2)
        print('kinetic', energyCount)
        return energyCount

    def energyPotential(self):
        energyCount = 0
        for ball in self.balls:
            energyCount += ball.mass * MoveWall.getInstance().accelerationY * (MoveWall.getInstance().maxY - ball.y)
        print('potential', energyCount)
        return energyCount

    def draw(self):
        # self.stopIfLowEnergy()
        self.move()
        MoveWall.getInstance().move()
        for ball in self.balls:
            ball.drawPolygon()
            ball.rotationIndicator()

    def move(self):
        # В случае столкновения шаров друг с другом решается задача о нецентральном упругом ударе
        self.setAcceleration()

        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
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
