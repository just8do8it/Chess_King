import unittest
from game import Game
from figure import Figure
from board import ChessBoard

def reverse_board(board):
	new_board = []
	for i in range(8):
		new_board.append(board[7 - i]) 
	
	return new_board

class TestGame(unittest.TestCase):
	def test_rook(self):

		chess_board = ChessBoard()

		b_R1 = Figure("R1", chess_board.board, 'A', 8, "black")
		b_H1 = Figure("H1", chess_board.board, 'B', 8, "black")
		b_B1 = Figure("B1", chess_board.board, 'C', 8, "black")
		b_Q1 = Figure("Q1", chess_board.board, 'D', 8, "black")
		b_K1 = Figure("K1", chess_board.board, 'E', 8, "black")
		b_B2 = Figure("B2", chess_board.board, 'F', 8, "black")
		b_H2 = Figure("H2", chess_board.board, 'G', 8, "black")
		b_R2 = Figure("R2", chess_board.board, 'H', 8, "black")
		b_P1 = Figure("P1", chess_board.board, 'A', 7, "black")
		b_P2 = Figure("P2", chess_board.board, 'B', 7, "black")
		b_P3 = Figure("P3", chess_board.board, 'C', 7, "black")
		b_P4 = Figure("P4", chess_board.board, 'D', 7, "black")
		b_P5 = Figure("P5", chess_board.board, 'E', 7, "black")
		b_P6 = Figure("P6", chess_board.board, 'F', 7, "black")
		b_P7 = Figure("P7", chess_board.board, 'G', 7, "black")
		b_P8 = Figure("P8", chess_board.board, 'H', 7, "black")

		w_R1 = Figure("R1", chess_board.board, 'A', 1, "white")
		w_H1 = Figure("H1", chess_board.board, 'B', 1, "white")
		w_B1 = Figure("B1", chess_board.board, 'C', 1, "white")
		w_Q1 = Figure("Q1", chess_board.board, 'D', 1, "white")
		w_K1 = Figure("K1", chess_board.board, 'E', 1, "white")
		w_B2 = Figure("B2", chess_board.board, 'F', 1, "white")
		w_H2 = Figure("H2", chess_board.board, 'G', 1, "white")
		w_R2 = Figure("R2", chess_board.board, 'H', 1, "white")
		w_P1 = Figure("P1", chess_board.board, 'A', 2, "white")
		w_P2 = Figure("P2", chess_board.board, 'B', 2, "white")
		w_P3 = Figure("P3", chess_board.board, 'C', 2, "white")
		w_P4 = Figure("P4", chess_board.board, 'D', 2, "white")
		w_P5 = Figure("P5", chess_board.board, 'E', 2, "white")
		w_P6 = Figure("P6", chess_board.board, 'F', 2, "white")
		w_P7 = Figure("P7", chess_board.board, 'G', 2, "white")
		w_P8 = Figure("P8", chess_board.board, 'H', 2, "white")

		w_figs = [w_R1, w_H1, w_B1, w_Q1, w_K1, w_B2, w_H2, w_R2, w_P1, w_P2, w_P3, w_P4, w_P5, w_P6, w_P7, w_P8]
		b_figs = [b_R1, b_H1, b_B1, b_Q1, b_K1, b_B2, b_H2, b_R2, b_P1, b_P2, b_P3, b_P4, b_P5, b_P6, b_P7, b_P8]

		moves = ["D2-D10", "D2-D5", "D2-D1", "D2-D4", "G7-G6", "D4-D3", "D4-C3", "D4-C4", "D4-C5", "D4-E5", "D4-E4",
				"D4-E3", "D4-D5", "C7-C6", "D5-C6", "exit"]
		
		board = [
			{"A":b_R1, "B":b_H1, "C":b_B1, "D":b_Q1, "E":b_K1, "F":b_B2, "G":b_H2, "H":b_R2},
			
			{"A":b_P1, "B":b_P2, "C":None, "D":b_P4, "E":b_P5, "F":b_P6, "G":None, "H":b_P8},
			
			{"A":None, "B":None, "C":w_P4, "D":None, "E":None, "F":None, "G":b_P7, "H":None},
			
			{"A":None, "B":None, "C":None, "D":None, "E":None, "F":None, "G":None, "H":None},
			
			{"A":None, "B":None, "C":None, "D":None, "E":None, "F":None, "G":None, "H":None},
			
			{"A":None, "B":None, "C":None, "D":None, "E":None, "F":None, "G":None, "H":None},
			
			{"A":w_P1, "B":w_P2, "C":w_P3, "D":None, "E":w_P5, "F": w_P6, "G":w_P7, "H":w_P8},
			
			{"A":w_R1, "B":w_H1, "C":w_B1, "D":w_Q1, "E":w_K1, "F":w_B2, "G":w_H2, "H":w_R2}
		]

		board = reverse_board(board)

		game = Game(w_figs, b_figs, chess_board)
		game.run(moves)

		self.assertEqual(game.chess_board.board, board)

	def test_basic_movement(self):
		chess_board = ChessBoard()

		b_R1 = Figure("R1", chess_board.board, 'A', 8, "black")
		b_H1 = Figure("H1", chess_board.board, 'B', 8, "black")
		b_B1 = Figure("B1", chess_board.board, 'C', 8, "black")
		b_Q1 = Figure("Q1", chess_board.board, 'D', 8, "black")
		b_K1 = Figure("K1", chess_board.board, 'E', 8, "black")
		b_B2 = Figure("B2", chess_board.board, 'F', 8, "black")
		b_H2 = Figure("H2", chess_board.board, 'G', 8, "black")
		b_R2 = Figure("R2", chess_board.board, 'H', 8, "black")
		b_P1 = Figure("P1", chess_board.board, 'A', 7, "black")
		b_P2 = Figure("P2", chess_board.board, 'B', 7, "black")
		b_P3 = Figure("P3", chess_board.board, 'C', 7, "black")
		b_P4 = Figure("P4", chess_board.board, 'D', 7, "black")
		b_P5 = Figure("P5", chess_board.board, 'E', 7, "black")
		b_P6 = Figure("P6", chess_board.board, 'F', 7, "black")
		b_P7 = Figure("P7", chess_board.board, 'G', 7, "black")
		b_P8 = Figure("P8", chess_board.board, 'H', 7, "black")

		w_R1 = Figure("R1", chess_board.board, 'A', 1, "white")
		w_H1 = Figure("H1", chess_board.board, 'B', 1, "white")
		w_B1 = Figure("B1", chess_board.board, 'C', 1, "white")
		w_Q1 = Figure("Q1", chess_board.board, 'D', 1, "white")
		w_K1 = Figure("K1", chess_board.board, 'E', 1, "white")
		w_B2 = Figure("B2", chess_board.board, 'F', 1, "white")
		w_H2 = Figure("H2", chess_board.board, 'G', 1, "white")
		w_R2 = Figure("R2", chess_board.board, 'H', 1, "white")
		w_P1 = Figure("P1", chess_board.board, 'A', 2, "white")
		w_P2 = Figure("P2", chess_board.board, 'B', 2, "white")
		w_P3 = Figure("P3", chess_board.board, 'C', 2, "white")
		w_P4 = Figure("P4", chess_board.board, 'D', 2, "white")
		w_P5 = Figure("P5", chess_board.board, 'E', 2, "white")
		w_P6 = Figure("P6", chess_board.board, 'F', 2, "white")
		w_P7 = Figure("P7", chess_board.board, 'G', 2, "white")
		w_P8 = Figure("P8", chess_board.board, 'H', 2, "white")

		w_figs = [w_R1, w_H1, w_B1, w_Q1, w_K1, w_B2, w_H2, w_R2, w_P1, w_P2, w_P3, w_P4, w_P5, w_P6, w_P7, w_P8]
		b_figs = [b_R1, b_H1, b_B1, b_Q1, b_K1, b_B2, b_H2, b_R2, b_P1, b_P2, b_P3, b_P4, b_P5, b_P6, b_P7, b_P8]

		moves = [
				"A2-A4", "B7-B5", "C2-C4", "D7-D5", "E2-E4", "F7-F5", # moving the pawns 
				"G2-G4", "H7-H5", "A4-B5", "D5-C4", "E4-F5", "H5-G4", # out of the way
				"A1-C1", "A1-A10", "A1-B3", "A1-C3", "A1-A5", # rook movement
				"G8-G7", "G8-G5", "G8-H7", "G8-F5", "G8-H6", # horse movement 
				"A5-D5", "C1-B2", "C1-A3", "C1-D2", "C1-F4", "C1-C3", # bishop movement
				"D1-D2", "D1-D4", "D1-H5", "D1-B3", # queen movement 
				"E8-E7", "E8-E5", "E8-F8", "E8-F7", # king movement
				"F1-D3", "exit" # last bishop move
			]
		
		board = [
			{"A":b_R1, "B":b_H1, "C":b_B1, "D":b_Q1, "E":None, "F":b_B2, "G":None, "H":b_R2},

			{"A":b_P1, "B":None, "C":b_P3, "D":None, "E":b_P5, "F":b_K1, "G":b_P7, "H":None},

			{"A":None, "B":None, "C":None, "D":None, "E":None, "F":None, "G":None, "H":b_H2},

			{"A":w_R1, "B":w_P1, "C":None, "D":None, "E":None, "F":w_P5, "G":None, "H":None},

			{"A":None, "B":None, "C":b_P4, "D":None, "E":None, "F":None, "G":b_P8, "H":None},
			
			{"A":None, "B":w_Q1, "C":None, "D":w_B2, "E":None, "F":None, "G":None, "H":None},
			
			{"A":None, "B":w_P2, "C":None, "D":w_P4, "E":None, "F":w_P6, "G":None, "H":w_P8},

			{"A":None, "B":w_H1, "C":w_B1, "D":None, "E":w_K1, "F":None, "G":w_H2, "H":w_R2}

		]

		board = reverse_board(board)

		game = Game(w_figs, b_figs, chess_board)
		game.run(moves)

		self.assertEqual(game.chess_board.board, board)




	def test_taking_figures(self):
		chess_board = ChessBoard()

		b_R1 = Figure("R1", chess_board.board, 'A', 8, "black")
		b_H1 = Figure("H1", chess_board.board, 'B', 8, "black")
		b_B1 = Figure("B1", chess_board.board, 'C', 8, "black")
		b_Q1 = Figure("Q1", chess_board.board, 'D', 8, "black")
		b_K1 = Figure("K1", chess_board.board, 'E', 8, "black")
		b_B2 = Figure("B2", chess_board.board, 'F', 8, "black")
		b_H2 = Figure("H2", chess_board.board, 'G', 8, "black")
		b_R2 = Figure("R2", chess_board.board, 'H', 8, "black")
		b_P1 = Figure("P1", chess_board.board, 'A', 7, "black")
		b_P2 = Figure("P2", chess_board.board, 'B', 7, "black")
		b_P3 = Figure("P3", chess_board.board, 'C', 7, "black")
		b_P4 = Figure("P4", chess_board.board, 'D', 7, "black")
		b_P5 = Figure("P5", chess_board.board, 'E', 7, "black")
		b_P6 = Figure("P6", chess_board.board, 'F', 7, "black")
		b_P7 = Figure("P7", chess_board.board, 'G', 7, "black")
		b_P8 = Figure("P8", chess_board.board, 'H', 7, "black")

		w_R1 = Figure("R1", chess_board.board, 'A', 1, "white")
		w_H1 = Figure("H1", chess_board.board, 'B', 1, "white")
		w_B1 = Figure("B1", chess_board.board, 'C', 1, "white")
		w_Q1 = Figure("Q1", chess_board.board, 'D', 1, "white")
		w_K1 = Figure("K1", chess_board.board, 'E', 1, "white")
		w_B2 = Figure("B2", chess_board.board, 'F', 1, "white")
		w_H2 = Figure("H2", chess_board.board, 'G', 1, "white")
		w_R2 = Figure("R2", chess_board.board, 'H', 1, "white")
		w_P1 = Figure("P1", chess_board.board, 'A', 2, "white")
		w_P2 = Figure("P2", chess_board.board, 'B', 2, "white")
		w_P3 = Figure("P3", chess_board.board, 'C', 2, "white")
		w_P4 = Figure("P4", chess_board.board, 'D', 2, "white")
		w_P5 = Figure("P5", chess_board.board, 'E', 2, "white")
		w_P6 = Figure("P6", chess_board.board, 'F', 2, "white")
		w_P7 = Figure("P7", chess_board.board, 'G', 2, "white")
		w_P8 = Figure("P8", chess_board.board, 'H', 2, "white")

		w_figs = [w_R1, w_H1, w_B1, w_Q1, w_K1, w_B2, w_H2, w_R2, w_P1, w_P2, w_P3, w_P4, w_P5, w_P6, w_P7, w_P8]
		b_figs = [b_R1, b_H1, b_B1, b_Q1, b_K1, b_B2, b_H2, b_R2, b_P1, b_P2, b_P3, b_P4, b_P5, b_P6, b_P7, b_P8]
		
		moves = [
			"A2-A4", "B7-B5", "C2-C4", "D7-D5", "E2-E4", "F7-F5", # moving the pawns 
			"G2-G4", "H7-H5", "A4-B5", "D5-C4", "E4-F5", "H5-G4", # out of the way
			"A1-A7", "A8-A7", "F1-C4", "E8-F7", "C4-E6", "F7-E6", 
			"B1-A3", "D8-D2", "C1-D2", "G8-H6", "E1-E2", "H6-F5", "exit"
		]
		
		board = [
			{"A":None, "B":b_H1, "C":b_B1, "D":None, "E":None, "F":b_B2, "G":None, "H":b_R2},

			{"A":b_R1, "B":None, "C":b_P3, "D":None, "E":b_P5, "F":None, "G":b_P7, "H":None},

			{"A":None, "B":None, "C":None, "D":None, "E":b_K1, "F":None, "G":None, "H":None},

			{"A":None, "B":w_P1, "C":None, "D":None, "E":None, "F":b_H2, "G":None, "H":None},

			{"A":None, "B":None, "C":None, "D":None, "E":None, "F":None, "G":b_P8, "H":None},
			
			{"A":w_H1, "B":None, "C":None, "D":None, "E":None, "F":None, "G":None, "H":None},
			
			{"A":None, "B":w_P2, "C":None, "D":w_B1, "E":w_K1, "F":w_P6, "G":None, "H":w_P8},

			{"A":None, "B":None, "C":None, "D":w_Q1, "E":None, "F":None, "G":w_H2, "H":w_R2}
		]

		board = reverse_board(board)

		game = Game(w_figs, b_figs, chess_board)
		game.run(moves)

		self.assertEqual(game.chess_board.board, board)
		self.assertEqual(game.w_player.won_figures, [b_P2, b_P6, b_P1, b_P4, b_Q1])
		self.assertEqual(game.b_player.won_figures, [w_P3, w_P7, w_R1, w_B2, w_P4, w_P5])

	def test_end(self):
		chess_board = ChessBoard()

		b_R1 = Figure("R1", chess_board.board, 'A', 8, "black")
		b_H1 = Figure("H1", chess_board.board, 'B', 8, "black")
		b_B1 = Figure("B1", chess_board.board, 'C', 8, "black")
		b_Q1 = Figure("Q1", chess_board.board, 'D', 8, "black")
		b_K1 = Figure("K1", chess_board.board, 'E', 8, "black")
		b_B2 = Figure("B2", chess_board.board, 'F', 8, "black")
		b_H2 = Figure("H2", chess_board.board, 'G', 8, "black")
		b_R2 = Figure("R2", chess_board.board, 'H', 8, "black")
		b_P1 = Figure("P1", chess_board.board, 'A', 7, "black")
		b_P2 = Figure("P2", chess_board.board, 'B', 7, "black")
		b_P3 = Figure("P3", chess_board.board, 'C', 7, "black")
		b_P4 = Figure("P4", chess_board.board, 'D', 7, "black")
		b_P5 = Figure("P5", chess_board.board, 'E', 7, "black")
		b_P6 = Figure("P6", chess_board.board, 'F', 7, "black")
		b_P7 = Figure("P7", chess_board.board, 'G', 7, "black")
		b_P8 = Figure("P8", chess_board.board, 'H', 7, "black")

		w_R1 = Figure("R1", chess_board.board, 'A', 1, "white")
		w_H1 = Figure("H1", chess_board.board, 'B', 1, "white")
		w_B1 = Figure("B1", chess_board.board, 'C', 1, "white")
		w_Q1 = Figure("Q1", chess_board.board, 'D', 1, "white")
		w_K1 = Figure("K1", chess_board.board, 'E', 1, "white")
		w_B2 = Figure("B2", chess_board.board, 'F', 1, "white")
		w_H2 = Figure("H2", chess_board.board, 'G', 1, "white")
		w_R2 = Figure("R2", chess_board.board, 'H', 1, "white")
		w_P1 = Figure("P1", chess_board.board, 'A', 2, "white")
		w_P2 = Figure("P2", chess_board.board, 'B', 2, "white")
		w_P3 = Figure("P3", chess_board.board, 'C', 2, "white")
		w_P4 = Figure("P4", chess_board.board, 'D', 2, "white")
		w_P5 = Figure("P5", chess_board.board, 'E', 2, "white")
		w_P6 = Figure("P6", chess_board.board, 'F', 2, "white")
		w_P7 = Figure("P7", chess_board.board, 'G', 2, "white")
		w_P8 = Figure("P8", chess_board.board, 'H', 2, "white")

		w_figs = [w_R1, w_H1, w_B1, w_Q1, w_K1, w_B2, w_H2, w_R2, w_P1, w_P2, w_P3, w_P4, w_P5, w_P6, w_P7, w_P8]
		b_figs = [b_R1, b_H1, b_B1, b_Q1, b_K1, b_B2, b_H2, b_R2, b_P1, b_P2, b_P3, b_P4, b_P5, b_P6, b_P7, b_P8]

		moves = ["E2-E4", "F7-F6", "D2-D4", "G7-G5", "D1-H5", "exit"]

		board = [
			{"A":b_R1, "B":b_H1, "C":b_B1, "D":b_Q1, "E":b_K1, "F":b_B2, "G":b_H2, "H":b_R2},

			{"A":b_P1, "B":b_P2, "C":b_P3, "D":b_P4, "E":b_P5, "F":None, "G":None, "H":b_P8},

			{"A":None, "B":None, "C":None, "D":None, "E":None, "F":b_P6, "G":None, "H":None},

			{"A":None, "B":None, "C":None, "D":None, "E":None, "F":None, "G":b_P7, "H":w_Q1},

			{"A":None, "B":None, "C":None, "D":w_P4, "E":w_P5, "F":None, "G":None, "H":None},
			
			{"A":None, "B":None, "C":None, "D":None, "E":None, "F":None, "G":None, "H":None},
			
			{"A":w_P1, "B":w_P2, "C":w_P3, "D":None, "E":None, "F":w_P6, "G":w_P7, "H":w_P8},

			{"A":w_R1, "B":w_H1, "C":w_B1, "D":None, "E":w_K1, "F":w_B2, "G":w_H2, "H":w_R2}
		]

		board = reverse_board(board)

		game = Game(w_figs, b_figs, chess_board)
		game.run(moves)

		self.assertEqual(game.b_checkmate, 1)

if __name__ == "__main__":
	unittest.main()


	# {"A":b_R1', "B":b_H1, "C":b_B1, "D":b_Q1, "E":b_K1, "F":b_B2, "G":b_H2, "H":b_R2},

	# {"A":b_P1, "B":b_P2, "C":b_P3, "D":b_P4, "E":b_P5, "F":b_P6, "G":b_P7, "H":b_P8},

	# {"A":None, "B":None, "C":None, "D":None, "E":None, "F":None, "G":None, "H":None},

	# {"A":None, "B":None, "C":None, "D":None, "E":None, "F":None, "G":None, "H":None},

	# {"A":None, "B":None, "C":None, "D":None, "E":None, "F":None, "G":None, "H":None},
	
	# {"A":None, "B":None, "C":None, "D":None, "E":None, "F":None, "G":None, "H":None},
	
	# {"A":w_P1, "B":w_P2, "C":w_P3, "D":w_P4, "E":w_P5, "F":w_P6, "G":w_P7, "H":w_P8},

	# {"A":w_R1, "B":w_H1, "C":w_B1, "D":w_Q1, "E":w_K1, "F":w_B2, "G":w_H2, "H":w_R2}
