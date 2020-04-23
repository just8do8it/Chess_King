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

		if self.name == "P1" or self.name == "P2" or \
			self.name == "P3" or self.name == "P4" or \
			self.name == "P5" or self.name == "P6" or \
			self.name == "P7" or self.name == "P8":

				if self.player == "white" and new_ltr == self.curr_pos_ltr and self.curr_pos_num == self.start_pos_num and new_pos_num == self.curr_pos_num + 2 or \
					self.player == "white" and new_ltr == self.curr_pos_ltr and new_pos_num == self.curr_pos_num + 1 or \
					self.player == "white" and new_ltr == self.curr_pos_ltr + 1 and new_pos_num == self.curr_pos_num + 1 or \
					self.player == "white" and new_ltr == self.curr_pos_ltr - 1 and new_pos_num == self.curr_pos_num + 1 or \
					self.player == "black" and self.curr_pos_num == self.start_pos_num and new_pos_num == self.curr_pos_num - 2 or \
					self.player == "black" and new_ltr == self.curr_pos_ltr and new_pos_num == self.curr_pos_num - 1 or \
					self.player == "black" and new_ltr == self.curr_pos_ltr + 1 and new_pos_num == self.curr_pos_num - 1 or \
					self.player == "black" and new_ltr == self.curr_pos_ltr - 1 and new_pos_num == self.curr_pos_num - 1:
					
						if new_ltr == self.curr_pos_ltr + 1 or new_ltr == self.curr_pos_ltr - 1:
							if self.board[new_pos_num - 1][new_pos_ltr] != "  ":
								self.curr_pos_num = new_pos_num
								self.curr_pos_ltr = new_ltr
								return True, new_pos_num, new_ltr
							else:
								return False
						else:
							if self.board[new_pos_num - 1][new_pos_ltr] == "  ":
								self.curr_pos_num = new_pos_num
								self.curr_pos_ltr = new_ltr
								return True
							else:
								return False

				else:
					return False

		elif self.name == "R1" or self.name == "R2":

			if new_pos_num > self.curr_pos_num:
				if self.curr_pos_ltr != new_ltr:
					return False
				for num in range(self.curr_pos_num, new_pos_num - 1):
					if self.board[num][chr(self.curr_pos_ltr)] != "  ":
						return False	

			elif new_pos_num < self.curr_pos_num:
				if self.curr_pos_ltr != new_ltr:
					return False
				for num in range(new_pos_num, self.curr_pos_num - 1):
					if self.board[num][chr(self.curr_pos_ltr)] != "  ":
						return False

			elif new_ltr > self.curr_pos_ltr:
				if self.curr_pos_num != new_pos_num:
					return False
				for ltr in range(self.curr_pos_ltr + 1, new_ltr):
					if self.board[self.curr_pos_num - 1][chr(ltr)] != "  ":
						return False

			elif new_ltr < self.curr_pos_ltr:
				if self.curr_pos_num != new_pos_num:
					return False
				for ltr in range(new_ltr + 1, self.curr_pos_ltr):
					if self.board[self.curr_pos_num - 1][chr(ltr)] != "  ":
						return False


			if new_pos_num != self.curr_pos_num:
				self.curr_pos_num = new_pos_num

				if self.board[new_pos_num - 1][new_pos_ltr] != "  ":
					return True, new_pos_num, new_ltr
				else:
					return True

			elif new_ltr != self.curr_pos_ltr:
				self.curr_pos_ltr = new_ltr

				if self.board[new_pos_num - 1][new_pos_ltr] != "  ":
					return True, new_pos_num, new_ltr
				else:
					return True


		elif self.name == "H1" or self.name == "H2":
			if new_ltr < self.curr_pos_ltr - 2 or new_ltr > self.curr_pos_ltr + 2 or new_ltr == self.curr_pos_ltr or \
				new_pos_num < self.curr_pos_num - 2 or new_pos_num > self.curr_pos_num + 2 or new_pos_num == self.curr_pos_num:
					return False
			else:
				if abs(new_ltr - self.curr_pos_ltr) == 1 and abs(new_pos_num - self.curr_pos_num) == 1:
					return False
				else:
					self.curr_pos_num = new_pos_num
					self.curr_pos_ltr = new_ltr
					
					if self.board[new_pos_num - 1][new_pos_ltr] != "  ":
						return True, new_pos_num, new_ltr
					else:
						return True

		elif self.name == "B1" or self.name == "B2":
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
					if self.board[self.curr_pos_num + num_counter - 1][chr(self.curr_pos_ltr + ltr_counter)] != "  ":
						return False
					num_counter += spec_num_counter
					ltr_counter += spec_ltr_counter
				self.curr_pos_num = new_pos_num
				self.curr_pos_ltr = new_ltr

				if self.board[new_pos_num - 1][new_pos_ltr] != "  ":
					return True, new_pos_num, new_ltr
				else:
					return True


		elif self.name == "Q1":
			if new_ltr == self.curr_pos_ltr:
				if new_pos_num > self.curr_pos_num:
					for num in range(self.curr_pos_num, new_pos_num - 1):
						if self.board[num][chr(self.curr_pos_ltr)] != "  ":
							return False	

				elif new_pos_num < self.curr_pos_num:
					for num in range(new_pos_num, self.curr_pos_num - 1):
						if self.board[num][chr(self.curr_pos_ltr)] != "  ":
							return False
				
			elif new_pos_num == self.curr_pos_num:
				if new_ltr > self.curr_pos_ltr:
					for ltr in range(self.curr_pos_ltr + 1, new_ltr):
						if self.board[self.curr_pos_num - 1][chr(ltr)] != "  ":
							return False

				elif new_ltr < self.curr_pos_ltr:
					for ltr in range(new_ltr + 1, self.curr_pos_ltr):
						if self.board[self.curr_pos_num - 1][chr(ltr)] != "  ":
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
						if self.board[self.curr_pos_num + num_counter - 1][chr(self.curr_pos_ltr + ltr_counter)] != "  ":
							return False
						num_counter += spec_num_counter
						ltr_counter += spec_ltr_counter

			
			self.curr_pos_num = new_pos_num
			self.curr_pos_ltr = new_ltr

			if self.board[new_pos_num - 1][new_pos_ltr] != "  ":
				return True, new_pos_num, new_ltr
			else:
				return True

		elif self.name == "K1":
			if abs(new_pos_num - self.curr_pos_num) > 1 or abs(new_ltr - self.curr_pos_ltr) > 1:
				return False

			self.curr_pos_num = new_pos_num
			self.curr_pos_ltr = new_ltr

			if self.board[new_pos_num - 1][new_pos_ltr] != "  ":
				return True, new_pos_num, new_ltr
			else:
				return True