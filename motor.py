import display
import ia
import colorama
import numpy.matlib as np
import time
import Train

class Connect4():
    plyTurn = -1
    win = 0
    #board = [[0 for y in range(6)] for x in range(7)]
    board : np.matrix= np.zeros((7,6), dtype="int8")
    
    #Y =  1
    #R = -1
    visualBoard = None

    def __init__(self, showBoard = True):
        self.board = np.zeros((7,6), dtype="int8")
        # self.board = np.matrix([
        #     [ 0,  0,  0,  0, -1, -1],
        #     [ 0,  0,  1,  1,  1,  1],
        #     [ 0,  1, -1,  1,  1, -1],
        #     [ 0,  0,  0, -1, -1, -1],
        #     [ 0,  0, -1, -1,  1,  1],
        #     [ 0,  0,  0,  0,  1,  1],
        #     [ 0,  0,  0,  0, -1, -1],
        # ])
        self.win = 0
        self.plyTurn = -1
        if showBoard:
            self.visualBoard = display.VisualBoard()
            self.visualBoard.updateAll(self.board)
    
    def dropCoin(self, x, color):
        for i in range(6):
            if self.board[x,i + 1] != 0 or i == 4:
                y = 5 if self.board[x,i + 1] == 0 else i
                self.board[x,y] =  color
                #print(f"i: {i}")
                if self.visualBoard != None:
                    #self.visualBoard.updateCell(x , y, color)
                    self.visualBoard.updateAll(self.board)
                break
    
    
                
    
    def Play(self, playColumn):
        if self.board[playColumn, 0] != 0 and self.win == 0:
            return self.Observation(), -1, True
        self.dropCoin(playColumn, self.plyTurn)
        win = winPlay(self.board, playColumn)
        if win:
            self.win = self.plyTurn
        else:
            self.plyTurn *= -1
        return self.Observation(), 10 if win else 0, win
    
    def CloseGame(self):
        if self.visualBoard != None:
            self.visualBoard.Close()

    def Observation(self):
        return self.board.copy().reshape((42,1))
    
    
def winPlay(board, playCol):
    x = playCol
    y = 0
    for _y in range(6):
        if board[x,_y] != 0:
            y = _y
            break
    #Printboard(board)
    #print(y)
    if board[x,y] != 0:
        dirrs = [[1, 1], [0, 1], [-1, 1], [1, 0]]
        for curDir in dirrs:
            aligne = 0
            for i in range(-3, 4):
                _x = x + (curDir[0] * i)
                _y = y + (curDir[1] * i)
                if _x < 0 or _y < 0 or _x > 6 or _y > 5:
                    #print("skip")
                    continue
                #print(f"{_y}, {_x}, {len(board)},{len(board[0])}")
                if board[_x,_y] == board[x,y]:
                    aligne += 1
                else:
                    aligne = 0
                if aligne == 4:
                    return True
    return False


def Printboard(board):
        for y in range(6):
            pr = ""
            for x in range(7):
                pr = pr + str(board[x,y]) +  "   "
            print(pr)