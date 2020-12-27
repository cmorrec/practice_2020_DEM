displayRatio = 1000
midInteractionNum = 1000


def getForceDamping(c):
    return 1 - (1 - c) ** (1 / midInteractionNum)


isForce = True
# Класс GlobalUtils будет хранить в себе все сторонние библиотеки и константы
epsVelocity = 0.01
epsAcceleration = 0.01
eps = 1e-9
# inf = 1e11
# Критически малая величина, необходимая для сравнения вещественных чисел

step = 100
deltaTime = 1 * 1e-5
# Шаг по времени
cn_wall = 10
cs_wall = 10
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
