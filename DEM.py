from tkinter import *
from Ball import *
from Coordinate import *
from Line import *
from Wall import *
from Elements import *
import numpy as np
import time
mWidth = 500
mHeight = 500

n = 3
print("Количество шаров: ", n)
x = 250
print("Координата х шара в начальный момент времени: ", x)
y = 250
print("Координата y шара в начальный момент времени: ", y)
velocity = 5
print("Скорость шара равна: ", velocity)
radius = 30
print("Радиус шара равен: ", radius)
alpha = 40
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
# coordinate1 = Coordinate(mWidth / 2, 0)
# coordinate2 = Coordinate(mWidth, mHeight / 2)
# coordinate3 = Coordinate(mWidth / 2, mHeight)
# coordinate4 = Coordinate(0, mHeight / 2)

# Прямоугольник
coordinate1 = Coordinate(0, 0)
coordinate2 = Coordinate(mWidth, 0)
coordinate3 = Coordinate(mWidth, mHeight)
coordinate4 = Coordinate(0, mHeight)

# Трапеция
# coordinate1 = Coordinate(mWidth / 4, 0)
# coordinate2 = Coordinate(3 * mWidth / 4, 0)
# coordinate3 = Coordinate(mWidth, mHeight - 50)
# coordinate4 = Coordinate(0, mHeight - 50)

coordinates = np.array([coordinate1, coordinate2, coordinate3, coordinate3])

line1 = Line(coordinate1.x, coordinate1.y, coordinate2.x, coordinate2.y)
line2 = Line(coordinate2.x, coordinate2.y, coordinate3.x, coordinate3.y)
line3 = Line(coordinate3.x, coordinate3.y, coordinate4.x, coordinate4.y)
line4 = Line(coordinate4.x, coordinate4.y, coordinate1.x, coordinate1.y)
lines = np.array([line1, line2, line3, line4])

wall = Wall(coordinates, lines, canvas, 'black')
ball1 = Ball(x, y, canvas, 'red', radius, alpha, velocity, wall)
ball2 = Ball(x+80, y, canvas, 'green', radius, -alpha, velocity, wall)
ball3 = Ball(x-80, y, canvas, 'blue', radius, -alpha, velocity, wall)
balls = np.array([ball1, ball2, ball3])
elements = Elements(balls, canvas)
while not elements.starts:
    if elements.started:
        elements.draw(balls)
    tk.update_idletasks()
    tk.update()
    time.sleep(0.05)
