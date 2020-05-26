import unittest
from main import Game

class TestGame(unittest.TestCase):
	def test_rook(self):
		moves = ["D2-D10", "D2-D5", "D2-D1", "D2-D4", "G7-G6", "D4-D3", "D4-C3", "D4-C4", "D4-C5", "D4-E5", "D4-E4",
				"D4-E3", "D4-D5", "C7-C6", "D5-C6", "exit"]
		
		board = [
			{"A":'R1', "B":'H1', "C":'B1', "D":'Q1', "E":'K1', "F":'B2', "G":'H2', "H":'R2'},
			
			{"A":'P1', "B":'P2', "C":'P3', "D":'  ', "E":'P5', "F":'P6', "G":'P7', "H":'P8'},
			
			{"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'  ', "H":'  '},
			
			{"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'  ', "H":'  '},
			
			{"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'  ', "H":'  '},
			
			{"A":'  ', "B":'  ', "C":'P4', "D":'  ', "E":'  ', "F":'  ', "G":'P7', "H":'  '},
			
			{"A":'P1', "B":'P2', "C":'  ', "D":'P4', "E":'P5', "F":'P6', "G":'  ', "H":'P8'},
			
			{"A":'R1', "B":'H1', "C":'B1', "D":'Q1', "E":'K1', "F":'B2', "G":'H2', "H":'R2'}
		]

		game = Game()
		game.run(moves)

		self.assertEqual(game.chess_board.board, board)

	def test_basic_movement(self):
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
			{"A":'  ', "B":'H1', "C":'B1', "D":'  ', "E":'K1', "F":'  ', "G":'H2', "H":'R2'},
			
			{"A":'  ', "B":'P2', "C":'  ', "D":'P4', "E":'  ', "F":'P6', "G":'  ', "H":'P8'},
			
			{"A":'  ', "B":'Q1', "C":'  ', "D":'B2', "E":'  ', "F":'  ', "G":'  ', "H":'  '},
			
			{"A":'  ', "B":'  ', "C":'P4', "D":'  ', "E":'  ', "F":'  ', "G":'P8', "H":'  '},
			
			{"A":'R1', "B":'P1', "C":'  ', "D":'  ', "E":'  ', "F":'P5', "G":'  ', "H":'  '},
			
			{"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'  ', "H":'H2'},
			
			{"A":'P1', "B":'  ', "C":'P3', "D":'  ', "E":'P5', "F":'K1', "G":'P7', "H":'  '},

			{"A":'R1', "B":'H1', "C":'B1', "D":'Q1', "E":'  ', "F":'B2', "G":'  ', "H":'R2'}

		]

		game = Game()
		game.run(moves)

		self.assertEqual(game.chess_board.board, board)




	def test_taking_figures(self):
		moves = [
				"A2-A4", "B7-B5", "C2-C4", "D7-D5", "E2-E4", "F7-F5", # moving the pawns 
				"G2-G4", "H7-H5", "A4-B5", "D5-C4", "E4-F5", "H5-G4", # out of the way
				"A1-A7", "A8-A7", "F1-C4", "E8-F7", "C4-E6", "F7-E6", 
				"B1-A3", "D8-D2", "C1-D2", "G8-H6", "E1-E2", "H6-F5", "exit"
			]
		
		board = [
			{"A":'  ', "B":'  ', "C":'  ', "D":'Q1', "E":'  ', "F":'  ', "G":'H2', "H":'R2'},
			
			{"A":'  ', "B":'P2', "C":'  ', "D":'B1', "E":'K1', "F":'P6', "G":'  ', "H":'P8'},
			
			{"A":'H1', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'  ', "H":'  '},
			
			{"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'P8', "H":'  '},
			
			{"A":'  ', "B":'P1', "C":'  ', "D":'  ', "E":'  ', "F":'H2', "G":'  ', "H":'  '},
			
			{"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'K1', "F":'  ', "G":'  ', "H":'  '},
			
			{"A":'R1', "B":'  ', "C":'P3', "D":'  ', "E":'P5', "F":'  ', "G":'P7', "H":'  '},
			
			{"A":'  ', "B":'H1', "C":'B1', "D":'  ', "E":'  ', "F":'B2', "G":'  ', "H":'R2'}
		]

		game = Game()
		game.run(moves)

		self.assertEqual(game.chess_board.board, board)
		self.assertEqual(game.w_player.won_figures, ["P2", "P6", "P1", "P4", "Q1"])
		self.assertEqual(game.b_player.won_figures, ["P3", "P7", "R1", "B2", "P4", "P5"])

	def test_end(self):
		pass

if __name__ == "__main__":
	unittest.main()


	# {"A":'R1', "B":'H1', "C":'B1', "D":'Q1', "E":'K1', "F":'B2', "G":'H2', "H":'R2'},

	# {"A":'P1', "B":'P2', "C":'P3', "D":'P4', "E":'P5', "F":'P6', "G":'P7', "H":'P8'},

	# {"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'  ', "H":'  '},

	# {"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'  ', "H":'  '},

	# {"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'  ', "H":'  '},
	
	# {"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'  ', "H":'  '},
	
	# {"A":'P1', "B":'P2', "C":'P3', "D":'P4', "E":'P5', "F":'P6', "G":'P7', "H":'P8'},

	# {"A":'R1', "B":'H1', "C":'B1', "D":'Q1', "E":'K1', "F":'B2', "G":'H2', "H":'R2'}



	# {"A":'  ', "B":'H1', "C":'B1', "D":'  ', "E":'  ', "F":'B2', "G":'  ', "H":'R2'},

	# {"A":'R1', "B":'  ', "C":'P3', "D":'  ', "E":'P5', "F":'  ', "G":'P7', "H":'  '},

	# {"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'K1', "F":'  ', "G":'  ', "H":'  '},

	# {"A":'  ', "B":'P1', "C":'  ', "D":'  ', "E":'  ', "F":'H2', "G":'  ', "H":'  '},

	# {"A":'  ', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'P8', "H":'  '},
	
	# {"A":'H1', "B":'  ', "C":'  ', "D":'  ', "E":'  ', "F":'  ', "G":'  ', "H":'  '},
	
	# {"A":'  ', "B":'P2', "C":'  ', "D":'B1', "E":'K1', "F":'P6', "G":'  ', "H":'P8'},

	# {"A":'  ', "B":'  ', "C":'  ', "D":'Q1', "E":'  ', "F":'B2', "G":'H2', "H":'R2'}