from Elements import *


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

    # Непосредственно решение задачи о нецентральном упругом ударе двух дисков
    velocity1XLocalNew = ((i.mass - j.mass) * velocity1XLocal + 2 * j.mass * velocity2XLocal) / (i.mass + j.mass)
    velocity2XLocalNew = (2 * i.mass * velocity1XLocal + (j.mass - i.mass) * velocity2XLocal) / (i.mass + j.mass)
    # Демпфирование
    dampeningNormalI = (velocity1XLocalNew - velocity2XLocalNew) * i.cn
    dampeningNormalJ = (velocity2XLocalNew - velocity1XLocalNew) * j.cn
    dampeningTangentI = (velocity1YLocal - velocity2YLocal - (
            i.velocityTheta * i.radius + j.velocityTheta * j.radius)) * i.cs
    dampeningTangentJ = (velocity2YLocal - velocity1YLocal - (
            i.velocityTheta * i.radius + j.velocityTheta * j.radius)) * j.cs
    # Учет демпфирования
    velocity1XLocalNew = dampeningVelocity(dampeningNormalI, velocity1XLocalNew)
    velocity2XLocalNew = dampeningVelocity(dampeningNormalJ, velocity2XLocalNew)
    velocity1YLocal = dampeningVelocity(dampeningTangentI, velocity1YLocal)
    velocity2YLocal = dampeningVelocity(dampeningTangentJ, velocity2YLocal)
    # Задание новой угловой скорости дисков
    rotation(i, j, velocity1YLocal, velocity2YLocal)
    # Возвращение к глобальной системе координат
    newAlphaI = atan2(velocity1YLocal, velocity1XLocalNew + eps) + gamma
    newAlphaJ = atan2(velocity2YLocal, velocity2XLocalNew + eps) + gamma
    newVelocityAbsoluteI = sqrt(velocity1XLocalNew ** 2 + velocity1YLocal ** 2)
    newVelocityAbsoluteJ = sqrt(velocity2XLocalNew ** 2 + velocity2YLocal ** 2)
    # Задание нового вектора скорости
    i.changeVelocity(newAlphaI, newVelocityAbsoluteI)
    j.changeVelocity(newAlphaJ, newVelocityAbsoluteJ)


class ElementsForce(Elements):
    def move(self):
        # В случае столкновения шаров друг с другом решается задача о нецентральном упругом ударе
        self.setAcceleration()

        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if isCross(self.balls[i], self.balls[j]):
                    methodForce(self.balls[i], self.balls[j])
