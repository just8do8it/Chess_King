import sys, os, copy
sys.path.append(os.getenv('PYTHON_GAME'))
import pdb
import subprocess
import time
from figure import Figure
from player import Player
from board import ChessBoard

subprocess.call("clear")

class Game:
	def __init__(self, w_figs, b_figs, board):
		chess_board = ChessBoard()
		ok = 1
		passed = -1

		if w_figs == [] and b_figs == [] and board == None:
			w_figures, b_figures = self.generate_figures(chess_board)
		else:
			w_figures, b_figures, chess_board = w_figs, b_figs, board
		
		chess_board.change_board(w_figures, b_figures)

		alive_figures = []
		for x in w_figures:
			alive_figures.append([x.curr_pos_ltr, x.curr_pos_num, x.player])
		for x in b_figures:
			alive_figures.append([x.curr_pos_ltr, x.curr_pos_num, x.player])

		w_player = Player("white", w_figures)
		b_player = Player("black", b_figures)

		self.chess_board = chess_board
		self.w_player = w_player
		self.b_player = b_player
		self.curr_player = None
		self.opponent = None
		self.alive_figures = alive_figures
		self.ok = ok
		self.passed = passed
		self.w_check = 0
		self.b_check = 0
		self.w_checkmate = 0
		self.b_checkmate = 0
		self.draw = 0
		self.ended = 0

	def generate_figures(self, chess_board):
		b_figure_1 = Figure("R1", chess_board.board, 'A', 8, "black")
		b_figure_2 = Figure("H1", chess_board.board, 'B', 8, "black")
		b_figure_3 = Figure("B1", chess_board.board, 'C', 8, "black")
		b_figure_4 = Figure("Q1", chess_board.board, 'D', 8, "black")
		b_figure_5 = Figure("K1", chess_board.board, 'E', 8, "black")
		b_figure_6 = Figure("B2", chess_board.board, 'F', 8, "black")
		b_figure_7 = Figure("H2", chess_board.board, 'G', 8, "black")
		b_figure_8 = Figure("R2", chess_board.board, 'H', 8, "black")
		b_figure_9 = Figure("P1", chess_board.board, 'A', 7, "black")
		b_figure_10 = Figure("P2", chess_board.board, 'B', 7, "black")
		b_figure_11 = Figure("P3", chess_board.board, 'C', 7, "black")
		b_figure_12 = Figure("P4", chess_board.board, 'D', 7, "black")
		b_figure_13 = Figure("P5", chess_board.board, 'E', 7, "black")
		b_figure_14 = Figure("P6", chess_board.board, 'F', 7, "black")
		b_figure_15 = Figure("P7", chess_board.board, 'G', 7, "black")
		b_figure_16 = Figure("P8", chess_board.board, 'H', 7, "black")

		w_figure_1 = Figure("R1", chess_board.board, 'A', 1, "white")
		w_figure_2 = Figure("H1", chess_board.board, 'B', 1, "white")
		w_figure_3 = Figure("B1", chess_board.board, 'C', 1, "white")
		w_figure_4 = Figure("Q1", chess_board.board, 'D', 1, "white")
		w_figure_5 = Figure("K1", chess_board.board, 'E', 1, "white")
		w_figure_6 = Figure("B2", chess_board.board, 'F', 1, "white")
		w_figure_7 = Figure("H2", chess_board.board, 'G', 1, "white")
		w_figure_8 = Figure("R2", chess_board.board, 'H', 1, "white")
		w_figure_9 = Figure("P1", chess_board.board, 'A', 2, "white")
		w_figure_10 = Figure("P2", chess_board.board, 'B', 2, "white")
		w_figure_11 = Figure("P3", chess_board.board, 'C', 2, "white")
		w_figure_12 = Figure("P4", chess_board.board, 'D', 2, "white")
		w_figure_13 = Figure("P5", chess_board.board, 'E', 2, "white")
		w_figure_14 = Figure("P6", chess_board.board, 'F', 2, "white")
		w_figure_15 = Figure("P7", chess_board.board, 'G', 2, "white")
		w_figure_16 = Figure("P8", chess_board.board, 'H', 2, "white")

		w_figures = [w_figure_1, w_figure_2, w_figure_3,
					w_figure_4, w_figure_5, w_figure_6, 
					w_figure_7, w_figure_8, w_figure_9, 
					w_figure_10, w_figure_11, w_figure_12, 
					w_figure_13, w_figure_14, w_figure_15, w_figure_16]

		b_figures = [b_figure_1, b_figure_2, b_figure_3,
					b_figure_4, b_figure_5, b_figure_6,
					b_figure_7, b_figure_8, b_figure_9,
					b_figure_10, b_figure_11, b_figure_12,
					b_figure_13, b_figure_14, b_figure_15, b_figure_16]

		return w_figures, b_figures


	def determine_check(self, curr_player, opponent, board, check):
		for fig in self.curr_player.figures:
			if fig.name == "K1":
				for fig_positions in self.opponent.next_positions:
					for f_pos in fig_positions:
						if fig.curr_pos_num == f_pos[0] and chr(fig.curr_pos_ltr) == f_pos[1]:
							check += 1
							break
				break
		
		return check

	def make_board_copy(self, curr_player_copy):
		board_copy = copy.deepcopy(self.chess_board)
		curr_figures = []
		opponent_figures = []

		for line in board_copy.board:
			for key in line:
				figure = line[key]
				if figure != None:
					if figure.player == curr_player_copy.color:
						curr_figures.append(figure)
					else:
						opponent_figures.append(figure)
		
		return board_copy, curr_figures, opponent_figures

	
	def win_condition_check(self):
		check = 0
		mate = 0
		max_pos = 0

		check = self.determine_check(self.curr_player, self.opponent, self.chess_board, 0)
			
		for fig in self.curr_player.figures:
			if fig.name == "K1":
				max_pos = len(fig.movable_positions)
				for king_move in fig.movable_positions:
					for fig_positions in self.opponent.next_positions:
						for f_pos in fig_positions:
							if king_move[0] == f_pos[0] and king_move[1] == f_pos[1]:
								mate += 1

		############################################################
		if check and mate:
			curr_player_copy = copy.deepcopy(self.curr_player)

			board_copy, curr_figures, opponent_figures = self.make_board_copy(curr_player_copy)
			
			for fig in curr_figures:
				for pos in fig.movable_positions:
					board_copy, curr_figures, opponent_figures = self.make_board_copy(curr_player_copy)

					for figure in opponent_figures:
						figure.update_movable_positions(opponent_figures)

					source_fig = board_copy.board[fig.curr_pos_num - 1][chr(fig.curr_pos_ltr)]
					source_fig.move(pos[0], pos[1], 0)

					board_copy.board[fig.curr_pos_num - 1][chr(fig.curr_pos_ltr)] = None
					board_copy.board[pos[0] - 1][pos[1]] = source_fig
					
					# if fig.name == "P7":
					# 	for line in board_copy.board:
					# 		for key in line:
					# 			print(key)
					# 			if line[key] != None:
					# 				print(line[key].name)
					# 			print("\n")
					
					special_check = 0

					for figure in curr_figures:
						if figure.name == "K1":
							king = figure
							for opponent_fig in opponent_figures:
								opponent_fig.update_movable_positions(opponent_figures)
								for f_pos in opponent_fig.movable_positions:
									if king.curr_pos_num == f_pos[0] and chr(king.curr_pos_ltr) == f_pos[1]:
										special_check += 1
										break
									else:
										if source_fig.name == "P4":
											pass
											# print(opponent_fig.name, "\n", opponent_fig.movable_positions, "\n")
										# print(source_fig.name, source_fig.curr_pos_num, chr(source_fig.curr_pos_ltr))
										# print(source_fig.name, source_fig.curr_pos_num, chr(source_fig.curr_pos_ltr))
								break
					
					print("Special check: ", special_check, "Check: ", check, "Mate: ", mate)
					if special_check < check:
						if mate != 0:
							mate -= 1

		############################################################

		if check != 0:
			if mate == max_pos:
				if self.curr_player == self.w_player:
					print("CHECKMATE")
					self.w_checkmate = 1
					self.ended = 1
				else:
					self.b_checkmate = 1
					self.ended = 1
			else:
				if self.curr_player == self.w_player:
					self.w_check = 1
				else:
					self.b_check = 1
		else:
			if self.curr_player == self.w_player:
				self.w_check = 0
			else:
				self.b_check = 0
			if mate == max_pos and mate != 0:
				self.draw = 1
				self.ended = 1

	def run(self, external_commands):
		command_counter = 0
		is_moved = None
		while(1):
			self.curr_player = Player("", [])
			command = ""
			if command_counter == len(external_commands) - 1:
				is_moved = 0

			if self.ok == 0 or self.passed == 0:
				# print("Not a valid command. Try again\n")
				self.ok = 1
			self.passed = 0

			if self.chess_board.counter % 2 == 0:
				#print("\nBlack's turn\n\n")
				self.curr_player = self.b_player
				self.opponent = self.w_player
			else:
				#print("\nWhite's turn\n\n")
				self.curr_player = self.w_player
				self.opponent = self.b_player

			self.opponent.next_positions.clear()
			
			for fig in self.opponent.figures:
				fig.update_movable_positions(self.opponent.figures)
				self.opponent.next_positions.append(fig.movable_positions)
			
			self.win_condition_check()

			if command_counter < len(external_commands):
				command = external_commands[command_counter]
				if command == "exit":
					break
				command_counter += 1
			# else:
			# 	command = input("Enter a command: ")
			else:
				break

			if len(command) != 5:
				self.ok = 0
				continue

			src_letter = command[0]
			src_number = command[1]
			dest_letter = command[3]
			dest_number = command[4]

			if (src_number < '1' and src_number > '8') or \
				src_letter not in self.chess_board.letters.keys() or \
				(dest_number < '1' and dest_number > '8') or \
				dest_letter not in self.chess_board.letters.keys() or \
				len(command) != 5 or \
				command[2] != '-':
					self.ok = 0
					continue
			
			src_number = int(src_number)
			dest_number = int(dest_number)

			source_fig = self.chess_board.board[src_number - 1][src_letter]

			if source_fig == None:
				self.ok = 0
				continue

			if source_fig.player == self.curr_player.color:
				true = True
				result = source_fig.move(dest_number, dest_letter, 0)

				if type(result) == type(true):
					if source_fig.is_alive == 1 and result == True:
						self.chess_board.board[src_number - 1][src_letter] = None
						self.chess_board.board[dest_number - 1][dest_letter] = source_fig
						self.passed = 1
						is_moved = 1
					else:
						self.ok = 0
				else:
					taken_figure_num = result[1]
					taken_figure_ltr = result[2]
					
					killed = 0

					for fig in self.opponent.figures:
						fig_details = [fig.name, fig.curr_pos_ltr, fig.curr_pos_num, fig.player]
						if fig.curr_pos_num == taken_figure_num and \
							fig.curr_pos_ltr == taken_figure_ltr and \
							fig_details not in self.curr_player.won_figures:
								fig.is_alive = 0
								self.curr_player.won_figures.append(fig_details)
								killed = 1
					
					if killed == 0:
						for figure in self.curr_player.figures:
							if source_fig.name == figure.name:
								figure.curr_pos_num = src_number
								figure.curr_pos_ltr = ord(src_letter)
						self.ok = 0
					else:
						self.chess_board.board[src_number - 1][src_letter] = None
						self.chess_board.board[dest_number - 1][dest_letter] = source_fig
						self.passed = 1
						is_moved = 1

			
			if self.ok == 0 or self.passed == 0:
				continue
			
			self.win_condition_check()

			self.alive_figures = []
			for x in self.w_player.figures:
				if x.is_alive:
					self.alive_figures.append([x.curr_pos_ltr, x.curr_pos_num, x.player])
			for x in self.b_player.figures:
				if x.is_alive:
					self.alive_figures.append([x.curr_pos_ltr, x.curr_pos_num, x.player])

			self.chess_board.counter += 1

		return is_moved
			
# game = Game([], [], None)
# game.run(["E2-E4"])
# game.run(["A7-A5"])
# game.run(["F2-F3", "E7-E5", "G2-G4", "D8-H4"])