import subprocess
import time
from chess_board import ChessBoard
from figure import Figure
from player import Player

subprocess.call("clear")
chess_board = ChessBoard()
ok = 1
passed = -1

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


w_player = Player("white", w_figures)
b_player = Player("black", b_figures)


class Game:
	def __init__(self, chess_board, w_player, b_player, ok, passed):
		self.chess_board = chess_board
		self.w_player = w_player
		self.b_player = b_player
		self.ok = ok
		self.passed = passed

	def run(self, external_commands):
		command_counter = 0

		while 1:
			curr_player = Player("", [])
			command = ""

			#subprocess.call("clear")

			print("White's player won figures: ", end="")
			print(", ".join(self.w_player.won_figures))
			print("Black's player won figures: " + '\033[m', end="")
			print(", ".join(self.b_player.won_figures))
			self.chess_board.print_board(b_player)

			if self.ok == 0 or self.passed == 0:
				print("Not a valid command. Try again\n")
				self.ok = 1
			self.passed = 0

			if self.chess_board.counter % 2 == 0:
				print("\nBlack's turn\n\n")
				curr_player = b_player
			else:
				print("\nWhite's turn\n\n")
				curr_player = w_player
			

			if command_counter < len(external_commands):
				command = external_commands[command_counter]
				command_counter += 1
			else:
				command = input("Enter a command: ")
			

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

			figure_print = self.chess_board.board[src_number - 1][src_letter]
			if figure_print == '  ':
				#print("blank")
				self.ok = 0
				continue

			#time.sleep(1)

			for figure in curr_player.figures:
				if figure.name == figure_print and figure.player == curr_player.color and \
					chr(figure.curr_pos_ltr) == src_letter and figure.curr_pos_num == src_number:
						true = True
						result = figure.move(dest_letter, dest_number)

						if type(result) == type(true):
							if figure.is_alive == 1 and result == True:
								#print("case 1")
								self.chess_board.board[src_number - 1][src_letter] = '  '
								self.chess_board.board[dest_number - 1][dest_letter] = figure_print
								self.passed = 1
								break
							else:
								print("not moved correctly")
								self.ok = 0
								break
						else:
							taken_figure_num = result[1]
							taken_figure_ltr = result[2]
							
							killed = 0

							if curr_player.color == "white":
								for fig in self.b_player.figures:
									if fig.curr_pos_num == taken_figure_num and \
										fig.curr_pos_ltr == taken_figure_ltr:
											fig.is_alive = 0
											self.w_player.won_figures.append(fig.name)
											killed = 1
							else:
								for fig in self.w_player.figures:
									if fig.curr_pos_num == taken_figure_num and \
										fig.curr_pos_ltr == taken_figure_ltr:
											fig.is_alive = 0
											self.b_player.won_figures.append(fig.name)
											killed = 1
							if killed == 0:
								self.ok = 0
							else:
								self.chess_board.board[src_number - 1][src_letter] = '  '
								self.chess_board.board[dest_number - 1][dest_letter] = figure_print
								self.passed = 1

							break

			if self.ok == 0 or self.passed == 0:
				continue

			self.chess_board.counter += 1


pre_moves = ["A2-A4", "B7-B5", "A4-B5", "C7-C6", "E2-E4", "D8-A5"]

game = Game(chess_board, w_player, b_player, ok, passed)
game.run(pre_moves)