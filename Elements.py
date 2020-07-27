from Ball import *
from math import *

eps = 1e-5


class Elements:
    def __init__(self, balls, canvas):
        self.balls = balls
        self.starts = False
        self.started = False
        self.canvas = canvas
        self.canvas.bind_all('<KeyPress-s>', self.start)  # s - начало движения
        self.canvas.bind_all('<KeyPress-e>', self.exit)  # e - конец движения
        self.summ = 0
        self.velocityXSignPlus = True
        self.velocityYSignPlus = True
        self.distance = 0

    def method(self, i, j):
        # приведение к задаче о столкновении шаров(линия столкновения становится горизонтальной)
        # угол между линией удара и горизонталью
        if not self.balls[i].x == self.balls[j].x:
             gamma = atan((self.balls[i].y - self.balls[j].y) / (self.balls[i].x - self.balls[j].x))
        else:
             gamma = pi/2
        alphaRadian_1_tmp = self.balls[i].alphaRadian
        alphaRadian_2_tmp = self.balls[j].alphaRadian
        velocity1X_old = self.balls[i].velocityAbsolute * cos(alphaRadian_1_tmp)
        velocity1Y = self.balls[i].velocityAbsolute * sin(alphaRadian_1_tmp)
        velocity2X_old = self.balls[j].velocityAbsolute * cos(alphaRadian_2_tmp)
        velocity2Y = self.balls[j].velocityAbsolute * sin(alphaRadian_2_tmp)
        velocity1Y_new = velocity1Y
        velocity2Y_new = velocity2Y
        velocity1X_new = ((self.balls[i].mass - self.balls[j].mass) * velocity1X_old + 2 * self.balls[j].mass *velocity2X_old) / (self.balls[i].mass + self.balls[j].mass)
        velocity2X_new = - (2 * self.balls[i].mass * velocity1X_old + (self.balls[j].mass - self.balls[i].mass) * velocity2X_old) / (self.balls[i].mass + self.balls[j].mass)
        newAlphaI = pi - atan(velocity1Y_new / velocity1X_new) - gamma
        newAlphaJ = atan(velocity2Y_new / velocity2X_new) - gamma
        newVelocityAbsoluteI = sqrt(velocity1X_new**2 + velocity1Y**2)
        newVelocityAbsoluteJ = sqrt(velocity2X_new**2 + velocity2Y**2)
        self.balls[i].changeAlpha(newAlphaI, newVelocityAbsoluteI)
        self.balls[j].changeAlpha(newAlphaJ, newVelocityAbsoluteJ)

    def move(self):  # проверяем столкнулись ли шары
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if self.request(i, j):
                    self.method(i, j)

    def request(self, i, j):
        if sqrt((self.balls[i].x - self.balls[j].x) ** 2 + (self.balls[i].y - self.balls[j].y) ** 2) < (
                self.balls[i].radius + self.balls[j].radius):
            # self.distance = sqrt((self.balls[i].x - self.balls[j].x) ** 2 + (self.balls[i].y - self.balls[j].y) ** 2)
            # if self.balls[i].velocityX > 0:
            #     # проверяем какой знак имеют скорости первого шара. От этого зависит условие сближения/удаления шаров
            #     self.velocityXSignPlus = True
            # self.velocityXSignPlus = False
            # if self.balls[i].velocityY > 0:
            #     self.velocityYSignPlus = True
            # self.velocityYSignPlus = False
            # # Возвращаем True если шары летят навстречу друг другу, в обратном случае False.
            # if self.velocityXSignPlus:
            #     if self.distance < self.distance - (self.balls[i].velocityX - self.balls[j].velocityX) * 0.05:
            #         print('7')
            #         if self.velocityYSignPlus:
            #             if self.distance < self.distance - (self.balls[i].velocityY - self.balls[j].velocityY) * 0.05:
            #                 print('1')
            #                 return False
            #             print('2')
            #             return True
            #         if self.distance < self.distance + (self.balls[i].velocityY - self.balls[j].velocityY) * 0.05:
            #             print("3")
            #             return False
            #         print('4')
            #         return True
            #     print('5')
            #     return True
            # # Если же знак скорости Х отрицательный проделываем остальные проверки заново.
            # if self.distance < self.distance + (self.balls[i].velocityX - self.balls[j].velocityX) * 0.05:
            #     print('6')
            #     if self.velocityYSignPlus:
            #         if self.distance < self.distance - (self.balls[i].velocityY - self.balls[j].velocityY) * 0.05:
            #             print('8')
            #             return False
            #         print("9")
            #         return True
            #     if self.distance < self.distance + (self.balls[i].velocityY - self.balls[j].velocityY) * 0.05:
            #         print('10')
            #         return False
            #     print('11')
            #     return True
            # print('12')
            if self.distanceNow(i, j) >= self.distanceNext(i, j):
                print(i, j, self.distanceNow(i, j), self.distanceNext(i, j), True)
                return True
            print(i, j, self.distanceNow(i, j), self.distanceNext(i, j), False)
        return False

    def distanceNow(self, i, j):
        return sqrt((self.balls[i].x - self.balls[j].x) ** 2 + (self.balls[i].y - self.balls[j].y) ** 2)

    def distanceNext(self, i, j):
        return sqrt(((self.balls[i].x + self.balls[i].velocityX) - (self.balls[j].x + self.balls[j].velocityX)) ** 2 + (
                (self.balls[i].y + self.balls[i].velocityY) - (self.balls[j].y + self.balls[j].velocityY)) ** 2)

    def start(self, event):
        self.started = True

    def exit(self, event):
        self.started = False

    def draw(self):
        self.move()
        for ball in self.balls:
            ball.drawPolygon()
