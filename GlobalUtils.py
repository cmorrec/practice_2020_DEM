from math import *
import numpy as np
import time
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from PIL import ImageTk

displayRatio = 1000
midInteractionNum = 600


def getForceDamping(c):
    return 1 - (1 - c) ** (1 / midInteractionNum)


isForce = True
# Класс GlobalUtils будет хранить в себе все сторонние библиотеки и константы
epsVelocity = 10
epsAcceleration = 0.1
eps = 1e-11
inf = 1e11
# Критически малая величина, необходимая для сравнения вещественных чисел

frequency = 0.01  # Это частота приятная глазу, ее лучше не менять
deltaTime = 0.0001  # Не может быть больше чем frequency
# Шаг по времени
cn_wall = 0.01
cs_wall = 0.01
if isForce:
    cn_wall = getForceDamping(cn_wall)
    cs_wall = getForceDamping(cs_wall)

# коэффициенты демпфирования для стенок
accelerationX = 0
accelerationY = 9.81
kn = 2 * 1e4
ks = 1
# Энергия
kineticPlot = []
potentialPlot = []
summaryPlot = []
stepCount = [0]


def Buttons():
    but_1 = Button(text='Start',
                   width=17, height=2,
                   bg='#5195fc', fg='white',
                   activebackground='#77DDE7',  # цвет нажатой кнопки
                   activeforeground='#FF2400',  # цвет надписи когда кнопка нажата
                   font='Hack 16')  # шрифт и размер надписи
    folderImage = ImageTk.PhotoImage(file="folder.png")
    but_2 = Button(image=folderImage)
    but_3 = Button(text='Stop',
                   width=17, height=2,
                   bg='#fc5151', fg='white',
                   activebackground='#77DDE7',
                   activeforeground='#FF2400',
                   font='Hack 16')
    buttons = [but_1, but_2, but_3]
    return buttons


def saveResults(elements):
    # Запись результатов в файл
    ballsEndFile = open('balls_end.txt', 'w')
    linesEndFile = ['\t\tx\t\t\t\t\ty\t\tradius\t\talpha\t\t\tvelocity\t\tacceleration']
    for ball in elements.balls:
        linesEndFile.append(
            str(ball.x) + ' ' + str(ball.y) + ' ' + str(ball.radius) + ' ' + str(ball.getAlpha()) + ' ' + str(
                ball.velocityAbsolute) + ' ' + str(ball.getAcceleration()))
    for line in linesEndFile:
        ballsEndFile.write(line + '\n')
    ballsEndFile.close()


def plotter():
    plt.style.use('fivethirtyeight')
    fig = plt.figure(figsize=(8, 8))
    ax = plt.subplot(111)
    ax.plot(stepCount, kineticPlot, label='Кинетическая')
    ax.plot(stepCount, potentialPlot, label='Потенциальная')
    ax.plot(stepCount, summaryPlot, label='Суммарная')
    ax.set_title('')
    chartBox = ax.get_position()
    ax.set_position([chartBox.x0, chartBox.y0, chartBox.width * 0.7, chartBox.height])
    ax.legend(loc='upper right', bbox_to_anchor=(0.9, 0.8))
    ax.xaxis.set_major_locator(ticker.MultipleLocator((stepCount[-1] // 100) * 10))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator((stepCount[-1] // 100) * 2))
    ax.yaxis.set_major_locator(ticker.MultipleLocator((summaryPlot[-1] // 100) * (stepCount[-1] // 100 * 10)))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator((summaryPlot[-1] // 100) * (stepCount[-1] // 100 * 20)))
    ax.tick_params(axis='both',
                   which='major',
                   direction='inout',
                   length=20,
                   width=2,
                   color='#e54747',
                   pad=10,
                   labelsize=10,
                   labelcolor='#000',
                   bottom=True,
                   top=True,
                   left=True,
                   right=True,
                   labelbottom=True,
                   labeltop=True,
                   labelleft=True,
                   labelright=True,
                   labelrotation=70)

    ax.tick_params(axis='both',
                   which='minor',
                   direction='out',
                   length=10,
                   width=1,
                   color='#e54747',
                   pad=10,
                   labelsize=15,
                   labelcolor='#000',
                   bottom=True,
                   top=True,
                   left=True,
                   right=True)
    ax.grid(which='major',
            color='k')
    ax.minorticks_on()
    ax.grid(which='minor',
            color='gray',
            linestyle=':')
    ax.set_ylabel('Energy, 10e5 J')
    ax.set_xlabel('Steps')
    # ax.set_xlim(xmin=nrg[0], xmax=nrg[-1])
    fig.tight_layout()

    plt.show()


def dampeningVelocity(dampening, velocity):
    if abs(velocity) - abs(dampening) > 0:
        return velocity - dampening
    else:
        return 0
