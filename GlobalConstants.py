displayRatio = 1000
midInteractionNum = 32


def getForceDamping(c):
    return 1 - (1 - c) ** (1 / midInteractionNum)


isForce = True
# Класс GlobalUtils будет хранить в себе все сторонние библиотеки и константы
epsVelocity = 0.01
epsAcceleration = 0.00001
eps = 1e-9
# inf = 1e11
# Критически малая величина, необходимая для сравнения вещественных чисел

step = 100
deltaTime = 1 * 1e-5
# Шаг по времени
cn_wall = 1
cs_wall = 1
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

E_1 = 2 * 1e11
E_2 = 2 * 1e11
nu_1 = 0.3
nu_2 = 0.3
E_eff = ((1 - (nu_1 ** 2))/E_1 + (1 - (nu_2 ** 2))/E_2) ** (-1)
G_1 = 8 * 1e10
G_2 = 8 * 1e10
G_eff = ((2 - nu_1)/G_1 + (2 - nu_2)/G_2) ** (-1)
