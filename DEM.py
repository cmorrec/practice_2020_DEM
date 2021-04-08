from ElementsForce import *

ballStartFileName1Ball = './ball_sets/1_ball.txt'
ballStartFileName2Ball = './ball_sets/2_ball.txt'
ballStartFileName4Ball = './ball_sets/4_ball.txt'
ballStartFileName4BallAnother = './ball_sets/4_ball_another.txt'
ballStartFileName2PlateVol = './ball_sets/2_plate_volume.txt'
ballStartFileName2PlateDen = './ball_sets/2_plate_density.txt'
ballStartFileName4Plate = './ball_sets/4_plate.txt'
ballStartFileName4PlateCustom = './ball_sets/4_plate_custom.txt'
ballStartFileNameSimple = './ball_sets/balls_start_simple.txt'
ballStartFileNameBallMill = './ball_sets/mill/ball_mill_60.txt'
ballStartFileNameBallMillBig = './ball_sets/mill/ball_mill_120.txt'
ballStartFileNameVibro1 = './ball_sets/vibro/vibrotest_1.txt'

ballStartFileNameTest1_1 = './ball_sets/tests/ball-ball/tests1/test1_1.txt'
ballStartFileNameTest1_2 = './ball_sets/tests/ball-ball/tests1/test1_2.txt'
ballStartFileNameTest1_3 = './ball_sets/tests/ball-ball/tests1/test1_3.txt'
ballStartFileNameTest1_4 = './ball_sets/tests/ball-ball/tests1/test1_4.txt'

ballStartFileNameTest2_1 = './ball_sets/tests/ball-ball/tests2/test2_1.txt'
ballStartFileNameTest2_2 = './ball_sets/tests/ball-ball/tests2/test2_2.txt'
ballStartFileNameTest2_3 = './ball_sets/tests/ball-ball/tests2/test2_3.txt'
ballStartFileNameTest2_4 = './ball_sets/tests/ball-ball/tests2/test2_4.txt'

ballStartFileNameTest3_1 = './ball_sets/tests/ball-wall/tests3/test3_1.txt'
ballStartFileNameTest3_2 = './ball_sets/tests/ball-wall/tests3/test3_2.txt'
ballStartFileNameTest3_3 = './ball_sets/tests/ball-wall/tests3/test3_3.txt'
ballStartFileNameTest3_4 = './ball_sets/tests/ball-wall/tests3/test3_4.txt'
ballStartFileNameTest3_5 = './ball_sets/tests/ball-wall/tests3/test3_5.txt'

ballStartFileNameTest4_1 = './ball_sets/tests/ball-wall/tests4/test4_1.txt'
ballStartFileNameTest4_2 = './ball_sets/tests/ball-wall/tests4/test4_2.txt'
ballStartFileNameTest4_3 = './ball_sets/tests/ball-wall/tests4/test4_3.txt'
ballStartFileNameTest4_4 = './ball_sets/tests/ball-wall/tests4/test4_4.txt'
ballStartFileNameTest4_5 = './ball_sets/tests/ball-wall/tests4/test4_5.txt'

coordinatesFileNameCircle = './walls_dynamic/circle.txt'
coordinatesFileNameCylinderBall = './walls_dynamic/cylinder_ball.txt'
coordinatesFileNameCylinderCone = './walls_dynamic/cylinder_cone.txt'
coordinatesFileNamePolygon = './walls_dynamic/polygon.txt'
coordinatesFileNameRhombus = './walls_dynamic/rhombus.txt'
coordinatesFileNameSquare = './walls_dynamic/square.txt'
coordinatesFileNameSquareBig = './walls_dynamic/square_big.txt'
coordinatesFileNameTrapezoid = './walls_dynamic/trapezoid.txt'
coordinatesFileNameTriangle = './walls_dynamic/triangle.txt'
coordinatesFileNameMill = './walls_dynamic/wall_mill.txt'
coordinatesFileNameVibroBox = './walls_dynamic/vibro_box.txt'

coordinatesFileName = coordinatesFileNamePolygon
ballStartFileName = ballStartFileName4Ball
oreBallStartFileName = ballStartFileName4BallAnother
coordinatesFile = open(coordinatesFileName, 'r')
coordinatesFromFile = []

