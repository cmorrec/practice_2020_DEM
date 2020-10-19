from MoveLine import *
from Coordinate import *


# Класс Wall принимает в себя координаты и может принимать линии
#
# Является Singleton`ом, т.е. к нему можно обратиться из любой точки
# программы и возможно создать только один объект этого класса
#
# Для некоего синтаксического сахара необходимы:
#   - проверка на связность линий
#   - проверка на выпуклость многоугольника
#   - соотвествующие исключения
#   - конструктор, принимающий на вход только координаты(и строящий на их основе массив линий)
#   - конструктор, принимающий на вход только линии
#
# Класс Wall может принимать в себя любое количество линий и координат
#
# На данный момент класс не используется и является лишь родителем используемого
# класса MoveWall


class Wall:
    __instance = None

    def __init__(self, canvas=None, color=None, coordinates=None, accelerationX=0, accelerationY=0, lines=None):
        if coordinates is None:
            coordinates = [Coordinate(), Coordinate()]
        if lines is None:
            lines = []
            for i in range(len(coordinates)):
                lines.append(MoveLine(coordinates[i % len(coordinates)], coordinates[(i + 1) % len(coordinates)]))
        self.accelerationX = accelerationX
        self.accelerationY = accelerationY
        self.coordinates = coordinates
        self.lines = np.array(lines)
        self.canvas = canvas
        for line in self.lines:
            line.setID(canvas.create_line(line.startX1, line.startY1, line.startX2, line.startY2, fill=color))
        Wall.__instance = self

        def __new__(cls):
            if not hasattr(cls, 'instance'):
                cls.instance = super(Wall, cls).__new__(cls)
            return cls.instance

        @staticmethod
        def getInstance():
            return Wall.__instance
