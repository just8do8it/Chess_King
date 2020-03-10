import subprocess
from chess_board import ChessBoard
from figure import Figure
from player import Player

subprocess.call("clear")
chess = ChessBoard()
ok = 1

w_figure_1 = Figure("R1", chess.board, "A", 8)
w_figure_2 = Figure("H1", chess.board, "B", 8)
w_figure_3 = Figure("B1", chess.board, "C", 8)
w_figure_4 = Figure("Q1", chess.board, "D", 8)
w_figure_5 = Figure("K1", chess.board, "E", 8)
w_figure_6 = Figure("B2", chess.board, "F", 8)
w_figure_7 = Figure("H2", chess.board, "G", 8)
w_figure_8 = Figure("R2", chess.board, "H", 8)
w_figure_9 = Figure("P1", chess.board, "A", 7)
w_figure_10 = Figure("P2", chess.board, "B", 7)
w_figure_11 = Figure("P3", chess.board, "C", 7)
w_figure_12 = Figure("P4", chess.board, "D", 7)
w_figure_13 = Figure("P5", chess.board, "E", 7)
w_figure_14 = Figure("P6", chess.board, "F", 7)
w_figure_15 = Figure("P7", chess.board, "G", 7)
w_figure_16 = Figure("P8", chess.board, "H", 7)

b_figure_1 = Figure("R1", chess.board, "A", 1)
b_figure_2 = Figure("H1", chess.board, "B", 1)
b_figure_3 = Figure("B1", chess.board, "C", 1)
b_figure_4 = Figure("Q1", chess.board, "D", 1)
b_figure_5 = Figure("K1", chess.board, "E", 1)
b_figure_6 = Figure("B2", chess.board, "F", 1)
b_figure_7 = Figure("H2", chess.board, "G", 1)
b_figure_8 = Figure("R2", chess.board, "H", 1)
b_figure_9 = Figure("P1", chess.board, "A", 2)
b_figure_10 = Figure("P2", chess.board, "B", 2)
b_figure_11 = Figure("P3", chess.board, "C", 2)
b_figure_12 = Figure("P4", chess.board, "D", 2)
b_figure_13 = Figure("P5", chess.board, "E", 2)
b_figure_14 = Figure("P6", chess.board, "F", 2)
b_figure_15 = Figure("P7", chess.board, "G", 2)
b_figure_16 = Figure("P8", chess.board, "H", 2)

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


while 1:
	curr_player = Player("", [])

	subprocess.call("clear")
	chess.print_board()

	if ok == 0:
		print("Not a valid command. Try again\n")

	if chess.counter % 2 == 0:
		print("\nBlack's turn\n\n")
		curr_player = b_player
	else:
		print("\nWhite's turn\n\n")
		curr_player = w_player

	command = input("Enter a command: ")

	if len(command) != 5:
		continue

	src_letter = command[0]
	src_number = command[1] 
	dest_letter = command[3]
	dest_number = command[4]

	if (src_number < '1' and src_number > '8') or \
		src_letter not in chess.letters.keys() or \
		(dest_number < '1' and dest_number > '8') or \
		dest_letter not in chess.letters.keys() or \
		len(command) != 5 or \
		command[2] != '-':
			ok = 0
			continue

	src_number = int(src_number)
	dest_number = int(dest_number)

	figure_print = chess.board[src_number - 1][src_letter]
	if figure_print == '  ':
		ok = 0
		continue

	for figure in curr_player.figures:
		if figure.name == figure_print:
			if figure.is_alive == 1 and figure.move(dest_letter, dest_number) == True:
				chess.board[src_number - 1][src_letter] = '  '
				chess.board[dest_number - 1][dest_letter] = figure_print
			else:
				ok = 0
				break

	if ok == 0:
		continue

	ok = 1
	chess.counter += 1