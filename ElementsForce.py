from Elements import *

def rotationForce(i, j, velocity1YLocal, velocity2YLocal):
    velocityThetaI = i.velocityTheta
    velocityThetaJ = j.velocityTheta

    i.velocityTheta += (1 /(i.mass * i.radius)) * (1 - i.cs) * (
            (velocity1YLocal - velocity2YLocal)*deltaTime - (velocityThetaI * i.radius + velocityThetaJ * j.radius)) * (
                               deltaTime**2)
    j.velocityTheta += (1 / (j.mass * j.radius)) * (1 - j.cs) * (
            velocity2YLocal - velocity1YLocal - (velocityThetaI * i.radius + velocityThetaJ * j.radius)) * (
                               deltaTime ** 2)
def isCrossForce(i, j):
    # проверяем столкнулись ли шары  и если да -- двигаются ли они навстречу друг другу
    if distanceNow(i, j) < (i.radius + j.radius):
        return True
    return False

def methodForce(i, j):
    # Решение задачи о нецентральном упругом ударе двух дисков, путём приведения к задаче о
    # столкновении шаров по оси Х(линия столкновения становится горизонтальной, происходит
    # переход в локальную систему координат)
    # Также учет диссипации при каждом столкновении шаров

    # Угол между линией удара и горизонталью
    gamma = atan2((i.y - j.y), (i.x - j.x))
    # Углы направления шаров в локальной системе координат
    alphaRadian1Local = i.alphaRadian - gamma
    alphaRadian2Local = j.alphaRadian - gamma
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
    entryNormal1 = (velocity1XLocal - velocity2XLocal) * deltaTime
    entryNormal2 = (velocity2XLocal - velocity1XLocal) * deltaTime
    entryTangent1 = (velocity1YLocal - velocity2YLocal - (
            i.velocityTheta * i.radius + j.velocityTheta * j.radius)) * deltaTime
    entryTangent2 = (velocity2YLocal - velocity1YLocal - (
            i.velocityTheta * i.radius + j.velocityTheta * j.radius)) * deltaTime

    forceNormal1 = kn * entryNormal1
    forceTangent1 = ks * entryTangent1
    forceNormal2 = kn * entryNormal2
    forceTangent2 = ks * entryTangent2

    accelerationNormal1 = forceNormal1 / i.mass
    accelerationTangent1 = forceTangent1 / i.mass
    accelerationNormal2 = forceNormal2 / j.mass
    accelerationTangent2 = forceTangent2 / j.mass

    # Задание новой угловой скорости дисков
    # rotation(i, j, velocity1YLocal, velocity2YLocal)

    i.saveAcceleration(gamma, accelerationNormal1, 0)
    j.saveAcceleration(gamma, accelerationNormal2, 0)


def methodForceLength(i, j):
    # Решение задачи о нецентральном упругом ударе двух дисков, путём приведения к задаче о
    # столкновении шаров по оси Х(линия столкновения становится горизонтальной, происходит
    # переход в локальную систему координат)
    # Также учет диссипации при каждом столкновении шаров

    # Угол между линией удара и горизонталью
    gamma = atan2((i.y - j.y), (i.x - j.x))
    # Углы направления шаров в локальной системе координат
    alphaRadian1Local = i.alphaRadian - gamma
    alphaRadian2Local = j.alphaRadian - gamma
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
    entryNormal1 = (i.radius + j.radius - sqrt((i.x - j.x) ** 2 + (i.y - j.y) ** 2))
    entryNormal2 = (i.radius + j.radius - sqrt((i.x - j.x) ** 2 + (i.y - j.y) ** 2))
    entryTangent1 = (2 * sqrt(abs(2 * i.radius * entryNormal1 - entryNormal1 ** 2)))
    entryTangent2 = (2 * sqrt(abs(2 * j.radius * entryNormal2 - entryNormal2 ** 2)))

    forceNormal1 = - kn * entryNormal1
    forceTangent1 = -ks * entryTangent1
    forceNormal2 = kn * entryNormal2
    forceTangent2 = ks * entryTangent2

    accelerationNormal1 = forceNormal1 / i.mass
    accelerationTangent1 = forceTangent1 / i.mass
    accelerationNormal2 = forceNormal2 / j.mass
    accelerationTangent2 = forceTangent2 / j.mass


    rotation(i, j, velocity1YLocal, velocity2YLocal)

    i.saveAccelerationLength(gamma, accelerationNormal1, 0)
    j.saveAccelerationLength(gamma, accelerationNormal2, 0)


class ElementsForce(Elements):
    def move(self):
        # В случае столкновения шаров друг с другом решается задача о нецентральном упругом ударе
        self.setAcceleration()

        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if isCrossForce(self.balls[i], self.balls[j]):
                    if not (self.balls[i].crossPolygon() and self.balls[j].crossPolygon()):
                        methodForceLength(self.balls[i], self.balls[j])
                    elif (self.balls[i].velocityAbsolute < epsVelocity and self.balls[j].velocityAbsolute < epsVelocity) and (self.balls[i].crossPolygon() and self.balls[j].crossPolygon()):
                        self.balls[i].velocityAbsolute = 0
                        self.balls[j].velocityAbsolute = 0
                        self.balls[i].accelerationY = 0
                        self.balls[i].accelerationY = 0
