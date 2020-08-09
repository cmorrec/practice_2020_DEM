from Ball import *


# Класс Elements содержит в себе массив шаров и координирует их движение между собой,
# в частности отслеживает и регулирует столкновение шаров

# В будущем нужно реализовать  проверку о ненакладывании мячей один на другой


class Elements:
    def __init__(self, balls, canvas):
        self.balls = balls
        self.ballsCrossing = []
        for i in range(len(balls)):
            self.ballsCrossing.append(False)
        self.starts = False
        self.started = False
        self.canvas = canvas
        self.canvas.bind_all('<KeyPress-s>', self.start)  # s - начало движения
        self.canvas.bind_all('<KeyPress-e>', self.exit)  # e - конец движения

    def energyMonitoring(self):
        print("Количество энергии", self.energy(), "\n")
        if self.energy() < eps:
            self.starts = True

    def start(self, event):
        self.started = True
        self.energyMonitoring()

    def exit(self, event):
        self.started = False
        saveResults(self)
        self.energyMonitoring()

    def energy(self):
        energyCount = 0
        for ball in self.balls:
            energyCount += ball.mass * (ball.velocityAbsolute ** 2)
        return energyCount

    def draw(self):
        self.move()
        for ball in self.balls:
            ball.drawPolygon()
            ball.rotationIndicator()

    def move(self):
        # В случае столкновения шаров друг с другом решается задача о нецентральном упругом ударе
        self.setAcceleration()

        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if self.isCross(i, j):
                    self.method(i, j)

    def setAcceleration(self):
        for ball in self.balls:
            ball.isCrossAnything = ball.crossPolygon()

        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if self.distanceNow(i, j) < (self.balls[i].radius + self.balls[j].radius):
                    self.balls[i].isCrossAnything = True
                    self.balls[j].isCrossAnything = True

        for ball in self.balls:
            ball.setAcceleration()

    def isCross(self, i, j):
        # проверяем столкнулись ли шары  и если да -- двигаются ли они навстречу друг другу
        if self.distanceNext(i, j) < self.distanceNow(i, j) < (self.balls[i].radius + self.balls[j].radius):
            return True
        return False

    def distanceNow(self, i, j):
        # Расстояние между двумя шарами в данный момент времени
        return sqrt((self.balls[i].x - self.balls[j].x) ** 2 + (self.balls[i].y - self.balls[j].y) ** 2)

    def distanceNext(self, i, j):
        # Расстояние между двумя шарами в следующий момент времени
        return sqrt(((self.balls[i].x + self.balls[i].velocityX) - (self.balls[j].x + self.balls[j].velocityX)) ** 2 + (
                (self.balls[i].y + self.balls[i].velocityY) - (self.balls[j].y + self.balls[j].velocityY)) ** 2)

    def rotation(self, i, j, velocity1YLocal, velocity2YLocal):
        self.balls[i].velocityTheta -= (self.balls[j].mass / (self.balls[i].mass * self.balls[i].radius)) * (
                1 - self.balls[i].cs) * (velocity1YLocal - velocity2YLocal - (
                self.balls[i].velocityTheta * self.balls[i].radius + self.balls[j].velocityTheta * self.balls[
            j].radius))
        self.balls[j].velocityTheta -= (self.balls[i].mass / (self.balls[j].mass * self.balls[j].radius)) * (
                1 - self.balls[j].cs) * (velocity1YLocal - velocity2YLocal - (
                self.balls[i].velocityTheta * self.balls[i].radius + self.balls[j].velocityTheta * self.balls[
            j].radius))

    def method(self, i, j):
        # Решение задачи о нецентральном упругом ударе двух дисков, путём приведения к задаче о
        # столкновении шаров по оси Х(линия столкновения становится горизонтальной, происходит
        # переход в локальную систему координат)
        # Также учет диссипации при каждом столкновении шаров

        # Угол между линией удара и горизонталью
        gamma = atan2((self.balls[i].y - self.balls[j].y), (self.balls[i].x - self.balls[j].x))
        # Углы направления шаров в локальной системе координат
        alphaRadian1Local = self.balls[i].alphaRadian - gamma
        alphaRadian2Local = self.balls[j].alphaRadian - gamma
        # Скорости шаров в локальной системе координат
        velocity1XLocal = self.balls[i].velocityAbsolute * cos(alphaRadian1Local)
        velocity1YLocal = self.balls[i].velocityAbsolute * sin(alphaRadian1Local)
        velocity2XLocal = self.balls[j].velocityAbsolute * cos(alphaRadian2Local)
        velocity2YLocal = self.balls[j].velocityAbsolute * sin(alphaRadian2Local)
        # Относительная скорость и демпфирование
        dampeningNormal = (abs(velocity1XLocal - velocity2XLocal)) * self.balls[i].cn
        dampeningTangent = (abs(velocity1YLocal - velocity2YLocal) - (
                self.balls[i].velocityTheta * self.balls[i].radius + self.balls[j].velocityTheta * self.balls[
            j].radius)) * self.balls[i].cs

        # Непосредственно решение задачи о нецентральном упругом ударе двух дисков, задание новой угловой скорости дисков
        velocity1XLocalNew = ((self.balls[i].mass - self.balls[j].mass) * velocity1XLocal + 2 * self.balls[
            j].mass * velocity2XLocal) / (self.balls[i].mass + self.balls[j].mass)
        velocity2XLocalNew = (2 * self.balls[i].mass * velocity1XLocal + (
                self.balls[j].mass - self.balls[i].mass) * velocity2XLocal) / (
                                     self.balls[i].mass + self.balls[j].mass)
        self.rotation(i, j, velocity1YLocal, velocity2YLocal)
        # Учет демпфирования
        if abs(velocity1XLocalNew) - dampeningNormal > 0:
            velocity1XLocalNew = (abs(velocity1XLocalNew) - dampeningNormal) * velocity1XLocalNew / abs(
                velocity1XLocalNew)
        else:
            velocity1XLocalNew = 0
        if abs(velocity2XLocalNew) - dampeningNormal > 0:
            velocity2XLocalNew = (abs(velocity2XLocalNew) - dampeningNormal) * velocity2XLocalNew / abs(
                velocity2XLocalNew)
        else:
            velocity2XLocalNew = 0
        # Возвращение к глобальной системе координат
        newAlphaI = atan2(velocity1YLocal, velocity1XLocalNew + eps) + gamma
        newAlphaJ = atan2(velocity2YLocal, velocity2XLocalNew + eps) + gamma
        newVelocityAbsoluteI = sqrt(velocity1XLocalNew ** 2 + velocity1YLocal ** 2)
        newVelocityAbsoluteJ = sqrt(velocity2XLocalNew ** 2 + velocity2YLocal ** 2)
        # Задание нового вектора скорости
        self.balls[i].changeVelocity(newAlphaI, newVelocityAbsoluteI)
        self.balls[j].changeVelocity(newAlphaJ, newVelocityAbsoluteJ)
