class ChessBoard:
	def __init__(self):
		self.counter = 1
		self.letters = {"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'  ', "H":'  '}
		self.first_row = {"A":'R1', "B":'H1', "C":'B1', "D":'Q1', "E":'K1', "F":'B2', "G":'H2', "H":'R2'}
		self.second_row = {"A":'P1', "B":'P2', "C":'P3', "D":'P4', "E":'P5', "F":'P6', "G":'P7', "H":'P8'}
		self.board = []
		self.white_taken_figures = []
		self.black_taken_figures = []

		for i in range(8):
			if i == 0 or i == 7:
				self.board.append(self.first_row.copy())
			elif i == 1 or i == 6:
				self.board.append(self.second_row.copy()) #if we pass by reference(w/out copy()) black mirrors white
			else:
				self.board.append(self.letters.copy()) 

	def print_board(self):
		print("\n")
		count = 7
		for line in self.board:
			print(" ", count + 1, end = "  ")
			for key in line:
				print("|" + "_" + self.board[count][key] + "_" + "|", end = " ")
			print("\n")
			count -= 1
		print("      ", end = " ")
		for letter in self.letters:
			print(letter + "     ", end = " ")
		print("\n")