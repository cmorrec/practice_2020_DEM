import sys
import time
from math import sin, cos
from tkinter import Tk, Canvas
from GlobalConstants import *

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

utils = file.readline().split(inLineDelimiter)
canvasWidth = float(utils[1])
canvasHeight = float(utils[2])

tk = Tk()
tk.title('DEM')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=int(canvasWidth), height=int(canvasHeight), highlightthickness=0)
canvas.pack()
tk.update()


class CustomBall:
    def __init__(self, number: int, x: float, y: float, theta: float, radius: float, color: str, canvas_):
        self.number = number
        self.x = x
        self.y = y
        self.xLastDraw = x
        self.yLastDraw = y
        self.theta = theta
        self.radius = radius
        self.color = color.rstrip()
        self.canvas = canvas_
        self.id = canvas.create_oval(displayRatio * (x - radius), displayRatio * (y - radius),
                                     displayRatio * (x + radius), displayRatio * (y + radius), fill=color.rstrip())
        self.id2 = canvas.create_line(displayRatio * x, displayRatio * y, displayRatio * (x + radius * cos(self.theta)),
                                      displayRatio * (y + radius * sin(self.theta)), width=2, fill="black")

    def setCoordinate(self, x: float, y: float, theta: float):
        self.x = x
        self.y = y
        self.theta = theta

    def remove(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.id2)


class CustomLine:
    def __init__(self, number: int, x1: float, y1: float, x2: float, y2: float, canvas_):
        self.number = number
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.canvas = canvas_
        self.id = canvas.create_line(displayRatio * x1, displayRatio * y1, displayRatio * x2, displayRatio * y2,
                                     fill='black')

    def setCoordinate(self, x1: float, y1: float, x2: float, y2: float):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def remove(self):
        self.canvas.delete(self.id)


balls = []
lines = []


def remove(_balls: list, _lines: list):
    tk.update_idletasks()
    tk.update()
    for ball in _balls:
        ball.remove()
    for line in _lines:
        line.remove()


input()

start_time = time.time()
while True:
    newLine = file.readline().split(inLineDelimiter)
    if newLine[0] == ballInitFlag:
        # ball: i x y theta radius color
        balls.append(
            CustomBall(int(newLine[1]), float(newLine[2]), float(newLine[3]), float(newLine[4]), float(newLine[5]),
                       newLine[6], canvas))
    elif newLine[0] == wallInitFlag:
        # wall: i x1 y1 x2 y2
        lines.append(
            CustomLine(int(newLine[1]), float(newLine[2]), float(newLine[3]), float(newLine[4]), float(newLine[5]),
                       canvas))
    elif newLine[0] == nextStepFlag:
        remove(balls, lines)
        balls.clear()
        lines.clear()
#        time.sleep(0.1)
    elif newLine[0] == utilsFlag:
        pass
    elif newLine[0] == endFileFlag or newLine[0] == '':
        break

print("+++ %s seconds +++" % (time.time() - start_time))
input()
