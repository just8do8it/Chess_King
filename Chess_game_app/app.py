from game.run import *
from flask import Flask, jsonify, request, render_template
from database import SQLite
import random

app = Flask(__name__)

game = Game()

@app.route('/', methods=['GET', 'POST'])
def chess():
    command = jsdata = request.get_json()
    
    if isinstance(command, str) == False:
        create_player()
        return render_template('main.html', board=game.chess_board.board)
    else:
        game.run([command])
        template_context = dict(board=game.chess_board.board, 
                        all_figures=game.special_figures,
                        w_won_figures=game.w_player.won_figures,
                        b_won_figures=game.b_player.won_figures);

        return render_template('main.html', **template_context)


@app.route('/createPlayer', methods=['POST'])
def create_player():
    # id = random.choice(range(100, 999))
    # query = "INSERT player (player_id, game_id) VALUES (%d, 0)" %(id,)
    # with SQLite() as db:
    #     cursor = db.execute(query)
    pass

@app.route('/createGame', methods=['POST'])
def create_game():
    # id = random.choice(range(1000, 9999))
    # query = "INSERT game (game_id, move_number) VALUES (%d, 0)" %(id,)
    # with SQLite() as db:
    #     cursor = db.execute(query)
    pass

if __name__=='__main__':
    app.run(debug=True)

