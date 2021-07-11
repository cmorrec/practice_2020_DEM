import sys
from math import pi
from GlobalConstants import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

if len(sys.argv) > 2:
    print('I can draw only one file at once!')
    exit(1)

if len(sys.argv) < 2:
    print('I need to get file!')
    exit(1)

fileName = sys.argv[1]
try:
    file = open(fileName, 'r')
    file.close()
except FileNotFoundError:
    print('I need real file!')
    exit(1)
file = open(fileName, 'r')

file.readline().split(inLineDelimiter)


wasBallsVolume = 0
wasBallsNum = 0
while True:
    newLine = file.readline().split(inLineDelimiter)
    if newLine[0] == ballInitFlag:
        if newLine[6] != '#4682b4':
            wasBallsNum += 1
            wasBallsVolume += (4 / 3) * pi * (float(newLine[5]) ** 3)
    else:
        break

savedBallsVolume = 0
savedBallsNum = 0
awayBallsVolume = 0
awayBallsNum = 0
flag = False
stepCount=[]
summaryPlot=[]
while True:
    newLine = file.readline().split(inLineDelimiter)
    if newLine[0] == ballInitFlag:
        if flag:
            savedBallsNum = 0
            savedBallsVolume = 0
            flag = False
        if newLine[6] != '#4682b4':
            savedBallsNum += 1
            savedBallsVolume += (4 / 3) * pi * (float(newLine[5]) ** 3)
    elif newLine[0] == wallInitFlag:
        flag = True
    elif newLine[0] == utilsFlag:
        awayBallsNum += 1
        awayBallsVolume += (4 / 3) * pi * (float(newLine[1]) ** 3)
    elif newLine[0] == strangeFlag:
        stepCount.append(float(newLine[3]))
        deadMass = float(newLine[0])
        saveMass = float(newLine[1])
        summaryPlot.append(deadMass / (deadMass + saveMass))
    elif newLine[0] == endFileFlag or newLine[0] == '':
        break

print('было', wasBallsVolume, wasBallsNum)
print('просеяно', awayBallsVolume, awayBallsNum)
print('осталось', savedBallsVolume, savedBallsNum)
print('эффективность', awayBallsVolume / (awayBallsVolume + savedBallsVolume))


plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(8, 8))
ax = plt.subplot(111)
ax.plot(stepCount, summaryPlot)
ax.set_title('')
chartBox = ax.get_position()
ax.set_position([chartBox.x0, chartBox.y0, chartBox.width * 0.7, chartBox.height])
ax.legend(loc='upper right', bbox_to_anchor=(0.9, 0.8))
ax.xaxis.set_major_locator(ticker.MultipleLocator(stepCount[-1] / 10))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(stepCount[-1] / 20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(summaryPlot[-1] * stepCount[-1] / 100))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(summaryPlot[-1] * stepCount[-1] / 200))
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
ax.set_ylabel('Эффективность')
ax.set_xlabel('Угловая скорость, рад/с')
# ax.set_xlim(xmin=nrg[0], xmax=nrg[-1])
fig.tight_layout()

plt.show()