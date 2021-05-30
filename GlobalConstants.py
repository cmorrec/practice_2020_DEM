displayRatio = 300
midInteractionNum = 100
inLineDelimiter = '\t'
ballFlag = 'ball:'
ballInitFlag = 'ballInit:'
wallFlag = 'wall:'
wallInitFlag = 'wallInit:'
utilsFlag = 'utils:'
nextStepFlag = 'next'
endFileFlag = 'end\n'


def getForceDamping(c):
    return 1 - (1 - c) ** (1 / midInteractionNum)


isDraw = True
isForce = True
# Класс GlobalUtils будет хранить в себе все сторонние библиотеки и константы
epsVelocity = 0.01
epsAcceleration = 0.00001
eps = 1e-9
# inf = 1e11
# Критически малая величина, необходимая для сравнения вещественных чисел

step = 100
deltaTime = 1 * 1e-5
numOfSeconds = 5
numOfSteps = int(numOfSeconds * int(1 / deltaTime))
addNewBalls = True
newBallPeriod = 0.2
newBallPeriodSteps = round(newBallPeriod * int(1 / deltaTime))
newBallCount = round(numOfSeconds / newBallPeriod)
newBallSteps = [i * newBallPeriodSteps for i in range(1, newBallCount)]

# Шаг по времени
cn_wall = 1
cs_wall = 0.2
Emod_wall = 2 * 1e11
nu_wall = 0.3
Gmod_wall = Emod_wall / (2 * (1 + nu_wall))
coefficientOfDampingTheta = 0

coefficientOfFrictionSliding = 0.1
coefficientOfFrictionRolling = 0.05

# коэффициенты демпфирования для стенок
accelerationX = 0
accelerationY = 9.81
kn = 2 * 1e5

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

ballStartFileNameFraction120 = './ball_sets/mill/fraction/120.txt'
ballStartFileNameOre120 = './ball_sets/mill/ore/120.txt'
ballStartFileNameFraction240 = './ball_sets/mill/fraction/240.txt'
ballStartFileNameOre240 = './ball_sets/mill/ore/240.txt'

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
coordinatesFileNameMill2Dot5m = './walls_dynamic/wall_mill_2dot5m.txt'
coordinatesFileNameMill1m = './walls_dynamic/wall_mill_1m.txt'
coordinatesFileNameVibroBox = './walls_dynamic/vibro_box.txt'
