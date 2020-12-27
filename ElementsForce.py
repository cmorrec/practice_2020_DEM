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

    # # Демпфирование
    # velocity1XLocal = dampingLocalVelocity(velocity1XLocal, velocity1XRelative, ball_1.cn)
    # velocity2XLocal = dampingLocalVelocity(velocity2XLocal, velocity2XRelative, ball_2.cn)
    # velocity1YLocal = dampingLocalVelocity(velocity1YLocal, velocity1YRelative, ball_1.cs)
    # velocity2YLocal = dampingLocalVelocity(velocity2YLocal, velocity2YRelative, ball_2.cs)
    # ball_1.changeVelocity(atan2(velocity1YLocal, velocity1XLocal + eps) + gama,
    #                       sqrt(velocity1XLocal ** 2 + velocity1YLocal ** 2))
    # ball_2.changeVelocity(atan2(velocity2YLocal, velocity2XLocal + eps) + gama,
    #                       sqrt(velocity2XLocal ** 2 + velocity2YLocal ** 2))

    # Непосредственно решение задачи о нецентральном упругом ударе двух дисков
    entryNormal = (ball_1.radius + ball_2.radius - sqrt((ball_1.x - ball_2.x) ** 2 + (ball_1.y - ball_2.y) ** 2))

    forceNormal1 = kn * entryNormal
    forceNormal2 = -1 * kn * entryNormal

    accelerationNormal1 = forceNormal1 / ball_1.mass
    accelerationNormal2 = forceNormal2 / ball_2.mass

    # print('velocity1YLocal', velocity1YLocal)
    # print('velocity2YLocal', velocity2YLocal)

    velocity1YRelative = findRelativeVelocityY(velocity1YLocal - velocity2YLocal, ball_1, ball_2)
    velocity2YRelative = -1 * velocity1YRelative
    signVelocityRelativeTangent1 = customSign(velocity1YRelative)
    signVelocityRelativeTangent2 = customSign(velocity2YRelative)

    velocityThetaRelative = ball_1.velocityTheta + ball_2.velocityTheta
    signVelocityRelativeAngular = customSign(velocityThetaRelative)

    radiusEffective = ((1 / ball_1.radius) + (1 / ball_2.radius)) ** (-1)

    # print(numberOfI)
    accelerationAngular1, accelerationTangent1 = ball_1.findAccelerationAngular(signVelocityRelativeTangent1,
                                                                                abs(forceNormal1), 1, radiusEffective,
                                                                                signVelocityRelativeAngular)
    # print(numberOfJ)
    accelerationAngular2, accelerationTangent2 = ball_2.findAccelerationAngular(signVelocityRelativeTangent2,
                                                                                abs(forceNormal2), -1, radiusEffective,
                                                                                signVelocityRelativeAngular)

    # ----------------------------- Damping part -----------------------------
    accelerationDampeningNormal1 = velocity1XLocal * ball_1.cn / ball_1.mass * (-1)
    accelerationDampeningTangent1 = velocity1YLocal * ball_1.cs / ball_1.mass * (-1)
    accelerationNormal1 += accelerationDampeningNormal1
    accelerationTangent1 += accelerationDampeningTangent1

    accelerationDampeningNormal2 = velocity2XLocal * ball_2.cn / ball_2.mass * (-1)
    accelerationDampeningTangent2 = velocity2YLocal * ball_2.cs / ball_2.mass * (-1)
    accelerationNormal2 += accelerationDampeningNormal2
    accelerationTangent2 += accelerationDampeningTangent2
    # ----------------------------- End damping part -----------------------------

    jerkNormal1, jerkTangent1, jerkAngular1 = ball_1.getJerk(velocity1XLocal,
                                                             accelerationNormal1 + getAccelerationFieldNormal(gama),
                                                             signVelocityRelativeTangent1,
                                                             1, radiusEffective, signVelocityRelativeAngular,
                                                             accelerationAngular1, accelerationTangent1)
    accelerationNormal1 += jerkNormal1 * deltaTime
    accelerationTangent1 += jerkTangent1 * deltaTime
    accelerationAngular1 += jerkAngular1 * deltaTime
    jerkNormal2, jerkTangent2, jerkAngular2 = ball_2.getJerk(velocity2XLocal,
                                                             accelerationNormal2 + getAccelerationFieldNormal(gama),
                                                             signVelocityRelativeTangent2,
                                                             -1, radiusEffective, signVelocityRelativeAngular,
                                                             accelerationAngular2, accelerationTangent2)
    accelerationNormal2 += jerkNormal2 * deltaTime
    accelerationTangent2 += jerkTangent2 * deltaTime
    accelerationAngular2 += jerkAngular2 * deltaTime

    ball_1.saveAccelerationLength(gama, accelerationNormal1, accelerationTangent1, jerkNormal1, jerkTangent1,
                                  jerkAngular1, entryNormal, accelerationAngular1, isBall=True, number=numberOf2)
    ball_2.saveAccelerationLength(gama, accelerationNormal2, accelerationTangent2, jerkNormal2, jerkTangent2,
                                  jerkAngular2, entryNormal, accelerationAngular2, isBall=True, number=numberOf1)


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
