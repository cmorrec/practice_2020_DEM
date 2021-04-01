displayRatio = 5000
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
deltaTime = 1 * 1e-6
numOfSeconds = 0.1
numOfSteps = int(numOfSeconds * int(1 / deltaTime))
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
