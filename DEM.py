from tkinter import *
from Ball import *
from Coordinate import *
from Line import *
from Wall import *
import numpy as np
import time

mWidth = 500
mHeight = 500

x = 260
print("Координата х шара в начальный момент времени: ", x)
y = 240
print("Координата y шара в начальный момент времени: ", y)
velocity = 15
print("Скорость шара равна: ", velocity)
radius = 20
print("Радиус шара равен: ", radius)
alpha = -30
print("Поворот вектора скорости относительно горизонтали: ", alpha)

tk = Tk()
tk.title('DEM')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=mWidth, height=mHeight, highlightthickness=0)
canvas.pack()
tk.update()

# Класс Wall может принимать в себя любое количество линий(4 - это для примера)
# Для большего количества точек(и соотвественно линий), надо создать их дополнительно и добавить в массив
# При желании посмотреть на другие фигуры раскомментируйте(и закомментируйте) соотвествующие участки кода

# Ромб
coordinate1 = Coordinate(mWidth / 2, 0)
coordinate2 = Coordinate(mWidth, mHeight / 2)
coordinate3 = Coordinate(mWidth / 2, mHeight)
coordinate4 = Coordinate(0, mHeight / 2)

# Прямоугольник
# coordinate1 = Coordinate(0, 0)
# coordinate2 = Coordinate(mWidth, 0)
# coordinate3 = Coordinate(mWidth, mHeight)
# coordinate4 = Coordinate(0, mHeight)

# Трапеция
# coordinate1 = Coordinate(mWidth / 4, 0)
# coordinate2 = Coordinate(3 * mWidth / 4, 0)
# coordinate3 = Coordinate(mWidth, mHeight)
# coordinate4 = Coordinate(0, mHeight)

coordinates = np.array([coordinate1, coordinate2, coordinate3, coordinate3])

line1 = Line(coordinate1.x, coordinate1.y, coordinate2.x, coordinate2.y)
line2 = Line(coordinate2.x, coordinate2.y, coordinate3.x, coordinate3.y)
line3 = Line(coordinate3.x, coordinate3.y, coordinate4.x, coordinate4.y)
line4 = Line(coordinate4.x, coordinate4.y, coordinate1.x, coordinate1.y)
lines = np.array([line1, line2, line3, line4])

wall = Wall(coordinates, lines, canvas, 'black')

ball = Ball(x, y, canvas, 'red', radius, alpha, velocity)

while not ball.starts:
    if ball.started:
        ball.drawPolygon(wall)
    tk.update_idletasks()
    tk.update()
    time.sleep(0.1)