isFirstLine = True

freqXWall = float(0)
freqYWall = float(0)
absXWall = float(0)
absYWall = float(0)
velocityThetaWall = float(0)

for line in coordinatesFile:
    words = line.split()
    data = []
    if isFirstLine:
        freqXWall = float(words[0])
        freqYWall = float(words[1])
        absXWall = float(words[2])
        absYWall = float(words[3])
        velocityThetaWall = float(words[4])
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
width = max(xCoordinates) - min(xCoordinates)
height = max(yCoordinates) - min(yCoordinates)
centerX = width / 2 + min(xCoordinates)
centerY = height / 2 + min(yCoordinates)
canvasWidth = displayRatio * (width + absXWall)
canvasHeight = displayRatio * (height + absYWall)

tk = Tk()
tk.title('DEM')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
tk.columnconfigure(0)
tk.columnconfigure(1)
tk.columnconfigure(2)
tk.rowconfigure(0)
tk.rowconfigure(1)
canvas = Canvas(tk, width=int(canvasWidth), height=int(canvasHeight), highlightthickness=0)
canvas.grid(row=0, columnspan=3)
buttons = Buttons()

wall = MoveWall(canvas, 'black', np.array(coordinatesFromFile), accelerationX, accelerationY, None, freqXWall,
                freqYWall, velocityThetaWall, absXWall, absYWall, centerX, centerY, width, height)

oreBallStartFile = open(oreBallStartFileName, 'r')
ballsStartFile = open(ballStartFileName, 'r')
ballsFromFile = []

eventBus = EventBus()


def readBalls(ballsStartFile_: TextIO, isBreakage: bool):
    for line_ in ballsStartFile_:
        words_ = line_.split()
        data_ = []
        j = 0
        color = ''
        for word_ in words_:
            if j != len(words_) - 1:
                data_.append(float(word_))
            else:
                color = word_
            j += 1
        if len(data_) > 0:
            if isBreakage:
                ballsFromFile.append(
                    BreakBall(data_[0], data_[1], data_[2], data_[2], data_[3], data_[4], data_[5], data_[6], data_[7],
                              data_[8], data_[9], data_[10], color, canvas, eventBus))
            else:
                if isForce:
                    ballsFromFile.append(
                        BallForce(data_[0], data_[1], data_[2], data_[3], data_[4], data_[5], data_[6], data_[7],
                                  data_[8], data_[9],
                                  data_[10], color,
                                  canvas))
                else:
                    ballsFromFile.append(
                        Ball(data_[0], data_[1], data_[2], data_[3], data_[4], data_[5], data_[6], data_[7], data_[8],
                             data_[9], data_[10],
                             color, canvas))
    ballsStartFile_.close()


readBalls(ballsStartFile, False)
readBalls(oreBallStartFile, True)

if isForce:
    elements = ElementsForce(ballsFromFile, canvas, eventBus)
else:
    elements = Elements(ballsFromFile, canvas)

buttons[0].bind('<Button-1>', elements.start)  # Обработчик событий
buttons[0].grid(row=1, column=0,
                padx=3)  # используем метод pack для отображения кнопки - в нём можно задать положение кнопки
buttons[1].grid(row=1, column=1)
buttons[2].bind('<Button-1>', elements.exit)
buttons[2].grid(row=1, column=2, padx=3)

resultFile = open(getName(elements, coordinatesFileName, ballStartFileName, freqXWall, freqYWall, velocityThetaWall),
                  'w')
makeUtils(resultFile, canvasWidth, canvasHeight)

elements.writeFile(resultFile)
elements.begin()

start_time = time.time()
steps = 0
while steps < numOfSteps:
    if elements.started:
        for i in range(step):
            elements.move()
    steps += step
    if isDraw:
        elements.draw()
        tk.update_idletasks()
        tk.update()
    elements.writeFile(resultFile)
    if addNewBalls:
        if steps >= newBallSteps[0]:
            elements.makeNewBall()
            newBallSteps.remove(newBallSteps[0])

print("+++ %s seconds +++" % (time.time() - start_time))

resultFile.write(endFileFlag)
resultFile.close()

elements.energyMonitoring()
elements.exit(None)
