from Elements import *


def isCrossForce(i, j):
    # проверяем столкнулись ли шары  и если да -- двигаются ли они навстречу друг другу
    if distanceNow(i, j) < (i.radius + j.radius):
        return True
    return False


def methodForce(i, j, numberOfI, numberOfJ):
    # Решение задачи о нецентральном упругом ударе двух дисков, путём приведения к задаче о
    # столкновении шаров по оси Х(линия столкновения становится горизонтальной, происходит
    # переход в локальную систему координат)
    # Также учет диссипации при каждом столкновении шаров

    # Угол между линией удара и горизонталью
    gamma = atan2((i.y - j.y), (i.x - j.x))
    # Углы направления шаров в локальной системе координат
    alphaRadian1Local = i.alphaRadian - gamma
    alphaRadian2Local = j.alphaRadian - gamma
    accelerationYAlphaRadianLocal = pi/2 - gamma
    # Скорости шаров в локальной системе координат
    velocity1XLocal = i.velocityAbsolute * cos(alphaRadian1Local)
    velocity1YLocal = i.velocityAbsolute * sin(alphaRadian1Local)
    velocity2XLocal = j.velocityAbsolute * cos(alphaRadian2Local)
    velocity2YLocal = j.velocityAbsolute * sin(alphaRadian2Local)

    # Демпфирование
    dampeningNormalI = (velocity1XLocal - velocity2XLocal) * i.cn
    dampeningNormalJ = (velocity2XLocal - velocity1XLocal) * j.cn
    dampeningTangentI = (velocity1YLocal - velocity2YLocal - (
            i.velocityTheta * i.radius + j.velocityTheta * j.radius)) * i.cs
    dampeningTangentJ = (velocity2YLocal - velocity1YLocal - (
            i.velocityTheta * i.radius + j.velocityTheta * j.radius)) * j.cs
    # Учет демпфирования
    velocity1XLocal = dampeningVelocity(dampeningNormalI, velocity1XLocal)
    velocity2XLocal = dampeningVelocity(dampeningNormalJ, velocity2XLocal)
    velocity1YLocal = dampeningVelocity(dampeningTangentI, velocity1YLocal)
    velocity2YLocal = dampeningVelocity(dampeningTangentJ, velocity2YLocal)
    i.changeVelocity(atan2(velocity1YLocal, velocity1XLocal + eps) + gamma,
                     sqrt(velocity1XLocal ** 2 + velocity1YLocal ** 2))
    j.changeVelocity(atan2(velocity2YLocal, velocity2XLocal + eps) + gamma,
                     sqrt(velocity2XLocal ** 2 + velocity2YLocal ** 2))

    # Непосредственно решение задачи о нецентральном упругом ударе двух дисков
    entryNormal = (i.radius + j.radius - sqrt((i.x - j.x) ** 2 + (i.y - j.y) ** 2))
    # entryTangent1 = (2 * sqrt(abs(2 * i.radius * entryNormal1 - entryNormal1 ** 2)))
    # entryTangent2 = (2 * sqrt(abs(2 * j.radius * entryNormal2 - entryNormal2 ** 2)))

    forceNormal1 = (1) * kn * entryNormal
    forceNormal2 = (-1) * kn * entryNormal
    # forceTangent1 = ks * entryTangent1
    # forceTangent2 = ks * entryTangent2

    accelerationNormal1 = forceNormal1 / i.mass
    accelerationNormal2 = forceNormal2 / j.mass
    # accelerationTangent1 = forceTangent1 / i.mass
    # accelerationTangent2 = forceTangent2 / j.mass

    rotationCS(i, j,velocity1YLocal, velocity2YLocal, dampeningTangentI, dampeningTangentJ)
    jerkI = i.getJerk(velocity1XLocal, accelerationNormal1 + accelerationY*cos(accelerationYAlphaRadianLocal), kn, i.mass)
    accelerationNormal1 += jerkI * deltaTime
    jerkJ = j.getJerk(velocity2XLocal, accelerationNormal2 + accelerationY*cos(accelerationYAlphaRadianLocal), kn, j.mass)
    accelerationNormal2 += jerkJ * deltaTime

    i.saveAccelerationLength(gamma, accelerationNormal1, jerkI, isBall=True, number=numberOfJ)
    j.saveAccelerationLength(gamma, accelerationNormal2, jerkJ, isBall=True, number=numberOfI)


def isCrossBefore(i, j, numberOfI, numberOfJ):  # Возможно стоит удалить две неиспользуемых переменных
    for interaction in i.interactionArray:
        if interaction.isBall and interaction.number == numberOfJ:
            return True
    return False


def deleteInteraction(i, numberOfJ):
    for interaction in i.interactionArray:
        if interaction.isBall and interaction.number == numberOfJ:
            i.interactionArray.remove(interaction)
            break


class ElementsForce(Elements):
    def __init__(self, balls, canvas):
        Elements.__init__(self, balls, canvas)

    def move(self):
        # Есть необходимость отключения не глобальных ускорений, а ускорений взаимодействия,
        # поэтому этот метод и строчка неизменны
        # self.setAcceleration()

        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if isCrossForce(self.balls[i], self.balls[j]):
                    methodForce(self.balls[i], self.balls[j], i, j)
                elif isCrossBefore(self.balls[i], self.balls[j], i, j):
                    deleteInteraction(self.balls[i], j)
                    deleteInteraction(self.balls[j], i)
