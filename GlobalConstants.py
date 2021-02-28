displayRatio = 1000
midInteractionNum = 100


def getForceDamping(c):
    return 1 - (1 - c) ** (1 / midInteractionNum)


isForce = True
# Класс GlobalUtils будет хранить в себе все сторонние библиотеки и константы
epsVelocity = 0.01
epsAcceleration = 0.00001
epsAcceleration2 = 1
eps = 1e-9
# inf = 1e11
# Критически малая величина, необходимая для сравнения вещественных чисел

step = 100
deltaTime = 1 * 1e-5
numOfSeconds = 1
numOfSteps = int(numOfSeconds * int(1 / deltaTime))
# Шаг по времени
cn_wall = 1
cs_wall = 0.2
Emod_wall = 2 * 1e11
nu_wall = 0.3
Gmod_wall = Emod_wall / (2 * (1 + nu_wall))
coefficientOfDampingTheta = 0

# if isForce:
#     cn_wall = getForceDamping(cn_wall)
#     cs_wall = getForceDamping(cs_wall)

coefficientOfFrictionSliding = 0.1
coefficientOfFrictionRolling = 0.05

# коэффициенты демпфирования для стенок
accelerationX = 0
accelerationY = 9.81
kn = 2 * 1e5
# ks = 0
