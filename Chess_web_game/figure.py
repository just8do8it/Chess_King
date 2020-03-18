class Figure:
	def __init__(self, name, board, start_pos_ltr, start_pos_num, player):
		self.name = name
		self.board = board
		self.start_pos_ltr = ord(start_pos_ltr)
		self.start_pos_num = start_pos_num
		self.curr_pos_ltr = ord(start_pos_ltr)
		self.curr_pos_num = start_pos_num
		self.player = player
		self.is_alive = 1

	def move(self, new_pos_ltr, new_pos_num):
		new_ltr = ord(new_pos_ltr)

		if self.player == "white":
			if self.name == "P1" or self.name == "P2" or \
				self.name == "P3" or self.name == "P4" or \
				self.name == "P5" or self.name == "P6" or \
				self.name == "P7" or self.name == "P8":
					if self.curr_pos_num == self.start_pos_num and new_pos_num == self.curr_pos_num + 2:
						if self.board[new_pos_num - 1][new_pos_ltr] == "  ":
							self.curr_pos_num += 2
							return True
						else:
							#print("not moving forward")
							return False
					if new_ltr == self.curr_pos_ltr and new_pos_num == self.curr_pos_num + 1:
						if self.board[new_pos_num - 1][new_pos_ltr] == "  ":
							self.curr_pos_num += 1
							return True
						else:
							#print("not moving forward")
							return False
					elif new_ltr == self.curr_pos_ltr + 1 and new_pos_num == self.curr_pos_num + 1:
						if self.board[new_pos_num - 1][new_pos_ltr] != "  ":
							self.curr_pos_ltr += 1
							self.curr_pos_num += 1
							return True, self.board[new_pos_num - 1][new_pos_ltr]
						else:
							return False
					elif new_ltr == self.curr_pos_ltr - 1 and new_pos_num == self.curr_pos_num + 1:
						if self.board[new_pos_num - 1][new_pos_ltr] != "  ":
							self.curr_pos_ltr -= 1
							self.curr_pos_num += 1
							return True, self.board[new_pos_num - 1][new_pos_ltr]
						else:
							#print("not taking opponent")
							return False
					else:
						print("not in right direction at all")
						return False

			else:
				return False

		elif self.player == "black":
			if self.name == "P1" or self.name == "P2" or \
				self.name == "P3" or self.name == "P4" or \
				self.name == "P5" or self.name == "P6" or \
				self.name == "P7" or self.name == "P8":
					if self.curr_pos_num == self.start_pos_num and new_pos_num == self.curr_pos_num - 2:
						if self.board[new_pos_num - 1][new_pos_ltr] == "  ":
							self.curr_pos_num -= 2
							return True
						else:
							#print("not moving forward")
							return False
					if new_ltr == self.curr_pos_ltr and new_pos_num == self.curr_pos_num - 1:
						if self.board[new_pos_num - 1][new_pos_ltr] == "  ":
							self.curr_pos_num -= 1
							return True
						else:
							#print("not moving forward")
							return False
					elif new_ltr == self.curr_pos_ltr + 1 and new_pos_num == self.curr_pos_num - 1:
						if self.board[new_pos_num - 1][new_pos_ltr] != "  ":
							self.curr_pos_ltr += 1
							self.curr_pos_num -= 1
							return True, self.board[new_pos_num - 1][new_pos_ltr]
						else:
							return False
					elif new_ltr == self.curr_pos_ltr - 1 and new_pos_num == self.curr_pos_num - 1:
						if self.board[new_pos_num - 1][new_pos_ltr] != "  ":
							self.curr_pos_ltr -= 1
							self.curr_pos_num -= 1
							return True, self.board[new_pos_num - 1][new_pos_ltr]
						else:
							#print("not taking opponent")
							return False
					else:
						print("not in right direction at all")
						return False

			else:
				return False
