from Ball import *
from math import *
class Elements:
    def __init__(self, balls, canvas, n):
        self.balls = balls
        self.n = n
        self.starts = False
        self.started = False
        self.canvas = canvas
        self.canvas.bind_all('<KeyPress-s>', self.start)  # s - начало движения
        self.canvas.bind_all('<KeyPress-e>', self.exit)  # e - конец движения

    def reset(self, balls, n): # проверяем столкнулись ли шары
        i=0
        while balls[i] == 0:
            if self.move():
                #угол между линией удара и вектором скорости первого шара
                fi = atan((-balls[i].y+balls[i+1].y)/(balls[i].x-balls[i+1].x))+balls[i].alphaRadiam

                balls[i].velocityX = ((balls[i].m-balls[i+1].m)*balls[i].velocityAbsolute*cos(fi) - 2*balls[i+1].m*balls[i+1].velocityX)/(balls[i].m+balls[i+1].m)
                balls[i+1].velocityX = (balls[i].m-balls[i+1].m)*balls[i+1].velocityX - 2*balls[i].m*balls[i].velocityAbsolute*cos(fi)
        i+=1

    def move(self, balls, n):
        for i in range(n):
            if ((balls[i].x - balls[i + 1].x) ** 2 + (- balls[i].y + balls[i + 1].y) ** 2) ** (0.5) <= (balls[i].radius + balls[i + 1].radius):
                return True
            return False

    def start(self, event):
        self.started = True

    def exit(self, event):
        self.started = False

    def draw(self, balls, n):
        for i in range(n):
            balls[i].drawPolygon()
