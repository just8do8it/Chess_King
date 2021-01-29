from python_game.game import Game
from init import create_app
from flask import Flask, jsonify, request, render_template, abort, session, redirect, url_for
from flask_login import login_required, current_user
from flask_session import Session
from flask_migrate import Migrate
from sqlalchemy import or_, and_, update, delete, insert
from flask_sqlalchemy import SQLAlchemy
from database import db_session
from models import User, GameT, gameDetails, userStats
import os, ast
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
    stats = db_session.query(userStats).filter_by(user_id = current_user.id).first()
    
    if stats.played_games == "":
        return render_template('profile.html', username=current_user.username,
                                            game_count=0,
                                            win_rate=0)

    game_ids = ast.literal_eval(stats.played_games)
    game_count = len(game_ids)
    game_desc = []
    game_dates = []
    game_end = ""
    win_count = 0
    draw_count = 0
    for id in game_ids:
        game = db_session.query(GameT).filter_by(id = id).first()

        opponent = None
        if current_user.id == game.w_player:
            opponent = db_session.query(User).filter_by(id = game.b_player).first()
        else:
            opponent = db_session.query(User).filter_by(id = game.w_player).first()
        
        opponent = opponent.username
        game_desc.append("Game with " + opponent)

        details = db_session.query(gameDetails).filter_by(game_id = id).first()
        game_dates.append(str(details.start_date))
        if details.winner == current_user.username:
            game_end = "win"
            win_count += 1
        elif details.winner == "draw":
            game_end = "draw"
            draw_count += 1
        else:
            game_end = "loss"
    
    win_rate = (win_count + (0.5 * draw_count)) / len(game_ids) * 100

    win_rate = float("{:.2f}".format(win_rate))
    
    return render_template('profile.html', username=current_user.username,
                                            game_count=game_count,
                                            game_ids=game_ids,
                                            games=game_desc,
                                            game_dates=game_dates,
                                            game_end=game_end,
                                            win_rate=win_rate)

@app.route('/replay/<string:game_id>', methods=['GET', 'POST'])
def replay(game_id):
    if request.method == "GET":
        return render_template("replay.html")
    else:
        game = db_session.query(GameT).filter_by(id = game_id).first()
        w_player = db_session.query(User).filter_by(id = game.w_player).first().username
        b_player = db_session.query(User).filter_by(id = game.b_player).first().username
        w_player = "Whites: " + w_player 
        b_player = "Blacks: " + b_player

        game_details = db_session.query(gameDetails).filter_by(game_id = game_id).first()
        moves = ast.literal_eval(game_details.moves)

        variable = request.get_json()
        if isinstance(variable, str) != True:
            return abort(404)
        
        move_counter = int(variable)

        py_game = Game([], [], None)

        if move_counter > len(moves):
            move_counter = len(moves)
            py_game.run(moves)
        else:
            py_game.run(moves[:move_counter])

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

        variables = dict(board=name_board,
                        all_figures=py_game.special_figures,
                        w_won_figures=w_won_figs,
                        b_won_figures=b_won_figs,
                        move_counter=move_counter,
                        w_player=w_player,
                        b_player=b_player)

        return variables


@app.route('/play')
def playroom():
    return render_template('play.html')

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
    games = db_session.query(GameT).filter(or_(GameT.w_player == current_user.id, 
                                            GameT.b_player == current_user.id)).all()
    
    if games:
        for game in games:
            game_details = db_session.query(gameDetails).filter_by(game_id = game.id).first()
            # print("1")
            if game_details.is_active:
                # print("2")
                first_player = db_session.query(User).filter_by(id = game.w_player).first()
                second_player = db_session.query(User).filter_by(id = game.b_player).first()
                opponent = None
                if current_user == first_player:
                    opponent = second_player
                else:
                    opponent = first_player

                if (first_player.waiting == 1 and second_player.waiting == 1) or opponent.is_playing == 1:
                    current_user.waiting = False
                    current_user.is_playing = True
                    db_session.commit()
                    variable = dict(game_id=game.id)
                    return variable

                break
    
    return abort(405)


