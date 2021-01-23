import pdb

class ChessBoard:
	def __init__(self):
		self.counter = 1
		self.letters = {"A": None, "B": None, "C": None, "D": None, "E": None, "F": None, "G": None, "H": None}
		self.board = []

		for i in range(8):
			self.board.append(self.letters.copy())

	def change_board(self, w_fig, b_fig):
		j = 0
		for i in range(2):
			for key in self.board[i]:
				self.board[i][key] = w_fig[j]
				j = j + 1
		
		j = 0
		for i in range(7, 5, -1):
			for key in self.board[i]:
				self.board[i][key] = b_fig[j]
				j = j + 1


	def print_board(self):
		print("\n")
		counter = 7
		for line in self.board:
			print(" ", counter + 1, end = "  ")
			for key in line:
				if self.board[counter][key] == None:
					print("|" + "_" + "  " + "_" + "|", end = " ")
				elif self.board[counter][key].player == "white":
					print("|" + "_" + self.board[counter][key].name + "_" + "|", end = " ")
				else:
					print("|" + "_" + '\033[33m' + self.board[counter][key].name + '\033[m' + "_" + "|", end = " ")
				
			print("\n")
			counter -= 1
		print("      ", end = " ")
		for letter in self.letters:
			print(letter + "     ", end = " ")
		print("\n")