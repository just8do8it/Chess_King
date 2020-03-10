class Figure:
	def __init__(self, name, board, start_pos_num, start_pos_ltr):
		self.name = name
		self.board = board
		self.start_pos_ltr = start_pos_ltr
		self.start_pos_num = start_pos_num
		self.curr_pos_ltr = start_pos_ltr
		self.curr_pos_num = start_pos_num
		self.is_alive = 1

	def move(self, new_pos_ltr, new_pos_num):
		print(self.name)
		if self.name == "P1" or self.name == "P2" or \
			self.name == "P3" or self.name == "P4" or \
			self.name == "P5" or self.name == "P6" or \
			self.name == "P7" or self.name == "P8":
				if new_pos_ltr == self.curr_pos_ltr and new_pos_num == self.curr_pos_num + 1:
					self.curr_pos_num += 1
					return True
				elif new_pos_ltr == self.curr_pos_ltr + 1:

				else:
					return False

		else:
			return False
