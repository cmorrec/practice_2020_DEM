from math import *
import numpy as np
import time
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from PIL import ImageTk

displayRatio = 1000
midInteractionNum = 1000


def getForceDamping(c):
    return 1 - (1 - c) ** (1 / midInteractionNum)


isForce = True
# Класс GlobalUtils будет хранить в себе все сторонние библиотеки и константы
epsVelocity = 0.01
epsAcceleration = 0.01
eps = 1e-11
inf = 1e11
# Критически малая величина, необходимая для сравнения вещественных чисел

step = 100
deltaTime = 1 * 1e-5
# Шаг по времени
cn_wall = 0.1
cs_wall = 0.1
if isForce:
    cn_wall = getForceDamping(cn_wall)
    cs_wall = getForceDamping(cs_wall)

coefficientOfFrictionSliding = 0.1 * deltaTime / 5
coefficientOfFrictionRolling = 0.1 * deltaTime / 10

# коэффициенты демпфирования для стенок
accelerationX = 0
accelerationY = 0
kn = 2 * 1e5
ks = 0
# Энергия
kineticPlot = []
potentialPlot = []
summaryPlot = []
wallInteraction = []
ballInteraction = []
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


def saveInteraction():
    linesEndFile = ['middle num of interaction = ' + str(midInteractionNum)]
    if len(wallInteraction) > 0:
        linesEndFile.append(
            'wall\tmin = ' + str(min(wallInteraction)) + '\tmax = ' + str(max(wallInteraction)) + '\tmiddle = ' + str(
                round(sum(wallInteraction) / len(wallInteraction), 1)) + '\tlen = ' + str(len(wallInteraction)))
    if len(ballInteraction) > 0:
        linesEndFile.append(
            'ball\tmin = ' + str(min(ballInteraction)) + '\tmax = ' + str(max(ballInteraction)) + '\tmiddle = ' + str(
                round(sum(ballInteraction) / len(ballInteraction), 1)) + '\tlen = ' + str(len(ballInteraction)))
    if len(wallInteraction) > 0 and len(ballInteraction) > 0:
        linesEndFile.append('all \tmin = ' + str(min(min(wallInteraction), min(ballInteraction))) + '\tmax = ' + str(
            max(max(wallInteraction), max(ballInteraction))) + '\tmiddle = ' + str(
            round((sum(ballInteraction) + sum(wallInteraction)) / (len(ballInteraction) + len(wallInteraction)),
                  1)) + '\tlen = ' + str(len(ballInteraction) + len(wallInteraction)))
    ballsInteractionFile = open('balls_end_interaction.txt', 'w')
    for line in linesEndFile:
        ballsInteractionFile.write(line + '\n')
    ballsInteractionFile.close()


def saveResults(elements):
    # Запись результатов в файл
    if isForce:
        saveInteraction()
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
    ax.yaxis.set_major_locator(ticker.MultipleLocator((summaryPlot[-1]) * (stepCount[-1] // 10 * 10)))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator((summaryPlot[-1]) * (stepCount[-1] // 10 * 20)))
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
    ax.set_ylabel('Energy, J')
    ax.set_xlabel('Steps')
    # ax.set_xlim(xmin=nrg[0], xmax=nrg[-1])
    fig.tight_layout()

    plt.show()


def dampeningVelocity(dampening, velocity):
    if abs(velocity) - abs(dampening) > 0:
        return velocity - dampening
    else:
        return 0
