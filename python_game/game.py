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
		self.command_counter = None
		self.is_moved = None
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
		w_figures = []
		b_figures = []
		
		names = ["R1", "H1", "B1", "Q1", "K1", "B2", "H2", "R2"]

		for i in range(8):
			w_figures.append(Figure(names[i], chess_board.board, chr(ord('A') + i), 1, "white"))
			b_figures.append(Figure(names[i], chess_board.board, chr(ord('A') + i), 8, "black"))

		for i in range(8):
			w_figures.append(Figure("P" + str(i + 1), chess_board.board, chr(ord('A') + i), 2, "white"))
			b_figures.append(Figure("P" + str(i + 1), chess_board.board, chr(ord('A') + i), 7, "black"))
			

		return w_figures, b_figures

	def make_board_copy(self, curr_player_copy, board_copy):
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
		
		return curr_figures, opponent_figures

	
	def win_condition_check(self, command_passed, chess_board_copy, curr_figures, curr_player_copy, opponent_copy):
		check = 0
		mate = 0
		max_pos = 0
		curr_player_copy.next_positions.clear()
		opponent_copy.next_positions.clear()

		for fig in curr_player_copy.figures:
			fig.update_movable_positions(chess_board_copy.board)
			curr_player_copy.next_positions.append(fig.movable_positions)
		
		for fig in opponent_copy.figures:
			fig.update_movable_positions(chess_board_copy.board)
			opponent_copy.next_positions.append(fig.movable_positions)
		
		for fig in curr_figures:
			if fig.name == "K1":
				fig.update_movable_positions(chess_board_copy.board)
				for opponent_fig in opponent_copy.figures:
					for f_pos in opponent_fig.movable_positions:
						if fig.curr_pos_num == f_pos[0] and fig.curr_pos_ltr == f_pos[1]:
							check += 1
							break
				break
		
		for fig in curr_figures:
			if fig.name == "K1":
				fig.update_movable_positions(chess_board_copy.board)
				max_pos = len(fig.movable_positions)
				for king_move in fig.movable_positions:
					for opponent_fig in opponent_copy.figures:
						if opponent_fig.name[0] == "P":
							chess_board = copy.deepcopy(chess_board_copy)
							source_num = 0
							source_ltr = ""
							pawn = None
							for line in chess_board.board:
								for key in line:
									figure = line[key]
									if figure == None:
										continue
									if figure.name == "K1" and figure.player == curr_player_copy.color:
										source_num = figure.curr_pos_num
										source_ltr = figure.curr_pos_ltr 
										figure.move(king_move[0], king_move[1], 0)
									elif figure.name == opponent_fig.name and figure.player == opponent_copy.color:
										pawn = figure
							
							if pawn != None:
								source_fig = chess_board.board[source_num - 1][chr(source_ltr)]
								chess_board.board[source_num - 1][chr(source_ltr)] = None
								chess_board.board[king_move[0] - 1][king_move[1]] = source_fig

								pawn.update_movable_positions(chess_board.board)
								opponent_fig = pawn

						for f_pos in opponent_fig.movable_positions:
							if king_move[0] == f_pos[0] and king_move[1] == f_pos[1]:
								mate += 1
				break
		
		if not command_passed and check:
			self.ended = -1
		else:
			if self.ended == -1:
				if check or (check and mate == max_pos):
					self.is_moved = 0
					self.ended = 0

		if check and mate:
			curr_figures, opponent_figures = self.make_board_copy(curr_player_copy, chess_board_copy)

			for fig in curr_figures:
				fig.update_movable_positions(chess_board_copy.board)
				curr_player_copy.next_positions.append(fig.movable_positions)
			
			for fig in opponent_figures:
				fig.update_movable_positions(chess_board_copy.board)
				opponent_copy.next_positions.append(fig.movable_positions)

			final_chess_board = chess_board_copy

			for fig in curr_figures:
				for pos in fig.movable_positions:
					chess_board = copy.deepcopy(final_chess_board)
					curr_figures, opponent_figures = self.make_board_copy(curr_player_copy, final_chess_board)

					source_fig = chess_board.board[fig.curr_pos_num - 1][chr(fig.curr_pos_ltr)]
					
					chess_board.board[fig.curr_pos_num - 1][chr(fig.curr_pos_ltr)] = None
					source_fig.move(pos[0], pos[1], 0)
					chess_board.board[pos[0] - 1][pos[1]] = source_fig
					
					curr_figures, opponent_figures = self.make_board_copy(curr_player_copy, chess_board)
					special_check = 0
					
					for figure in curr_figures:
						if figure.name == "K1":
							king = figure
							for opponent_fig in opponent_figures:
								opponent_fig.update_movable_positions(chess_board.board)
								for f_pos in opponent_fig.movable_positions:
									if king.curr_pos_num == f_pos[0] and chr(king.curr_pos_ltr) == f_pos[1]:
										special_check += 1
										break
							break
					if special_check < check:
						mate = 0
		
		if check != 0:
			if mate == max_pos and mate != 0:
				if self.curr_player == self.w_player:
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
		self.command_counter = 0
		self.is_moved = None
		while(1):
			if self.ok == 0 or self.passed == 0:
				self.ok = 1
			self.passed = 0

			self.curr_player = Player("", [])
			command = ""
			if self.command_counter == len(external_commands) - 1:
				self.is_moved = 0
			
			if self.chess_board.counter % 2 == 0:
				self.curr_player = self.b_player
				self.opponent = self.w_player
			else:
				self.curr_player = self.w_player
				self.opponent = self.b_player
			
			if self.command_counter < len(external_commands):
				command = external_commands[self.command_counter]
				if command == "exit":
					break
			else:
				self.win_condition_check(0, copy.deepcopy(self.chess_board), 
											copy.deepcopy(self.curr_player.figures),
											copy.deepcopy(self.curr_player), 
											copy.deepcopy(self.opponent))
				break
			
			self.win_condition_check(0, copy.deepcopy(self.chess_board), 
											copy.deepcopy(self.curr_player.figures),
											copy.deepcopy(self.curr_player), 
											copy.deepcopy(self.opponent))
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
					if result == True:
						self.chess_board.board[src_number - 1][src_letter] = None
						self.chess_board.board[dest_number - 1][dest_letter] = source_fig
						self.passed = 1
						self.is_moved = 1
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
						self.is_moved = 1

			
			if self.ok == 0 or self.passed == 0:
				continue
			else:				
				self.win_condition_check(1, copy.deepcopy(self.chess_board), 
											copy.deepcopy(self.curr_player.figures),
											copy.deepcopy(self.curr_player), 
											copy.deepcopy(self.opponent))
			self.alive_figures = []
			for x in self.w_player.figures:
				if x.is_alive:
					self.alive_figures.append([x.curr_pos_ltr, x.curr_pos_num, x.player])
			for x in self.b_player.figures:
				if x.is_alive:
					self.alive_figures.append([x.curr_pos_ltr, x.curr_pos_num, x.player])

			self.chess_board.counter += 1
			self.command_counter += 1
			
		return self.is_moved
			
# game = Game([], [], None)
# game.run(["E2-E4"])
# game.run(["A7-A5"])
# game.run(["F2-F3", "E7-E5", "G2-G4", "D8-H4"])