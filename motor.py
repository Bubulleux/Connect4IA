import display
from colorama import Back
import numpy as np


# Y =  1
# R = -1

class Connect4:
	plyTurn = -1
	win = 0
	plyStart = 0
	board = np.zeros((7, 6), dtype="int8")

	visual_board = None

	def __init__(self, show_board=True):
		self.board = np.zeros((7, 6), dtype="int8")
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
		self.plyStart = -1 if np.random.rand() > 0.5 else 1
		self.plyTurn = self.plyStart
		if show_board:
			self.visual_board = display.VisualBoard()
			self.visual_board.update_all(self.board)

	def drop_coin(self, x, color):
		for i in range(6):
			if self.board[x, i + 1] != 0 or i == 4:
				y = 5 if self.board[x, i + 1] == 0 else i
				self.board[x, y] = color
				if self.visual_board is not None:
					# self.visualBoard.updateCell(x , y, color)
					self.visual_board.update_all(self.board)
				break

	def play(self, play_column):
		if self.board[play_column, 0] != 0 and self.win == 0:
			return self.observation(), -10, True
		self.drop_coin(play_column, self.plyTurn)
		win = win_play(self.board, play_column)
		if win:
			self.win = self.plyTurn
		else:
			self.plyTurn *= -1
		return self.observation(), 10 if win and self.plyTurn != self.plyStart else 3 if win else 0, win

	def close_game(self):
		if self.visual_board is not None:
			self.visual_board.close()

	def observation(self):
		return self.board.copy().reshape((42, 1))

	def print(self):
		print()
		print_board(self.board)


def win_play(board, play_col):
	x = play_col
	y = 0
	for _y in range(6):
		if board[x, _y] != 0:
			y = _y
			break
	if board[x, y] != 0:
		dirs = [[1, 1], [0, 1], [-1, 1], [1, 0]]
		for curDir in dirs:
			align = 0
			for i in range(-3, 4):
				_x = x + (curDir[0] * i)
				_y = y + (curDir[1] * i)
				if _x < 0 or _y < 0 or _x > 6 or _y > 5:
					continue
				if board[_x, _y] == board[x, y]:
					align += 1
				else:
					align = 0
				if align == 4:
					return True
	return False


def print_board(board):
	for y in range(6):
		for i in range(2):
			pr = ""
			for x in range(7):
				color = Back.YELLOW if board[x, y] == 1 else Back.RED if board[x, y] == -1 else Back.WHITE
				pr = pr + f"{color}    {Back.RESET}"
			print(pr)
