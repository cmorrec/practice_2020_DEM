from math import *
class Ball:
    def __init__(self, x, y, canvas, color, radius, alpha, velocity):
        self.alphaRadian = alpha * pi / 180
        self.velocityX = velocity * cos(self.alphaRadian)
        self.velocityY = velocity * sin(self.alphaRadian)
        self.radius = radius
        self.x = x
        self.y = y
        self.velocityAbsolute = velocity
        self.canvas = canvas
        self.id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        #self.starts = False
        #self.started = False
        self.canvas.bind_all('<KeyPress-s>', self.start)                # s - начало движения
        self.canvas.bind_all('<KeyPress-e>', self.exit)                 # e - конец движения

    def move(self):
        pos = self.canvas.coords(self.id)                               # овал задается по 4-м коордиатам по которым
        self.x = (pos[0] + pos[2]) / 2                                  # можно найти координаты центра
        self.y = (pos[1] + pos[3]) / 2

        if not self.isInside():
            self.reset()
            self.velocityX = self.velocityAbsolute * cos(self.alphaRadian)
            self.velocityY = self.velocityAbsolute * sin(self.alphaRadian)

    def reset(self):
        # смена углов в зависимости от стены от которой оттолкнулся мяч
        if self.x < self.radius or self.x + self.radius > self.canvas_width:
            if self.alphaRadian < 0:
                self.alphaRadian = -pi - self.alphaRadian
            else:
                self.alphaRadian = pi - self.alphaRadian
        elif self.y < self.radius or self.y + self.radius > self.canvas_height:
            if (((self.y < self.radius) and (sin(self.alphaRadian) < 0)) or
                    ((self.y + self.radius > self.canvas_height) and (sin(self.alphaRadian) > 0))):
                # последнее сложное условие необходимо для того чтобы мяч успевал отойти от стены
                # при некоторых углах он бы без этого условия двигался бы вдоль стены
                self.alphaRadian *= -1

    def isInside(self):
        # проверка на выход мяча из границ
        return (self.x >= self.radius) and (self.x + self.radius <= self.canvas_width) and \
               (self.y >= self.radius) and (self.y + self.radius <= self.canvas_height)

    def draw(self):
        self.move()                                                 # фактическое движение
        self.canvas.move(self.id, self.velocityX, self.velocityY)   # прорисовка движения

    def start(self, event):
        self.started = True

    def exit(self, event):
        self.started = False
