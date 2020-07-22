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
        self.flac = 0

    def method(self, balls, i, j):# приведение к задаче о столкновении шаров(линия столкновения становится горизонтальной)
        # угол между линией удара и горизонталью
        gamma = atan(abs((balls[i].y - balls[j].y)) / abs((balls[i].x - balls[j].x)))
        alphaRadian_2_tmp = balls[j].alphaRadian
        alphaRadian_1_tmp = balls[i].alphaRadian
        Velocity1X_old = balls[i].velocityAbsolute * cos(alphaRadian_1_tmp)
        Velocity1Y = balls[i].velocityAbsolute * sin(alphaRadian_1_tmp)
        Velocity2X_old = balls[j].velocityAbsolute * cos(alphaRadian_2_tmp)
        Velocity2Y = balls[j].velocityAbsolute * sin(alphaRadian_2_tmp)


        Velocity1X_new = ((balls[i].m - balls[j].m) * Velocity1X_old + 2 * balls[j].m *Velocity2X_old) / (balls[i].m + balls[j].m)
        Velocity2X_new = (2 * balls[i].m * Velocity1X_old + (balls[j].m - balls[i].m) * Velocity2X_old) / (balls[i].m + balls[j].m)
        balls[i].alphaRadian = atan(Velocity1Y / Velocity1X_new) + gamma
        balls[j].alphaRadian = atan(Velocity2Y / Velocity2X_new) + gamma
        self.flac +=1

    def move(self, balls): # проверяем столкнулись ли шары
         for i in range(len(balls)):
             for j in range(len(balls)-1, -1, -1):
                 if self.request(balls, i, j):
                     self.method(balls, i, j)



    def request(self, balls, i, j):
            if sqrt((balls[i].x - balls[j].x) ** 2 + (balls[i].y - balls[j].y) ** 2) - (balls[i].radius + balls[j].radius) < eps and not i == j and self.flac == 0:
                self.flac = i
                return True
            self.flac+=1
            if self.flac == 3:
                self.flac = 0
            return False
    def start(self, event):
        self.started = True

    def exit(self, event):
        self.started = False

    def draw(self, balls):
        self.move(balls)
        for i in range(len(balls)):
            balls[i].drawPolygon()
