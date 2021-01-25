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

    E_eff = ((1 - (ball_1.nu ** 2)) / ball_1.Emod + (1 - (ball_2.nu ** 2)) / ball_2.Emod) ** (-1)
    G_eff = ((2 - ball_1.nu) / ball_1.Gmod + (2 - ball_2.nu) / ball_2.Gmod) ** (-1)

    velocity1XLocal, velocity1YLocal = findLocalVelocities(ball_1, gama)
    velocity2XLocal, velocity2YLocal = findLocalVelocities(ball_2, gama)

    velocity1XRelative = velocity1XLocal - velocity2XLocal
    velocity2XRelative = velocity2XLocal - velocity1XLocal

    # Непосредственно решение задачи о нецентральном упругом ударе двух дисков
    entryNormal = (ball_1.radius + ball_2.radius - sqrt((ball_1.x - ball_2.x) ** 2 + (ball_1.y - ball_2.y) ** 2))
    radiusEffective = ((1 / ball_1.radius) + (1 / ball_2.radius)) ** (-1)

    stiffness = getStiffness(radiusEffective, entryNormal, E_eff)
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

    # ----------------------------- Damping part -----------------------------
    accelerationDampeningNormal1 = velocity1XRelative * getDampingNormal(radiusEffective, entryNormal,
                                                                         ball_1.mass, ball_1.cn, E_eff) / ball_1.mass * (-1)
    accelerationDampeningTangent1 = velocity1YRelative * getDampingTangent(radiusEffective, entryNormal,
                                                                           ball_1.mass, ball_1.cs, G_eff) / ball_1.mass
    accelerationNormal1 += accelerationDampeningNormal1
    accelerationTangent1 += accelerationDampeningTangent1

    accelerationDampeningNormal2 = velocity2XRelative * getDampingNormal(radiusEffective, entryNormal,
                                                                         ball_2.mass, ball_2.cn, E_eff) / ball_2.mass * (-1)
    accelerationDampeningTangent2 = velocity2YRelative * getDampingTangent(radiusEffective, entryNormal,
                                                                           ball_2.mass, ball_2.cs, G_eff) / ball_2.mass
    accelerationNormal2 += accelerationDampeningNormal2
    accelerationTangent2 += accelerationDampeningTangent2
    # ----------------------------- End damping part -----------------------------
    jerkNormal1, jerkTangent1, jerkAngular1 = ball_1.getJerk(entryNormal, velocity1XRelative,
                                                             accelerationNormal1 + getAccelerationFieldNormal(gama),
                                                             signVelocityRelativeTangent1, 1, radiusEffective,
                                                             signVelocityRelativeAngular, accelerationAngular1,
                                                             accelerationTangent1, E_eff)
    accelerationNormal1 += jerkNormal1 * deltaTime
    accelerationTangent1 += jerkTangent1 * deltaTime
    accelerationAngular1 += jerkAngular1 * deltaTime
    jerkNormal2, jerkTangent2, jerkAngular2 = ball_2.getJerk(entryNormal, velocity2XRelative,
                                                             accelerationNormal2 + getAccelerationFieldNormal(gama),
                                                             signVelocityRelativeTangent2,
                                                             -1, radiusEffective, signVelocityRelativeAngular,
                                                             accelerationAngular2, accelerationTangent2, E_eff)
    accelerationNormal2 += jerkNormal2 * deltaTime
    accelerationTangent2 += jerkTangent2 * deltaTime
    accelerationAngular2 += jerkAngular2 * deltaTime

    ball_1.saveAccelerationLength(gama, accelerationNormal1, accelerationTangent1, jerkNormal1, jerkTangent1,
                                  jerkAngular1, entryNormal, accelerationAngular1, isBall=True, number=numberOf2,
                                  stiffness=stiffness)
    ball_2.saveAccelerationLength(gama, accelerationNormal2, accelerationTangent2, jerkNormal2, jerkTangent2,
                                  jerkAngular2, entryNormal, accelerationAngular2, isBall=True, number=numberOf1,
                                  stiffness=stiffness)


def isCrossBefore(i, numberOfJ):  # Возможно стоит удалить две неиспользуемых переменных
    for k in range(i.interactionArraySize):
        if i.interactionArray[k].isBall and i.interactionArray[k].number == numberOfJ:
            return True
    return False


def deleteInteractionBall(i, numberOfJ):
    for k, interaction in enumerate(i.interactionArray):
        if interaction.isBall and interaction.number == numberOfJ:
            # if len(ballInteraction) > 0:
            #     if ballInteraction[len(ballInteraction) - 1] != interaction.n:
            #         ballInteraction.append(interaction.n)
            # else:
            #     ballInteraction.append(interaction.n)
            i.deleteInteraction(k)
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
                    deleteInteractionBall(self.balls[i], j)
                    deleteInteractionBall(self.balls[j], i)
