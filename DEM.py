from Elements import *

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
canvas = Canvas(tk, width=mWidth, height=mHeight, highlightthickness=0)
canvas.pack()
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
while not elements.starts:
    if elements.started:
        elements.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(deltaTime)

saveResults(elements)
