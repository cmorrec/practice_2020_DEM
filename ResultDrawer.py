import sys
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
        self.color = color
        self.canvas = canvas_
        self.id = canvas.create_oval(displayRatio * (x - radius), displayRatio * (y - radius),
                                     displayRatio * (x + radius), displayRatio * (y + radius), fill=color)
        self.id2 = canvas.create_line(displayRatio * x, displayRatio * y, displayRatio * (x + radius * cos(self.theta)),
                                      displayRatio * (y + radius * sin(self.theta)), width=2, fill="black")

    def setCoordinate(self, x: float, y: float, theta: float):
        self.x = x
        self.y = y
        self.theta = theta

    def draw(self):
        self.canvas.move(self.id, displayRatio * (self.x - self.xLastDraw), displayRatio * (self.y - self.yLastDraw))
        self.canvas.coords(self.id2, displayRatio * self.x, displayRatio * self.y,
                           displayRatio * (self.x + self.radius * cos(self.theta)),
                           displayRatio * (self.y + self.radius * sin(self.theta)))
        self.xLastDraw = self.x
        self.yLastDraw = self.y


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

    def draw(self):
        self.canvas.coords(self.id,
                           displayRatio * self.x1,
                           displayRatio * self.y1,
                           displayRatio * self.x2,
                           displayRatio * self.y2)


balls = []
lines = []


def draw(_balls: list, _lines: list):
    for ball in _balls:
        ball.draw()
    for line in _lines:
        line.draw()
    tk.update_idletasks()
    tk.update()


while True:
    newLine = file.readline().split(inLineDelimiter)
    if newLine[0] == ballFlag:
        # ball: i x y theta
        balls[int(newLine[1])].setCoordinate(float(newLine[2]), float(newLine[3]), float(newLine[4]))
    elif newLine[0] == wallFlag:
        # wall: i x1 y1 x2 y2
        lines[int(newLine[1])].setCoordinate(float(newLine[2]), float(newLine[3]), float(newLine[4]), float(newLine[5]))
    elif newLine[0] == nextStepFlag:
        draw(balls, lines)
    elif newLine[0] == ballInitFlag:
        # ballInit: i x y theta radius color
        balls.append(
            CustomBall(int(newLine[1]), float(newLine[2]), float(newLine[3]), float(newLine[4]), float(newLine[5]),
                       newLine[6], canvas))
    elif newLine[0] == wallInitFlag:
        # wallInit: i x1 y1 x2 y2
        lines.append(
            CustomLine(int(newLine[1]), float(newLine[2]), float(newLine[3]), float(newLine[4]), float(newLine[5]),
                       canvas))
    elif newLine[0] == utilsFlag:
        pass
    elif newLine[0] == endFileFlag or newLine[0] == '':
        break

print('I`m draw this!!!!')
input()
