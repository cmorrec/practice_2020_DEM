from Ball import *
from Coordinate import *
from Wall import *
from Elements import *

mWidth = 500
mHeight = 500

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
ballStartFile = open('balls_start.txt', 'r')
ballEndFile = open('balls_end.txt', 'w')

coordinatesFromFile = []
linesFromFile = []
i = 0

for line in coordinatesFile:
    words = line.split()
    data = []
    for word in words:
        if i == 0:
            mWidth = int(word)
        elif i == 1:
            mHeight = int(word)
        else:
            data.append(int(word))
        i += 1
    if len(data) > 0:
        coordinatesFromFile.append(Coordinate(data[0], data[1]))

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
# coordinate3 = Coordinate(mWidth, mHeight - 50)
# coordinate4 = Coordinate(0, mHeight - 50)

coordinates = np.array([coordinate1, coordinate2, coordinate3, coordinate3])

line1 = Line(coordinate1, coordinate2)
line2 = Line(coordinate2, coordinate3)
line3 = Line(coordinate3, coordinate4)
line4 = Line(coordinate4, coordinate1)
lines = np.array([line1, line2, line3, line4])

wall = Wall(canvas, 'black', coordinatesFromFile)
ball1 = Ball(x, y, canvas, 'red', radius + 10, alpha, velocity + 3, wall)
ball2 = Ball(x + 80, y, canvas, 'green', radius, 2 * alpha, velocity - 3, wall)
ball3 = Ball(x - 80, y, canvas, 'blue', radius - 10, -alpha, velocity, wall)
balls = np.array([ball1, ball2, ball3])
elements = Elements(balls, canvas)
while not elements.starts:
    if elements.started:
        elements.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.05)