@app.route("/get_online_players", methods=['GET'])
def get_online_players():
    user = db_session.query(User).filter(User.waiting == True)
    if user.count() >= 1:
        first_user = current_user
        second_user = user.first()

        created_games = db_session.query(GameT).filter(or_(GameT.w_player == first_user.id, 
                                                        GameT.b_player == first_user.id)).all()
        
        if created_games:
            for game in created_games:        
                game_details = db_session.query(gameDetails).filter_by(game_id = game.id).first()
                if game_details.is_active:
                    current_user.waiting = 1
                    db_session.commit()
                    return abort(405)
        
        game_id = get_random_string(7)

        gameT = GameT(game_id, first_user.id, second_user.id)
        db_session.add(gameT)
        game_details = gameDetails(game_id, "", "")
        db_session.add(game_details)

        first_user.waiting = False
        first_user.is_playing = True
        
        second_user.waiting = False
        second_user.is_playing = True

        db_session.commit()

        variables = dict(game_id=game_id)
        return variables
    else:
        current_user.waiting = 1
        db_session.commit()
        return abort(405)


@app.route('/game/<string:game_id>', methods=['GET', 'POST'])
def chess(game_id):
    if request.method == "GET":
        game = db_session.query(GameT).filter_by(id = game_id).first()
        if current_user.id == game.w_player:
            return render_template("game.html")
        else:
            return render_template("b_game.html")
    else:
        py_game = Game([], [], None)       
        variables = {}

        command = request.get_json()
        if isinstance(command, str) != True:
            return abort(404)
        
        commands = []
        details_query = db_session.query(gameDetails).filter_by(game_id = game_id)
        game_details = details_query.first()
        if game_details.moves != "":
            commands = ast.literal_eval(game_details.moves)
        
        if command != "update":
            commands.append(command)
        # print(commands)
        is_moved = py_game.run(commands)        

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

        my_turn = None
        curr_game = db_session.query(GameT).filter_by(id = game_id).first()
        
        stats = db_session.query(userStats).filter_by(user_id = current_user.id).first()
        stats_games = []
        if stats.played_games != "":
            stats_games = ast.literal_eval(stats.played_games)
        
        if is_moved and game_id not in stats_games:
            details_query.update({"moves": str(commands)})
            winner = None
            if py_game.ended == 1:
                stats_query = db_session.query(userStats).filter_by(user_id = current_user.id)
                user_stats = stats_query.first()
                if user_stats.played_games == "":
                    games = []
                else:
                    games = ast.literal_eval(user_stats.played_games)
                
                games.append(curr_game.id)
                stats_query.update({"played_games": str(games)})
                
                
                if py_game.w_checkmate == 1:
                    my_turn = -1
                    winner = db_session.query(User).filter_by(id = curr_game.b_player).first()
                elif py_game.b_checkmate == 1:
                    my_turn = -2
                    winner = db_session.query(User).filter_by(id = curr_game.w_player).first()
                else:
                    my_turn = -3

                if my_turn > -3:
                    details_query.update({"is_active": False, "winner": winner.username})
                else:
                    details_query.update({"is_active": False, "winner": "draw"})
                    
            else:
                if py_game.curr_player.color == "black":
                    if current_user.id == curr_game.b_player:
                        my_turn = 1
                    else:
                        my_turn = 0
                else:
                    if current_user.id == curr_game.w_player:
                        my_turn = 1
                    else:
                        my_turn = 0
        else:
            if py_game.chess_board.counter == 1:
                if py_game.curr_player.color == "white":
                    if current_user.id == curr_game.b_player:
                        my_turn = 0
        
        db_session.commit()
        variables = dict(board=name_board,
                        all_figures=py_game.special_figures,
                        w_won_figures=w_won_figs,
                        b_won_figures=b_won_figs,
                        my_turn=my_turn)
        
        # print("\n")
        # py_game.chess_board.print_board()
        # print("\n")

        return variables

if __name__=='__main__':
    app.run(debug=True)

