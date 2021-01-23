from python_game.game import Game
from init import create_app
from flask import Flask, jsonify, request, render_template, abort, session, redirect, url_for
from flask_login import login_required, current_user
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from database import db_session
from models import User, GameT, gameDetails
import os
import models
import pdb
import string, random

import random
import auth

executing = 0
app = create_app()

def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/profile')                   
def profile():
    return render_template('profile.html')

@app.route('/play')
def playroom():
    return render_template('play.html')

@app.route('/start_waiting', methods=['POST'])
def start_waiting():
    current_user.waiting = True
    db_session.commit()
    return "OK"

@app.route('/end_waiting', methods=['POST'])
def end_waiting():
    current_user.waiting = False
    db_session.commit()
    return "OK"

@app.route('/quit_game', methods=['POST'])
def quit_game():
    current_user.is_playing = False
    db_session.commit()
    return "OK"

@app.route("/get_in_game", methods=['GET'])
def get_in_game():
    game_white = db_session.query(GameT).filter_by(w_player = current_user.id).first()
    games_black = db_session.query(GameT).filter_by(b_player = current_user.id).first()
    game = game_white or games_black
    if game:
        variable = dict(game_id=game.id)
        return variable
    else:
        return abort(405)

@app.route("/get_online_players", methods=['GET'])
def get_online_players():
    game = db_session.query(GameT).
    count = db_session.query(User).filter_by(waiting = True).count()
    if count >= 2:
        users = db_session.query(User).filter_by(waiting = True).limit(2)
        first_user = users[0]
        second_user = users[1]
        game_id = get_random_string(7)
        gameT = GameT(game_id, first_user.id, second_user.id)
        db_session.add(gameT)

        first_user.waiting = False
        first_user.is_playing = True
        
        second_user.waiting = False
        second_user.is_playing = True

        db_session.commit()
        variables = dict(game_id=game_id)

        return variables
    else:
        return abort(405)

@app.route('/game/<string:game_id>', methods=['GET', 'POST'])
def chess(game_id):
    if request.method == "GET":
        return render_template("game.html")
    else:
        py_game = Game([], [], None)       
        variables = {}

        command = request.get_json()
        if isinstance(command, str) != True:
            return abort(404)
        
        commands = []
        game_details = db_session.query(gameDetails).filter_by(game_id = game_id)

        if game_details.count():
            game_details = game_details.first()
            commands = game_details.moves.split(',')
        else:
            commands.append(command)
            game_details = gameDetails(game_id, "", "")
            db_session.add(game_details)
            db_session.commit()

        before_board = py_game.chess_board.board
        py_game.run([commands])
        after_board = py_game.chess_board.board
        
        w_won_figs = []
        b_won_figs = []

        name_board = [{}, {}, {}, {}, {}, {}, {}, {}]
        
        for fig in py_game.w_player.won_figures:
            w_won_figs.append(fig.name)

        for fig in py_game.b_player.won_figures:
            b_won_figs.append(fig.name)
        
        counter = 0
        for line in py_game.chess_board.board:
            for key in line:
                if line[key] == None:
                    name_board[counter][key] = "  "
                    continue
                name_board[counter][key] = line[key].name
            counter += 1
        
        if before_board != after_board:
            commands.append(command)
            game_details.update({game_details.moves: str(commands), game_details.board: name_board})
        
        db_session.commit()
        variables = dict(board=name_board, 
                        all_figures=py_game.special_figures,
                        w_won_figures=w_won_figs,
                        b_won_figures=b_won_figs)
        
        print("\n")
        game.chess_board.print_board()
        print("\n")

        return variables

if __name__=='__main__':
    app.run(debug=True)

