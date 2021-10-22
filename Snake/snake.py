import time
import random
import keyboard
import os

def writefield(fields):
    os.system("cls")
    for i in range(len(fields)):
        for j in range(len(fields[i])):
            print(fields[i][j],end="")
        print("")
    print("")

def spawnapple():

    global field
    global posapplex
    global posappley
    global schwanzteile

    while True:
        posappley = random.randint(0,len(field)-1)
        posapplex = random.randint(0,len(field[0])-1)

        if field[posappley][posapplex] == "[ ]":
            schwanzteile.append([])
            schwanzteile[len(schwanzteile)-1].append(posappley)
            schwanzteile[len(schwanzteile)-1].append(posapplex)                   #🍎
            field[posappley][posapplex] = "[o]"
            writefield(field)
            break
        else:
            posappley = random.randint(0,len(field)-1)
            posapplex = random.randint(0,len(field[0])-1)
            continue

def gameover():
    print("Game Over")
    print("Score: "+str(len(schwanzteile)-1))
    time.sleep(5)
    exit()

def listenforinput():

    global posx
    global posy
    global field
    global schwanzteile
    global posapplex
    global posappley
    global visitedfields
    global c

    visitedfields.append([])

    for i in range(len(field)):
        for j in range(len(field[i])):
            field[i][j] = "[ ]"

    schwanzteile[0][0] = posy
    schwanzteile[0][1] = posx
    
    field[posappley][posapplex] = "[o]"

    while True:
        if keyboard.is_pressed("w"):
            direction = "w"
            break
        elif keyboard.is_pressed("a"):
            direction = "a"
            break
        elif keyboard.is_pressed("s"):
            direction = "s"
            break
        elif keyboard.is_pressed("d"):
            direction = "d"
            break

        time.sleep(0.01)

    while keyboard.is_pressed("w") or keyboard.is_pressed("a") or keyboard.is_pressed("s") or keyboard.is_pressed("d"):
        time.sleep(0.1)
    
    if direction == "w":
        posy-=1
    elif direction == "a":
        posx-=1
    elif direction == "s":
        posy+=1
    elif direction == "d":
        posx+=1

    visitedfields[c].append(posy)
    visitedfields[c].append(posx)

    for i in range(len(visitedfields)-len(schwanzteile)):
        visitedfields.pop(0)
        c-=1

    for i in range(len(visitedfields)-1):
        field[visitedfields[i][0]][visitedfields[i][1]] = "[=]"

    if str(posx).startswith("-") or str(posy).startswith("-"):
        gameover()

    try:
        if field[posy][posx] == "[=]":
            gameover()
    except IndexError:
        print("",end="")

    try:
        field[posy][posx] = "[0]"
    except IndexError:
        gameover()

    writefield(field)

while True:
    try:
        fieldhight = int(input("Fieldheight: "))
        fieldwidth = int(input("Fieldwidth: "))
        if fieldhight < 3 or fieldwidth < 3:
            print("Minimum size is 3")
        else:
            break
    except ValueError:
        continue

field = [["[0]"]]


for j in range(fieldhight):
    field.append([])
    if j == 0:
        for i in range(fieldwidth-1):
            field[j].append("[ ]")
    else:
        for i in range(fieldwidth):
            field[j].append("[ ]")

field.pop()

schwanzteile = []
visitedfields = []
posx,posy = 0,0
posapplex,posappley = 0,0
c = 0

visitedfields.append([])
visitedfields[c].append(posy)
visitedfields[c].append(posx)

print(len(field))

spawnapple()

writefield(field)

while True:
    if posx == posapplex and posy == posappley:
        spawnapple()

    c+=1
    listenforinput()

    if len(schwanzteile) == len(field[0])*len(field):
        print("WoW you won!")
        print("Score:"+str(len(schwanzteile)-1))
        time.sleep(10)
        exit()
