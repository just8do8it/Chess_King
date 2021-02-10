from init import get_app, create_app, get_random_string
from python_game.game import Game
from init import create_app
from flask import Flask, jsonify, request, render_template, abort, session, redirect, url_for
from flask_login import login_required, current_user
from flask_session import Session
from sqlalchemy import or_, and_, update, delete, insert
from flask_sqlalchemy import SQLAlchemy
from database import db_session
from models import User, GameT, gameDetails, userStats, Tournament, Message
import os, ast, models, pdb, string, random
import auth

app = get_app()

@app.route('/quit_game', methods=['POST'])
def quit_game():
    game = db_session.query(GameT).filter(or_(GameT.w_player == current_user.id,
                                                GameT.b_player == current_user.id)).first()
    
    game_details = db_session.query(gameDetails).filter_by(game_id = game.id).first()
    if game_details.is_active:
        user_stats = db_session.query(userStats).filter_by(user_id = current_user.id).first()
        games = ast.literal_eval(user_stats.played_games)
        games.remove(game.id)
        user_stats.played_games = str(games)

    current_user.is_playing = False
    db_session.commit()
    return "OK"


@app.route('/game/<string:game_id>/messages', methods=['GET', 'POST'])
def message(game_id):
    if request.method == "GET":
        chat = []
        for message, user in db_session.query(Message, User).filter(and_(Message.user_id == User.id, 
                                                            Message.game_id == game_id)).all():

            time = str(message.time)
            time = time[11:16]
            chat.append("(" + time + ") " + user.username + ": " + message.text)
        
        return dict(chat=chat)
    
    text = request.get_json()
    message = Message(current_user.id, game_id, text)
    db_session.add(message)
    db_session.commit()
    return "OK"

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
                    details_query.update({"is_active": False, "winner": winner.id})
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
