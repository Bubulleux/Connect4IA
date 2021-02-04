import tkinter
import numpy.matlib as np

class VisualBoard():
    canvasCells = None
    clkCol = -1
    root = None
    canvas = None

    def __init__(self):
        self.canvasCells = np.ones((7,6), dtype="int8") * -1
        self.clkCol = -1
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, width = 50 * 7, height = 50 * 6)
        # self.canvas.bind('<Button-1>',clk)
        self.canvas.grid(column=0, row=0)

    def updateCell(self ,x, y, _color):
        color = "yellow" if _color == 1 else "red" if _color == -1 else "white"
        if (self.canvasCells[x,y] == -1):
            self.canvasCells[x,y] = self.canvas.create_rectangle(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill = color)
        else:
            self.canvas.itemconfig(self.canvasCells[x,y], fill = color)
        self.root.update()

    def updateAll(self, board):
        for x in range(7):
            for y in range(6):
                self.updateCell(x, y, board[x, y])

    def Close(self):
        self.root.destroy()
    
    # def clk(event):
    #     global clkCol
    #     clkCol = int(event.x / 50)

    # def whereDrop():
    #     global clkCol
    #     clkCol = -1
    #     while clkCol == -1:
    #         root.update()
    #         continue
        
    #     col = clkCol
    #     clkCol = -1
    #     return col

    

    #root.resizable(width=False, height=False)