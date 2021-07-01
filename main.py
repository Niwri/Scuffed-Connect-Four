from graphics import *
import keyboard
import time
import sys
import threading


width = 1000
height = 800
board = [[Circle(Point(0,0), 0)]*6 for x in range(7)]
boardRep = [[0]*6 for x in range(7)]
game = True
gameRound = True
playerTurn = True
red = color_rgb(255, 0, 0)
black = color_rgb(0, 0, 0)
counter = 0

win = GraphWin("Scuffed Connect Four", width, height)
win.setBackground(color_rgb(59, 59, 59))
space = 80
scoreOne = 0
scoreTwo = 0
playerOnePos = 3
playerTwoPos = 3

xPosOne = (width + space * (8 - 2 * 7)) / 2 - 40
xPosTwo = (width + space * (8 - 2 * 1)) / 2 + 40
yPosOne = (height + space * (7 - 2 * 6)) / 2 - 40
yPosTwo = (height + space * (7 - 2 * 1)) / 2 + 40

message = Text(Point(width / 2, yPosOne-100), "")
message.setSize(20)
message.setTextColor(color_rgb(255, 255, 255))

displayScoreOne = Text(Point(150, height-50), ("Player One's Score: " + str(scoreOne)))
displayScoreOne.setSize(15)
displayScoreOne.setTextColor(color_rgb(200, 200, 200))

displayScoreTwo = Text(Point(width-150, height-50), ("Player Two's Score: " + str(scoreTwo)))
displayScoreTwo.setSize(15)
displayScoreTwo.setTextColor(color_rgb(200, 200, 200))

def boardDisplay():
    global board, boardRep, message

    #Drawing grid
    b = Rectangle(Point(xPosOne-10, yPosOne-10), Point(xPosTwo+10, yPosTwo+10))
    b.setFill(color_rgb(0, 13, 54))
    b.draw(win)
    r = Rectangle(Point(xPosOne, yPosOne), Point(xPosTwo, yPosTwo))
    r.draw(win)
    r.setFill(color_rgb(147, 204, 219))

    #Drawing lines
    for x in range(6):
        xPos = (width + space * (8 - 2 * (6 - x))) / 2 - 40
        a = Line(Point(xPos, yPosOne), Point(xPos, yPosTwo))
        a.draw(win)

    #Drawing circles
    for x in range(7):
        for i in range(6):
            c = Circle(Point((width + space * (8 - 2 * (x + 1))) / 2, (height + space * (7 - 2 * (i + 1))) / 2), 35)
            c.setFill(color_rgb(98, 139, 150))
            c.draw(win)
            board[x][i] = Circle(Point((width+space*(8-2*(x+1)))/2, (height+space*(7-2*(i+1)))/2), 30)
            board[x][i].draw(win)
            board[x][i].setFill(color_rgb(255, 255, 255))

    #Setting Texts
    message.undraw()
    message.setText("")
    message.draw(win)

    displayScoreOne.undraw()
    displayScoreOne.setText(("Player One's Score: " + str(scoreOne)))
    displayScoreOne.draw(win)
    displayScoreTwo.undraw()
    displayScoreTwo.setText(("Player Two's Score: " + str(scoreTwo)))
    displayScoreTwo.draw(win)

def selectColumn(color, player, column):
    c = Circle(Point((width + space * (8 - 2 * (column + 1))) / 2, yPosOne - 40), 25)
    while True:
        c.undraw()
        c = Circle(Point((width + space * (8 - 2 * (column + 1))) / 2, yPosOne-40), 25)
        c.setFill(color)
        c.draw(win)
        x = win.getKey()

        if player==1:
            if x=='a' and column<6:
                column+=1
            elif x=='d' and column>0:
                column-=1
            elif x=='space':
                c.undraw()
                break
        if player == 2:
            if x=='Left' and column<6:
                column+=1
            elif x=='Right' and column>0:
                column-=1
            elif x=='Return':
                c.undraw()
                break

    return column


def playerOne():
    global playerOnePos
    while True:
        playerOnePos = selectColumn(color_rgb(105, 88, 88), 1, playerOnePos)

        if placePiece(playerOnePos, red, 1):
            break

