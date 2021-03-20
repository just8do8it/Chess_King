from init import get_app, create_app, get_random_string
from python_game.game import Game
from init import create_app
from flask import Flask, jsonify, request, render_template, abort, session, redirect, url_for
from flask_login import login_required, current_user
from flask_session import Session
from sqlalchemy import or_, and_, update, delete, insert
from database import db_session
from models import User, GameT, gameDetails, userStats, Tournament, Message
import os, ast, models, pdb, string, random, time
import auth

app = get_app()

@app.route('/quit_game', methods=['POST'])
@login_required
def quit_game():
    current_user.is_playing = False
    db_session.commit()
    return "OK"


@app.route('/game/<string:game_id>/messages', methods=['GET', 'POST'])
@login_required
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
@login_required
def game(game_id):
    game = db_session.query(GameT).filter_by(id = game_id).first()
    if request.method == "GET":
        game = db_session.query(GameT).filter_by(id = game_id).first()
        if current_user.id == game.w_player:
            opponent = db_session.query(User).filter_by(id = game.b_player).first()
            opponent_stats = db_session.query(userStats).filter_by(user_id = game.b_player).first()
            return render_template("whites_game.html", html_page = "whites_game.html", 
                                                    opponent_name = opponent.username,
                                                    opponent_win_rate = opponent_stats.win_rate)
        else:
            opponent = db_session.query(User).filter_by(id = game.w_player).first()
            opponent_stats = db_session.query(userStats).filter_by(user_id = game.w_player).first()
            return render_template("blacks_game.html", html_page = "blacks_game.html", 
                                                    opponent_name = opponent.username,
                                                    opponent_win_rate = opponent_stats.win_rate)
    else:
        py_game = Game([], [], None)       
        variables = {}

        command = request.get_json()
        if isinstance(command, str) != True:
            return abort(404)
        
        winner_is_me = None
        commands = []
        details_query = db_session.query(gameDetails).filter_by(game_id = game_id)
        game_details = details_query.first()
        if game_details.moves != "":
            commands = ast.literal_eval(game_details.moves)

        if command != "update":
            commands.append(command)
        
        is_moved = py_game.run(commands)

        my_turn = None

        if is_moved:
            if command != "update" or (command == "update" and str(commands) == game_details.moves):
               game_details.moves = str(commands)
            db_session.commit()
            winner = None
            if py_game.ended == 1:
                my_turn = -1
                
                if py_game.w_checkmate == 1:
                    winner = db_session.query(User).filter_by(id = game.b_player).first()
                elif py_game.b_checkmate == 1:
                    winner = db_session.query(User).filter_by(id = game.w_player).first()
                else:
                    my_turn = -2

                if my_turn == -1:
                    if winner == current_user:
                        winner_is_me = 1
                    else:
                        winner_is_me = 0
                    game_details.winner = winner.id
                    db_session.commit()
                else:
                    winner_is_me = 2
                    if game.tournament_id == None:
                        game_details.winner = 0
                    else:
                        if game_details.winner == None:
                            w_player_stats = db_session.query(userStats).filter_by(user_id = game.w_player).first()
                            b_player_stats = db_session.query(userStats).filter_by(user_id = game.b_player).first()
                            winner = None
                            if w_player_stats.win_rate > b_player_stats.win_rate:
                                winner = game.w_player
                            elif w_player_stats.win_rate < b_player_stats.win_rate:
                                winner = game.b_player
                            else:
                                winner = random.choice([game.w_player, game.b_player])
                            
                            game_details.winner = -1.11 * winner
                    
                    db_session.commit()
                
                update_win_rate(game.w_player, game)
                update_win_rate(game.b_player, game)
                    
            else:
                if py_game.curr_player.color == "black":
                    if current_user.id == game.b_player:
                        my_turn = 1
                    else:
                        my_turn = 0
                else:
                    if current_user.id == game.w_player:
                        my_turn = 1
                    else:
                        my_turn = 0
        else:
            if py_game.chess_board.counter == 1:
                if py_game.curr_player.color == "white":
                    if current_user.id == game.b_player:
                        my_turn = 0
        

        name_board = [{}, {}, {}, {}, {}, {}, {}, {}]
        
        counter = 0
        for line in py_game.chess_board.board:
            for key in line:
                if line[key] == None:
                    name_board[counter][key] = "  "
                    continue
                name_board[counter][key] = line[key].name
            counter += 1

        taken_figures = py_game.w_player.won_figures + py_game.b_player.won_figures
        
        variables = dict(board = name_board,
                        alive_figures = py_game.alive_figures,
                        taken_figures = taken_figures,
                        my_turn = my_turn,
                        winner_is_me = winner_is_me)

        return variables


def update_win_rate(user_id, game):
    user = db_session.query(User).filter_by(id = user_id).first()
    user.is_waiting = True
    user.is_playing = False
    
    games = []
    stats_query = db_session.query(userStats).filter_by(user_id = user_id)
    stats = stats_query.first()
    if stats.played_games == "":
        games = []
    else:
        games = ast.literal_eval(stats.played_games)
    
    if game.id not in games:
        games.append(game.id)
    stats_query.update({"played_games": str(games)})
    db_session.commit()

    game_ids = ast.literal_eval(stats.played_games)
    game_count = len(game_ids)
    game_endings = []
    win_count = 0
    draw_count = 0
    
    if game_count > 0:
        for id in game_ids:
            details = db_session.query(gameDetails).filter_by(game_id = id).first()
            
            if details.winner == user_id:
                game_endings.append("win")
                win_count += 1
            elif details.winner < 0:
                draw_count += 1
    
    win_rate = (win_count + (0.5 * draw_count)) / len(game_ids) * 100
    
    win_rate = float("{:.2f}".format(win_rate))

    stats_query.update({"win_rate": win_rate})
    db_session.commit()