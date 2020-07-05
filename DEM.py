from tkinter import *
from typing import List, Any

from Ball import *
import time

from practice_2020_DEM.Ball import Ball

mWidth = 500
mHeight = 500

x = 70
print("Координата х шара в начальный момент времени: ", x)
y = 50
print("Координата y шара в начальный момент времени: ", y)
velocity = 2
print("Скорость шара равна: ", velocity)
radius = 20
print("Радиус шара равен: ", radius)
alpha = 35
print("Поворот вектора скорости относительно горизонтали: ", alpha)

tk = Tk()
tk.title('DEM')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=mWidth, height=mHeight, highlightthickness=0)
canvas.pack()
tk.update()
ball=[]
for i in range(5):
    ball.append(Ball(x+50*i, y+50*i, canvas, 'red', radius, alpha, velocity))
    i+= 1

#while not ball[0].starts:
    #if ball[0].started:
while 1:
    for i in range(5):
        ball[i].draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)