def playerTwo():
    global playerTwoPos
    while True:
        playerTwoPos = selectColumn(color_rgb(105, 105, 105), 2, playerTwoPos)

        if placePiece(playerTwoPos, black, 2):
            break

def placePiece(column, color, player):
    global boardRep, board
    filled = False
    row = 0;
    for x in range(6):
        if boardRep[column][x] == 0:
            boardRep[column][x] = player
            board[column][x].setFill(color)
            row = x
            filled = True
            break

    if filled == False:
        return False
    else:
        checkWin(player, column, row)
        return True

def checkWin(player, column, row):
     #Vertical Check
     checkNum = 1
     if row > 2:
         for x in range(1,4):
             if boardRep[column][row-x] == player:
                 checkNum+=1
         if checkNum == 4:
             roundWin(player)
             return

     checkNum = 1
     #Horizontal Check
     leftCheck = True
     rightCheck = True
     for x in range(1,4):
         if column+x < 7 and rightCheck:
            if boardRep[column+x][row] == player:
                checkNum+=1
            else:
                rightCheck = False
         if column-x >= 0 and leftCheck:
            if boardRep[column-x][row] == player:
                checkNum+=1
            else:
                leftCheck = False
     if checkNum > 3:
         roundWin(player)
         return

     checkNum = 1
     #Bottom-left Top-right Diagonal Check
     topCheck = True
     bottomCheck = True
     for x in range(1, 4):
         if column + x < 7 and row - x >= 0 and topCheck:
             if boardRep[column+x][row-x] == player:
                 checkNum+=1
             else:
                 topCheck = False
         if column-x >= 0 and row+x < 6 and bottomCheck:
             if boardRep[column-x][row+x] == player:
                 checkNum+=1
             else:
                 bottomCheck = False
     if checkNum > 3:
         roundWin(player)
         return

     checkNum = 1
     # Bottom-right Top-left Diagonal Check
     topCheck = True
     bottomCheck = True
     for x in range(1, 4):
         if column + x < 7 and row + x < 6 and topCheck:
             if boardRep[column + x][row + x] == player:
                 checkNum += 1
             else:
                 topCheck = False
         if column - x >= 0 and row - x >= 0 and bottomCheck:
             if boardRep[column - x][row - x] == player:
                 checkNum += 1
             else:
                 bottomCheck = False
     if checkNum > 3:
         roundWin(player)
         return

     return


def roundWin(player):
    global scoreOne, scoreTwo, message

    if(player == 1):
        scoreOne+=1
    else:
        scoreTwo+=1

    displayScoreOne.undraw()
    displayScoreOne.setText(("Player One's Score: " + str(scoreOne)))
    displayScoreOne.draw(win)
    displayScoreTwo.undraw()
    displayScoreTwo.setText(("Player Two's Score: " + str(scoreTwo)))
    displayScoreTwo.draw(win)

    message.setText(("Player " + str(player) + " wins!"))
    messageTwo = Text(Point(width/2, yPosOne-30), "Press any key twice to restart")
    messageTwo.setSize(15)
    messageTwo.setTextColor(color_rgb(255,255,255))
    messageTwo.draw(win)
    win.getKey()
    win.getKey()
    messageTwo.undraw()
    reset()


def test():
    global playerTurn, counter

    while(game==True):
        if(playerTurn == True):
            playerOne()
            playerTurn = False
            counter+=1
        elif (playerTurn == False):
            playerTwo()
            playerTurn = True
            counter+=1

        if counter == 42:
            message.setText(("That's a draw!"))
            messageTwo = Text(Point(width / 2, yPosOne - 30), "Press any key twice to restart")
            messageTwo.setSize(15)
            messageTwo.setTextColor(color_rgb(255, 255, 255))
            messageTwo.draw(win)
            win.getKey()
            win.getKey()
            messageTwo.undraw()
            reset()

def reset():
    global playerTurn, board, boardRep, game, counter
    win.delete("all")
    game==False
    playerTurn = True
    boardRep = [[0] * 6 for x in range(7)]
    game == True
    counter = 0
    boardDisplay()

    test()


if __name__ == '__main__':
    try:
        boardDisplay()
        test()
    except:
        print("Ok")





