from Elements import *
from PIL import ImageTk
coordinatesFile = open('wall_coordinates.txt', 'r')
coordinatesFromFile = []

isFirstLine = True

velocityXWall = float(0)
velocityYWall = float(0)
absXWall = float(0)
absYWall = float(0)

for line in coordinatesFile:
    words = line.split()
    data = []
    if isFirstLine:
        velocityXWall = float(words[0])
        velocityYWall = float(words[1])
        absXWall = float(words[2])
        absYWall = float(words[3])
        isFirstLine = False
    else:
        for word in words:
            data.append(float(word))
    if len(data) > 0:
        coordinatesFromFile.append(Coordinate(data[0], data[1]))

coordinatesFile.close()

xCoordinates = []
yCoordinates = []
for coordinate in coordinatesFromFile:
    xCoordinates.append(coordinate.x)
    yCoordinates.append(coordinate.y)
mWidth = max(xCoordinates) - min(xCoordinates) + absXWall
mHeight = max(yCoordinates) - min(yCoordinates) + absYWall

tk = Tk()
tk.title('DEM')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
tk.columnconfigure(0)
tk.columnconfigure(1)
tk.columnconfigure(2)
tk.rowconfigure(0)
tk.rowconfigure(1)
canvas = Canvas(tk, width=mWidth, height=mHeight, highlightthickness=0)
canvas.grid(row=0, columnspan=3)
but_1 = Button(text='Start',
               width=17, height=2,
               bg='#5195fc', fg='white',
               activebackground='#77DDE7',  # цвет нажатой кнопки
               activeforeground='#FF2400',  # цвет надписи когда кнопка нажата
               font='Hack 16')  # шрифт и размер надписи
artem = ImageTk.PhotoImage(file="folder.png")
but_2 = Button(image=artem)
but_3 = Button(text='Stop',
               width=17, height=2,
               bg='#fc5151', fg='white',
               activebackground='#77DDE7',
               activeforeground='#FF2400',
               font='Hack 16')
tk.update()

wall = MoveWall(canvas, 'black', coordinatesFromFile, accelerationX, accelerationY, None, velocityXWall, velocityYWall,
                absXWall, absYWall)

ballsStartFile = open('balls_start.txt', 'r')
ballsFromFile = []

for line in ballsStartFile:
    words = line.split()
    data = []
    j = 0
    color = ''
    for word in words:
        if j != len(words) - 1:
            data.append(float(word))
        else:
            color = word
        j += 1
    if len(data) > 0:
        ballsFromFile.append(Ball(data[0], data[1], data[2], data[3], data[4], data[5], data[6], color, canvas))

ballsStartFile.close()

elements = Elements(ballsFromFile, canvas)

but_1.bind('<Button-1>', elements.start)  # Обработчик событий
but_1.grid(row=1, column=0, padx=3)  # используем метод pack для отображения кнопки - в нём можно задать положение кнопки
but_2.grid(row=1, column=1)
but_3.bind('<Button-1>', elements.exit)
but_3.grid(row=1, column=2, padx=3)

while not elements.starts:
    if elements.started:
        elements.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(deltaTime)

saveResults(elements)
