import sqlite3 as sqlite

DB_NAME = "chess.db"

conn = sqlite.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS game
	(
		game_id INTEGER,
		move_number TEXT
	)
''')
conn.commit()

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS commands
	(
		game_id INTEGER,
		moves TEXT
	)
''')
conn.commit()

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS player
	(
		player_id INTEGER,
		game_id INTEGER
	)
''')
conn.commit()

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS runningGame
	(
		game_id INTEGER,
		player1_id INTEGER,
		player2_id INTEGER,
		curr_player_id INTEGER
	)
''')
conn.commit()

class SQLite(object):
	def __enter__(self):
		self.conn = sqlite.connect(DB_NAME)
		return self.conn.cursor()

	def __exit__(self, type, value, traceback):
		self.conn.commit()