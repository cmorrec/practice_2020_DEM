from BallForce import *
from Elements import *


def isCrossForce(i, j):
    # проверяем столкнулись ли шары  и если да -- двигаются ли они навстречу друг другу
    if distanceNow(i, j) < (i.radius + j.radius):
        return True
    return False


def rotationCS(i, j, velocity1YLocal, velocity2YLocal, dampeningTangentI, dampeningTangentJ):
    i.rotationCS(velocity1YLocal, dampeningTangentI)
    j.rotationCS(velocity2YLocal, dampeningTangentJ)


def findLocalVelocities(ball, gama):
    # Угол между линией удара и горизонталью

    # Углы направления шаров в локальной системе координат
    alphaRadianLocal = ball.alphaRadian - gama
    # Скорости шаров в локальной системе координат
    velocityXLocal = ball.velocityAbsolute * cos(alphaRadianLocal)
    velocityYLocal = ball.velocityAbsolute * sin(alphaRadianLocal)

    return velocityXLocal, velocityYLocal


def findRelativeVelocityY(velocityYLocal, ball_1, ball_2):
    return velocityYLocal - ((ball_1.velocityTheta * ball_1.radius) + (ball_2.velocityTheta * ball_2.radius))


def dampingLocalVelocity(velocity, velocityRelative, c):
    dampening = velocityRelative * c
    velocity = dampeningVelocity(dampening, velocity)
    return velocity


def methodForce(ball_1, ball_2, numberOf1, numberOf2):
    # Решение задачи о нецентральном упругом ударе двух дисков, путём приведения к задаче о
    # столкновении шаров по оси Х(линия столкновения становится горизонтальной, происходит
    # переход в локальную систему координат)
    # Также учет диссипации при каждом столкновении шаров

    gama = atan2((ball_1.y - ball_2.y), (ball_1.x - ball_2.x))

    velocity1XLocal, velocity1YLocal = findLocalVelocities(ball_1, gama)
    velocity2XLocal, velocity2YLocal = findLocalVelocities(ball_2, gama)

    velocity1XRelative = velocity1XLocal - velocity2XLocal
    velocity2XRelative = velocity2XLocal - velocity1XLocal
    velocity1YRelative = findRelativeVelocityY(velocity1YLocal - velocity2YLocal, ball_1, ball_2)
    velocity2YRelative = -1 * velocity1YRelative

    # Демпфирование
    velocity1XLocal = dampingLocalVelocity(velocity1XLocal, velocity1XRelative, ball_1.cn)
    velocity2XLocal = dampingLocalVelocity(velocity2XLocal, velocity2XRelative, ball_2.cn)
    velocity1YLocal = dampingLocalVelocity(velocity1YLocal, velocity1YRelative, ball_1.cs)
    velocity2YLocal = dampingLocalVelocity(velocity2YLocal, velocity2YRelative, ball_2.cs)
    ball_1.changeVelocity(atan2(velocity1YLocal, velocity1XLocal + eps) + gama,
                          sqrt(velocity1XLocal ** 2 + velocity1YLocal ** 2))
    ball_2.changeVelocity(atan2(velocity2YLocal, velocity2XLocal + eps) + gama,
                          sqrt(velocity2XLocal ** 2 + velocity2YLocal ** 2))

    # Непосредственно решение задачи о нецентральном упругом ударе двух дисков
    entryNormal = (ball_1.radius + ball_2.radius - sqrt((ball_1.x - ball_2.x) ** 2 + (ball_1.y - ball_2.y) ** 2))
    radiusEffective = ((1 / ball_1.radius) + (1 / ball_2.radius)) ** (-1)

    stiffness = getStiffness(radiusEffective, entryNormal)
    forceNormal1 = stiffness * entryNormal
    forceNormal2 = -1 * stiffness * entryNormal

    forcePlot.append(abs(forceNormal1))
    velocityPlot.append(velocity1XLocal * 10000)
    if len(stepCountForce) == 0:
        stepCountForce.append(0)
    else:
        stepCountForce.append(stepCountForce[len(stepCountForce) - 1] + 1)

    accelerationNormal1 = forceNormal1 / ball_1.mass
    accelerationNormal2 = forceNormal2 / ball_2.mass

    jerk1 = ball_1.getJerk(velocity1XLocal, accelerationNormal1 + getAccelerationFieldNormal(gama), entryNormal, radiusEffective, forceNormal1)
    accelerationNormal1 += jerk1 * deltaTime
    jerk2 = ball_2.getJerk(velocity2XLocal, accelerationNormal2 + getAccelerationFieldNormal(gama), entryNormal, radiusEffective, forceNormal2)
    accelerationNormal2 += jerk2 * deltaTime

    # print('velocity1YLocal', velocity1YLocal)
    # print('velocity2YLocal', velocity2YLocal)

    velocity1YRelative = findRelativeVelocityY(velocity1YLocal - velocity2YLocal, ball_1, ball_2)
    velocity2YRelative = -1 * velocity1YRelative
    signVelocityRelativeTangent1 = customSign(velocity1YRelative)
    signVelocityRelativeTangent2 = customSign(velocity2YRelative)

    velocityThetaRelative = ball_1.velocityTheta + ball_2.velocityTheta
    signVelocityRelativeAngular = customSign(velocityThetaRelative)

    # print(numberOfI)
    accelerationAngular1, accelerationTangent1 = ball_1.findAccelerationAngular(signVelocityRelativeTangent1,
                                                                                abs(forceNormal1), 1, radiusEffective,
                                                                                signVelocityRelativeAngular)
    # print(numberOfJ)
    accelerationAngular2, accelerationTangent2 = ball_2.findAccelerationAngular(signVelocityRelativeTangent2,
                                                                                abs(forceNormal2), -1, radiusEffective,
                                                                                signVelocityRelativeAngular)

    ball_1.saveAccelerationLength(gama, accelerationNormal1, accelerationTangent1, jerk1, entryNormal,
                                  accelerationAngular1, isBall=True, number=numberOf2, stiffness=stiffness)
    ball_2.saveAccelerationLength(gama, accelerationNormal2, accelerationTangent2, jerk2, entryNormal,
                                  accelerationAngular2, isBall=True, number=numberOf1, stiffness=stiffness)


def isCrossBefore(i, numberOfJ):  # Возможно стоит удалить две неиспользуемых переменных
    for interaction in i.interactionArray:
        if interaction.isBall and interaction.number == numberOfJ:
            return True
    return False


def deleteInteraction(i, numberOfJ):
    for interaction in i.interactionArray:
        if interaction.isBall and interaction.number == numberOfJ:
            if len(ballInteraction) > 0:
                if ballInteraction[len(ballInteraction) - 1] != interaction.n:
                    ballInteraction.append(interaction.n)
            else:
                ballInteraction.append(interaction.n)
            i.interactionArray.remove(interaction)
            break


class ElementsForce(Elements):
    def __init__(self, balls, canvas):
        Elements.__init__(self, balls, canvas)

    def calculation(self):
        # Есть необходимость отключения не глобальных ускорений,
        # а ускорений взаимодействия, что проверяется отдельно
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if isCrossForce(self.balls[i], self.balls[j]):
                    methodForce(self.balls[i], self.balls[j], i, j)
                elif isCrossBefore(self.balls[i], j):
                    deleteInteraction(self.balls[i], j)
                    deleteInteraction(self.balls[j], i)

