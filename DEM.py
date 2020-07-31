from Ball import *
from Wall import *
from Elements import *


n = 3
print("Количество шаров: ", n)
x = 250
print("Дефолтная координата х шара в начальный момент времени: ", x)
y = 250
print("Дефолтная координата y шара в начальный момент времени: ", y)
velocity = 5
print("Дефолтная скорость шара равна: ", velocity)
radius = 25
print("Дефолтный радиус шара равен: ", radius)
alpha = 30
print("Дефолтный поворот вектора скорости относительно горизонтали: ", alpha)

coordinatesFile = open('wall_coordinates.txt', 'r')
coordinatesFromFile = []

for line in coordinatesFile:
    words = line.split()
    data = []
    for word in words:
        data.append(float(word))
    if len(data) > 0:
        coordinatesFromFile.append(Coordinate(data[0], data[1]))

coordinatesFile.close()

xCoordinates = []
yCoordinates = []
for coordinate in coordinatesFromFile:
    xCoordinates.append(coordinate.x)
    yCoordinates.append(coordinate.y)
mWidth = max(xCoordinates) - min(xCoordinates)
mHeight = max(yCoordinates) - min(yCoordinates)

tk = Tk()
tk.title('DEM')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=mWidth, height=mHeight, highlightthickness=0)
canvas.pack()
tk.update()

wall = Wall(canvas, 'black', coordinatesFromFile)

ballsStartFile = open('balls_start.txt', 'r')
ballsFromFile = []

for line in ballsStartFile:
    words = line.split()
    data = []
    j = 0
    color = ''
    for word in words:
        if j != len(words) - 1:
            data.append(float(word))
        else:
            color = word
        j += 1
    if len(data) > 0:
        ballsFromFile.append(Ball(data[0], data[1], data[2], data[3], data[4], data[5], data[6], color, canvas, wall))

ballsStartFile.close()

elements = Elements(ballsFromFile, canvas)
while not elements.starts:
    if elements.started:
        elements.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(deltaTime)

saveResults(elements)
