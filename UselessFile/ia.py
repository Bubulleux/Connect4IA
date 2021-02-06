import random
import motor
import numpy.matlib as np

class Play():
    board = []
    x = 0
    team = 0
    win = 0
    playAfter = [ 0 for i in range(7)]
    prevision = 0
    winRate = 0
    child = 0
    def calcPlay(self, board, x, team):
        self.team = team
        self.board = playHere(board, x, team)
        self.win = motor.winPlay(self.board.copy(), x)
        self.x = x
        self.winRate = 0
        self.playAfter = []
        if self.prevision < 3 and self.win != 1:
            #print(self.prevision)
            for x in range(7):
                if self.board[x,0] == 0:
                    self.child +=1 
                    curPlay = Play()
                    curPlay.prevision = self.prevision + 1
                    curPlay.calcPlay(self.board.copy(), x, -1 if self.team == 1 else 1)
                    if curPlay.winRate != 0:
                        self.playAfter.append(curPlay)
        self.winRate = 0
        if self.win:
            self.winRate = 1
        elif len(self.playAfter) == 0:
            #print("winRate = 0")
            self.winRate = 0
        else:
            #print(len(self.playAfter))
            total = 0
            i = 0
            pr = ""
            for play in self.playAfter:
                if play != 0 and play.winRate != 0:
                    total += play.winRate
                    i+= 1
                    pr+= "  " + str(play.winRate)
            if i != 0:
                self.winRate = total / i * -1
                #print(f"winrate: {self.winRate}, total: {total}, count value: {i}, result : {pr}, prevision = {self.prevision}")
        if self.winRate != 100:
            #print(("    " * self.prevision) + f"x : {self.x}, winrate: {self.winRate}, Prevision: {self.prevision}, Count PlayAfter {len(self.playAfter)}")
            pass

def whereDrop(_board):
    bestPlay = None
    for x in range(7):
        curPlay = Play()
        curPlay.calcPlay(_board.copy(), x, 1)
        if bestPlay == None:
            bestPlay = curPlay
        if curPlay.winRate > bestPlay.winRate:
            bestPlay = curPlay
        #Printboard(curPlay.board)
        #print(f"win: {curPlay.winRate}, x: {x}")
    return bestPlay.x

def playHere(_board, x, color):
    for i in range(6):
        #print(f"pos: ({x},{i+1}) ")
        if _board[x,i + 1] != 0 or i == 4:
            y = 5 if _board[x,i + 1] == 0 else i
            _board[x,y] =  color
            #print(f"i: {i}")
            break
    return _board




def Printboard(board):
    for y in range(6):
        pr = ""
        for x in range(7):
            pr = pr + str(board[x,y]) +  "   "
        print(pr)