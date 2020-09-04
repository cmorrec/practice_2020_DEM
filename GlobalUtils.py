from math import *
import numpy as np
import time
from tkinter import *

# Класс GlobalUtils будет хранить в себе все сторонние библиотеки и константы

eps = 1e-5
# Критически малая величина, необходимая для сравнения вещественных чисел

deltaTime = 0.01
deltaTimeDraw = 1e-7
# Шаг по времени
cn_wall = 0.1
cs_wall = 0.2
# коэффициенты демпфирования для стенок
accelerationX = 0
accelerationY = 2
kn = 1 * 1e5
ks = 1 * 1e2


def saveResults(elements):
    # Запись результатов в файл
    ballsEndFile = open('balls_end.txt', 'w')
    linesEndFile = ['x\t\t\t\t\t\t\ty\t\tradius\t\talpha\t\t\tvelocity\t\tacceleration']
    for ball in elements.balls:
        linesEndFile.append(
            str(ball.x) + ' ' + str(ball.y) + ' ' + str(ball.radius) + ' ' + str(ball.getAlpha()) + ' ' + str(
                ball.velocityAbsolute) + ' ' + str(ball.getAcceleration()))
    for line in linesEndFile:
        ballsEndFile.write(line + '\n')
    ballsEndFile.close()


def dampeningVelocity(dampening, velocity):
    if abs(velocity) - abs(dampening) > 0:
        return velocity - dampening
    else:
        return 0
