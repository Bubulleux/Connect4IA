import tkinter
import numpy as np


class VisualBoard:
	canvasCells = None
	clkCol = -1
	root = None
	canvas = None

	def __init__(self):
		self.canvasCells = np.ones((7, 6), dtype="int8") * -1
		self.clkCol = -1
		self.root = tkinter.Tk()
		self.canvas = tkinter.Canvas(self.root, width=50 * 7, height=50 * 6)
		# self.canvas.bind('<Button-1>',clk)
		self.canvas.grid(column=0, row=0)
		self.root.resizable(width=False, height=False)

	def update_cell(self, x, y, _color):
		color = "yellow" if _color == 1 else "red" if _color == -1 else "white"
		if self.canvasCells[x, y] != -1:
			self.canvas.itemconfig(self.canvasCells[x, y], fill=color)
		else:
			self.canvasCells[x, y] = self.canvas.create_rectangle(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill=color)
		self.root.update()

	def update_all(self, board):
		for x in range(7):
			for y in range(6):
				self.update_cell(x, y, board[x, y])

	def close(self):
		self.root.destroy()
