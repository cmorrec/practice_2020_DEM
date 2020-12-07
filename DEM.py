from BallForce import BallForce
from ElementsForce import *

ballStartFileName1Ball = './ball_sets/1_ball.txt'
ballStartFileName2Ball = './ball_sets/2_ball.txt'
ballStartFileName4Ball = './ball_sets/4_ball.txt'
ballStartFileName2PlateVol = './ball_sets/2_plate_volume.txt'
ballStartFileName2PlateDen = './ball_sets/2_plate_density.txt'
ballStartFileName4Plate = './ball_sets/4_plate.txt'
ballStartFileName4PlateCustom = './ball_sets/4_plate_custom.txt'
ballStartFileNameSimple = './ball_sets/balls_start_simple.txt'
ballStartFileNameTest2 = './ball_sets/test2.txt'

coordinatesFileNameCircle = './walls_dynamic/circle.txt'
coordinatesFileNameCylinderBall = './walls_dynamic/cylinder_ball.txt'
coordinatesFileNameCylinderCone = './walls_dynamic/cylinder_cone.txt'
coordinatesFileNamePolygon = './walls_dynamic/polygon.txt'
coordinatesFileNameRhombus = './walls_dynamic/rhombus.txt'
coordinatesFileNameSquare = './walls_dynamic/square.txt'
coordinatesFileNameTrapezoid = './walls_dynamic/trapezoid.txt'
coordinatesFileNameTriangle = './walls_dynamic/triangle.txt'

coordinatesFileName = coordinatesFileNameSquare
ballStartFileName = ballStartFileNameTest2

coordinatesFile = open(coordinatesFileName, 'r')
coordinatesFromFile = []

isFirstLine = True

velocityXWall = float(0)
velocityYWall = float(0)
absXWall = float(0)
absYWall = float(0)

for line in coordinatesFile:
    words = line.split()
    data = []
    if isFirstLine:
        velocityXWall = float(words[0])
        velocityYWall = float(words[1])
        absXWall = float(words[2])
        absYWall = float(words[3])
        isFirstLine = False
    else:
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
mWidth = displayRatio * (max(xCoordinates) - min(xCoordinates) + absXWall)
mHeight = displayRatio * (max(yCoordinates) - min(yCoordinates) + absYWall)

tk = Tk()
tk.title('DEM')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
tk.columnconfigure(0)
tk.columnconfigure(1)
tk.columnconfigure(2)
tk.rowconfigure(0)
tk.rowconfigure(1)
canvas = Canvas(tk, width=int(mWidth), height=int(mHeight), highlightthickness=0)
canvas.grid(row=0, columnspan=3)
buttons = Buttons()
tk.update()

wall = MoveWall(canvas, 'black', np.array(coordinatesFromFile), accelerationX, accelerationY, None, velocityXWall, velocityYWall,
                absXWall, absYWall)

ballsStartFile = open(ballStartFileName, 'r')
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
        if isForce:
            ballsFromFile.append(
                BallForce(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], color, canvas))
        else:
            ballsFromFile.append(
                Ball(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], color, canvas))

ballsStartFile.close()

if isForce:
    elements = ElementsForce(np.array(ballsFromFile), canvas)
else:
    elements = Elements(np.array(ballsFromFile), canvas)

buttons[0].bind('<Button-1>', elements.start)  # Обработчик событий
buttons[0].grid(row=1, column=0,
                padx=3)  # используем метод pack для отображения кнопки - в нём можно задать положение кнопки
buttons[1].grid(row=1, column=1)
buttons[2].bind('<Button-1>', elements.exit)
buttons[2].grid(row=1, column=2, padx=3)
tk.update_idletasks()
tk.update()

steps = 0
elements.begin()
while True:
    # start_time = time.time()
    if elements.started:
        for i in range(step):
            elements.move()
        # print("--- %s seconds ---" % (time.time() - start_time))
    steps += step
    elements.draw()
    tk.update_idletasks()
    tk.update()
    # print("+++ %s seconds +++" % (time.time() - start_time))
