import pdb, copy
from board import ChessBoard

class Figure:
	def __init__(self, name, chess_board, start_pos_ltr, start_pos_num, player):
		self.name = name
		self.chess_board = chess_board
		self.board = chess_board.board
		self.start_pos_ltr = ord(start_pos_ltr)
		self.start_pos_num = start_pos_num
		self.curr_pos_ltr = ord(start_pos_ltr)
		self.curr_pos_num = start_pos_num
		self.movable_positions = []
		self.player = player
		self.is_alive = 1


	def update_movable_positions(self, board):
		self.movable_positions.clear()
		if self.is_alive == 0:
			return

		i = 0
		num = None
		ltr = None
		letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

		for line in board:
			z = 0
			for key in line:
				figure = line[key]
				if figure == None:
					num = i + 1
					ltr = letters[z]
				else:
					if figure.player == self.player:
						z += 1
						continue
					num = figure.curr_pos_num
					ltr = chr(figure.curr_pos_ltr)

				result = self.move(num, ltr, 1)
				# if result == None:
					# print(self.name, self.player, self.curr_pos_num, chr(self.curr_pos_ltr), num, ltr)
					# for line in board:
					# 	print("\n", line)
				if (type(result) == bool and result == True) or (type(result) != bool and result[0] == True):					
					self.movable_positions.append((num, ltr))
				
				z += 1
			i += 1



	def move(self, new_pos_num, new_pos_ltr, test):
		if self.is_alive == 0:
			return False
		
		new_ltr = ord(new_pos_ltr)
		
		if self.name == "P1" or self.name == "P2" or \
			self.name == "P3" or self.name == "P4" or \
			self.name == "P5" or self.name == "P6" or \
			self.name == "P7" or self.name == "P8":
				return self.move_pawn(new_pos_num, new_pos_ltr, test, new_ltr)
		
		elif self.name == "R1" or self.name == "R2":
			return self.move_rook(new_pos_num, new_pos_ltr, test, new_ltr)

		elif self.name == "H1" or self.name == "H2":
			return self.move_horse(new_pos_num, new_pos_ltr, test, new_ltr)

		elif self.name == "B1" or self.name == "B2":
			return self.move_bishop(new_pos_num, new_pos_ltr, test, new_ltr)

		elif self.name == "Q1":
			return self.move_queen(new_pos_num, new_pos_ltr, test, new_ltr)

		elif self.name == "K1":
			return self.move_king(new_pos_num, new_pos_ltr, test, new_ltr)


	def move_pawn(self, new_pos_num, new_pos_ltr, test, new_ltr):
		if self.player == "white" and new_ltr == self.curr_pos_ltr and self.curr_pos_num == self.start_pos_num and new_pos_num == self.curr_pos_num + 2 or \
			self.player == "white" and new_ltr == self.curr_pos_ltr and new_pos_num == self.curr_pos_num + 1 or \
			self.player == "white" and new_ltr == self.curr_pos_ltr + 1 and new_pos_num == self.curr_pos_num + 1 or \
			self.player == "white" and new_ltr == self.curr_pos_ltr - 1 and new_pos_num == self.curr_pos_num + 1 or \
			self.player == "black" and new_ltr == self.curr_pos_ltr and self.curr_pos_num == self.start_pos_num and new_pos_num == self.curr_pos_num - 2 or \
			self.player == "black" and new_ltr == self.curr_pos_ltr and new_pos_num == self.curr_pos_num - 1 or \
			self.player == "black" and new_ltr == self.curr_pos_ltr + 1 and new_pos_num == self.curr_pos_num - 1 or \
			self.player == "black" and new_ltr == self.curr_pos_ltr - 1 and new_pos_num == self.curr_pos_num - 1:

				if new_ltr == self.curr_pos_ltr + 1 or new_ltr == self.curr_pos_ltr - 1:
					if self.chess_board.en_passant[0] != None:
						# print("\n\n", self.board[self.curr_pos_num - 1][new_pos_ltr],
						# 		"\n", self.chess_board.en_passant[0])
						if self.name == "P1":
							print(self.curr_pos_num, new_pos_ltr, 
								self.chess_board.en_passant[0].curr_pos_num, 
								chr(self.chess_board.en_passant[0].curr_pos_ltr))
						# print(self.board[self.curr_pos_num][new_pos_ltr].name, self.chess_board.en_passant[0].name)
						if self.board[new_pos_num - 1][new_pos_ltr] == None and \
							self.board[self.curr_pos_num - 1][new_pos_ltr] == self.chess_board.en_passant[0]:
								print("heyyyyyyyyyyyy")
								if test == 0:
									self.curr_pos_num = new_pos_num
									self.curr_pos_ltr = new_ltr
									return True, self.board[new_pos_num - 1][new_pos_ltr]
						else:
							return False
					elif self.board[new_pos_num - 1][new_pos_ltr] != None:
						if test == 0:
							self.curr_pos_num = new_pos_num
							self.curr_pos_ltr = new_ltr
							return True, self.board[new_pos_num - 1][new_pos_ltr]
						else:
							return True
					else:
						return False
				else:
					if new_pos_num == self.curr_pos_num + 2 or new_pos_num == self.curr_pos_num - 2:
						if self.player == "white":
							if self.board[new_pos_num - 2][new_pos_ltr] != None:
								return False
						else:
							if self.board[new_pos_num][new_pos_ltr] != None:
								return False
						
						if chr(new_ltr - 1) < 'A' or (chr(new_ltr - 1) >= 'A' and chr(new_ltr) < 'H'):
							if self.board[new_pos_num - 1][chr(new_ltr + 1)] != None and \
								self.board[new_pos_num - 1][chr(new_ltr + 1)].name[0] == "P":
									# print("shit 1")
									self.chess_board.en_passant = (self.board[new_pos_num - 1][chr(new_ltr + 1)],
													self.chess_board.counter)
									# print("bridge")
						
						if chr(new_ltr + 1) > 'H' or (chr(new_ltr) > 'A' and chr(new_ltr + 1) <= 'H'):
							if self.board[new_pos_num - 1][chr(new_ltr - 1)] != None and \
								self.board[new_pos_num - 1][chr(new_ltr - 1)].name[0] == "P":
									# print("shit 2")
									self.chess_board.en_passant = (self.board[new_pos_num - 1][chr(new_ltr - 1)],
													self.chess_board.counter)

					if self.board[new_pos_num - 1][new_pos_ltr] == None:
						if test == 0:
							self.curr_pos_num = new_pos_num
							self.curr_pos_ltr = new_ltr
						return True
					else:
						return False

		else:
			return False
	

	def move_rook(self, new_pos_num, new_pos_ltr, test, new_ltr):
		if new_pos_num > self.curr_pos_num:
				if self.curr_pos_ltr != new_ltr:
					return False
				for num in range(self.curr_pos_num, new_pos_num - 1):
					if self.board[num][chr(self.curr_pos_ltr)] != None:
						return False	

		elif new_pos_num < self.curr_pos_num:
			if self.curr_pos_ltr != new_ltr:
				return False
			for num in range(new_pos_num, self.curr_pos_num - 1):
				if self.board[num][chr(self.curr_pos_ltr)] != None:
					return False

		elif new_ltr > self.curr_pos_ltr:
			if self.curr_pos_num != new_pos_num:
				return False
			for ltr in range(self.curr_pos_ltr + 1, new_ltr):
				if self.board[self.curr_pos_num - 1][chr(ltr)] != None:
					return False

		elif new_ltr < self.curr_pos_ltr:
			if self.curr_pos_num != new_pos_num:
				return False
			for ltr in range(new_ltr + 1, self.curr_pos_ltr):
				if self.board[self.curr_pos_num - 1][chr(ltr)] != None:
					return False


		if new_pos_num != self.curr_pos_num:
			if test == 0:
				self.curr_pos_num = new_pos_num
			else:
				return True

			if self.board[new_pos_num - 1][new_pos_ltr] != None:
				return True, self.board[new_pos_num - 1][new_pos_ltr]
			else:
				return True

		elif new_ltr != self.curr_pos_ltr:
			if test == 0:
				self.curr_pos_ltr = new_ltr
			else:
				return True

			if self.board[new_pos_num - 1][new_pos_ltr] != None:
				return True, self.board[new_pos_num - 1][new_pos_ltr]
			else:
				return True
		
		else:
			return False
	

	def move_horse(self, new_pos_num, new_pos_ltr, test, new_ltr):
		if new_ltr < self.curr_pos_ltr - 2 or new_ltr > self.curr_pos_ltr + 2 or new_ltr == self.curr_pos_ltr or \
				new_pos_num < self.curr_pos_num - 2 or new_pos_num > self.curr_pos_num + 2 or new_pos_num == self.curr_pos_num:
					return False
		else:
			if abs(new_ltr - self.curr_pos_ltr) == 1 and abs(new_pos_num - self.curr_pos_num) == 1:
				return False
			else:
				if test == 0:
					self.curr_pos_num = new_pos_num
					self.curr_pos_ltr = new_ltr
				else:
					return True
				
				if self.board[new_pos_num - 1][new_pos_ltr] != None:
					return True, self.board[new_pos_num - 1][new_pos_ltr]
				else:
					return True
	
	def move_bishop(self, new_pos_num, new_pos_ltr, test, new_ltr):
		if abs(new_ltr - self.curr_pos_ltr) != abs(new_pos_num - self.curr_pos_num):
				return False
		else:
			num_counter = 0
			ltr_counter = 0
			spec_num_counter = 0
			spec_ltr_counter = 0

			if new_ltr > self.curr_pos_ltr and new_pos_num > self.curr_pos_num:
				spec_num_counter = 1
				spec_ltr_counter = 1
			elif new_ltr > self.curr_pos_ltr and new_pos_num < self.curr_pos_num:
				spec_num_counter = -1
				spec_ltr_counter = 1
			elif new_ltr < self.curr_pos_ltr and new_pos_num < self.curr_pos_num:
				spec_num_counter = -1
				spec_ltr_counter = -1
			elif new_ltr < self.curr_pos_ltr and new_pos_num > self.curr_pos_num:
				spec_num_counter = 1
				spec_ltr_counter = -1

			num_counter += spec_num_counter
			ltr_counter += spec_ltr_counter

			for i in range(abs(new_ltr - self.curr_pos_ltr) - 1):
				if self.board[self.curr_pos_num + num_counter - 1][chr(self.curr_pos_ltr + ltr_counter)] != None:
					return False
				num_counter += spec_num_counter
				ltr_counter += spec_ltr_counter
			
			if test == 0:
				self.curr_pos_num = new_pos_num
				self.curr_pos_ltr = new_ltr
			else:
				return True
			
			if self.board[new_pos_num - 1][new_pos_ltr] != None:
				return True, self.board[new_pos_num - 1][new_pos_ltr]
			else:
				return True


	def move_queen(self, new_pos_num, new_pos_ltr, test, new_ltr):
		if new_ltr == self.curr_pos_ltr:
				if new_pos_num > self.curr_pos_num:
					for num in range(self.curr_pos_num, new_pos_num - 1):
						if self.board[num][chr(self.curr_pos_ltr)] != None:
							return False	

				elif new_pos_num < self.curr_pos_num:
					for num in range(new_pos_num, self.curr_pos_num - 1):
						if self.board[num][chr(self.curr_pos_ltr)] != None:
							return False
				
		elif new_pos_num == self.curr_pos_num:
			if new_ltr > self.curr_pos_ltr:
				for ltr in range(self.curr_pos_ltr + 1, new_ltr):
					if self.board[self.curr_pos_num - 1][chr(ltr)] != None:
						return False

			elif new_ltr < self.curr_pos_ltr:
				for ltr in range(new_ltr + 1, self.curr_pos_ltr):
					if self.board[self.curr_pos_num - 1][chr(ltr)] != None:
						return False

		else:
			if abs(new_ltr - self.curr_pos_ltr) != abs(new_pos_num - self.curr_pos_num):
				return False
			else:
				num_counter = 0
				ltr_counter = 0
				spec_num_counter = 0
				spec_ltr_counter = 0

				if new_ltr > self.curr_pos_ltr and new_pos_num > self.curr_pos_num:
					spec_num_counter = 1
					spec_ltr_counter = 1
				elif new_ltr > self.curr_pos_ltr and new_pos_num < self.curr_pos_num:
					spec_num_counter = -1
					spec_ltr_counter = 1
				elif new_ltr < self.curr_pos_ltr and new_pos_num < self.curr_pos_num:
					spec_num_counter = -1
					spec_ltr_counter = -1
				elif new_ltr < self.curr_pos_ltr and new_pos_num > self.curr_pos_num:
					spec_num_counter = 1
					spec_ltr_counter = -1

				num_counter += spec_num_counter
				ltr_counter += spec_ltr_counter

				for i in range(abs(new_ltr - self.curr_pos_ltr) - 1):
					if self.board[self.curr_pos_num + num_counter - 1][chr(self.curr_pos_ltr + ltr_counter)] != None:
						return False
					# print(self.board[2]['G'])
					num_counter += spec_num_counter
					ltr_counter += spec_ltr_counter

		if test == 0:
			self.curr_pos_num = new_pos_num
			self.curr_pos_ltr = new_ltr
		else:
			return True
		
		if self.board[new_pos_num - 1][new_pos_ltr] != None:
			return True, self.board[new_pos_num - 1][new_pos_ltr]
		else:
			return True

	
	def move_king(self, new_pos_num, new_pos_ltr, test, new_ltr):
		if abs(new_pos_num - self.curr_pos_num) > 1 or abs(new_ltr - self.curr_pos_ltr) > 1:
			if self.curr_pos_num == self.start_pos_num and self.curr_pos_ltr == self.start_pos_ltr and test == 0:
				if new_ltr > self.curr_pos_ltr:
					return False, "forward"
				else:
					return False, "backwards"
			
			return False
		
		if test == 0:
			self.curr_pos_num = new_pos_num
			self.curr_pos_ltr = new_ltr
		else:
			return True

		if self.board[new_pos_num - 1][new_pos_ltr] != None:
			return True, self.board[new_pos_num - 1][new_pos_ltr]
		else:
			return True