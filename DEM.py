from tkinter import *
from Ball import *
import time

mWidth = 500
mHeight = 500

x = 70
print("Координата х шара в начальный момент времени: ", x)
y = 50
print("Координата y шара в начальный момент времени: ", y)
velocity = 10
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

ball = Ball(x, y, canvas, 'red', radius, alpha, velocity)
while not ball.starts:
    if ball.started:
        ball.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.1)
