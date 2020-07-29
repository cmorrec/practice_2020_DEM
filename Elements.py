from GlobalUtils import *


# Класс Elements содержит в себе массив шаров и координирует их движение между собой,
# в частности отслеживает и регулирует столкновение шаров

# В будущем нужно реализовать  проверку о ненакладывании мячей один на другой


class Elements:
    def __init__(self, balls, canvas):
        self.balls = balls
        self.starts = False
        self.started = False
        self.canvas = canvas
        self.canvas.bind_all('<KeyPress-s>', self.start)  # s - начало движения
        self.canvas.bind_all('<KeyPress-e>', self.exit)  # e - конец движения

    def start(self, event):
        self.started = True
        print("Изначальное количество энергии", self.energy(), "\n")

    def exit(self, event):
        self.started = False
        print("Конечное количество энергии", self.energy(), "\n\n")

    def energy(self):
        energyCount = 0
        for ball in self.balls:
            energyCount += ball.mass * (ball.velocityAbsolute ** 2)
        return energyCount

    def draw(self):
        self.move()
        for ball in self.balls:
            ball.drawPolygon()

    def move(self):
        # В случае столкновения шаров друг с другом решается задача о нецентральном упругом ударе
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if self.isCross(i, j):
                    self.method(i, j)

    def isCross(self, i, j):
        # проверяем столкнулись ли шары  и если да -- двигаются ли они навстречу друг другу
        if sqrt((self.balls[i].x - self.balls[j].x) ** 2 + (self.balls[i].y - self.balls[j].y) ** 2) < (
                self.balls[i].radius + self.balls[j].radius):
            if self.distanceNow(i, j) > self.distanceNext(i, j):
                return True
        return False

    def distanceNow(self, i, j):
        # Расстояние между двумя шарами в данный момент времени
        return sqrt((self.balls[i].x - self.balls[j].x) ** 2 + (self.balls[i].y - self.balls[j].y) ** 2)

    def distanceNext(self, i, j):
        # Расстояние между двумя шарами в следующий момент времени
        return sqrt(((self.balls[i].x + self.balls[i].velocityX) - (self.balls[j].x + self.balls[j].velocityX)) ** 2 + (
                (self.balls[i].y + self.balls[i].velocityY) - (self.balls[j].y + self.balls[j].velocityY)) ** 2)

    def method(self, i, j):
        # Решение задачи о нецентральном упругом ударе двух дисков, путём приведения к задаче о
        # столкновении шаров по оси Х(линия столкновения становится горизонтальной, происходит
        # переход в локальную систему координат)

        # Угол между линией удара и горизонталью
        gamma = atan2((self.balls[i].y - self.balls[j].y), (self.balls[i].x - self.balls[j].x))
        # Углы направления шаров в локальной системе координат
        alphaRadian_1_tmp = self.balls[i].alphaRadian - gamma
        alphaRadian_2_tmp = self.balls[j].alphaRadian - gamma
        # Скорости шаров в локальной системе координат
        velocity1XLocal = self.balls[i].velocityAbsolute * cos(alphaRadian_1_tmp)
        velocity1YLocal = self.balls[i].velocityAbsolute * sin(alphaRadian_1_tmp)
        velocity2XLocal = self.balls[j].velocityAbsolute * cos(alphaRadian_2_tmp)
        velocity2YLocal = self.balls[j].velocityAbsolute * sin(alphaRadian_2_tmp)

        # Непосредственно решение задачи о нецентральном упругом ударе двух дисков
        velocity1XLocalNew = ((self.balls[i].mass - self.balls[j].mass) * velocity1XLocal + 2 * self.balls[
            j].mass * velocity2XLocal) / (self.balls[i].mass + self.balls[j].mass)
        velocity2XLocalNew = (2 * self.balls[i].mass * velocity1XLocal + (
                self.balls[j].mass - self.balls[i].mass) * velocity2XLocal) / (
                                     self.balls[i].mass + self.balls[j].mass)

        # Возвращение к глобальной системе координат
        newAlphaI = atan2(velocity1YLocal, velocity1XLocalNew + eps) + gamma
        newAlphaJ = atan2(velocity2YLocal, velocity2XLocalNew + eps) + gamma
        newVelocityAbsoluteI = sqrt(velocity1XLocalNew ** 2 + velocity1YLocal ** 2)
        newVelocityAbsoluteJ = sqrt(velocity2XLocalNew ** 2 + velocity2YLocal ** 2)

        # Задание нового вектора скорости
        self.balls[i].changeVelocity(newAlphaI, newVelocityAbsoluteI)
        self.balls[j].changeVelocity(newAlphaJ, newVelocityAbsoluteJ)
