from init import get_app, create_app, get_random_string
from flask import Flask, jsonify, request, render_template, abort, session, redirect, url_for
from flask_login import login_required, current_user
from flask_session import Session
from sqlalchemy import or_, and_, update, delete, insert
from database import db_session
from models import User, GameT, gameDetails, userStats, Tournament, Message
import os, ast, models, pdb, string, random
import auth, game_base

app = get_app()

@app.route("/get_in_game", methods=['GET'])
@login_required
def get_in_game():
    games = db_session.query(GameT).filter(or_(GameT.w_player == current_user.id, 
                                            GameT.b_player == current_user.id)).all()
    
    if games != None:
        for game in games:
            game_details = db_session.query(gameDetails).filter_by(game_id = game.id).first()
            
            if game_details.winner == None:
                first_player = db_session.query(User).filter_by(id = game.w_player).first()
                second_player = db_session.query(User).filter_by(id = game.b_player).first()
                opponent = None
                if current_user == first_player:
                    opponent = second_player
                else:
                    opponent = first_player
                
                if (first_player.is_waiting == 1 and second_player.is_waiting == 1) or opponent.is_playing == 1:
                    current_user.is_waiting = False
                    current_user.is_playing = True
                    db_session.commit()
                    variable = dict(game_id = game.id)
                    return variable

                break
            else:
                if game.tournament_id != None:
                    # tournament = db_session.query(Tournament).filter_by(id = game.tournament_id).first()
                    if game_details.winner == -1.11 * game.w_player or game_details.winner == -1.11 * game.b_player:
                        if current_user.id != int(abs(game_details.winner) / 1.11):
                            current_user.is_waiting = False
                            current_user.is_playing = False
                            game_details.winner = int(game_details.winner / 1.11)
                            db_session.commit()
                            variable = dict(game_id = "http://localhost:5000/play")
                            return variable
                    
    
    return abort(405)


@app.route("/get_online_players", methods=['GET'])
@login_required
def get_online_players():
    user = db_session.query(User).filter(User.is_waiting == True)
    aborting = 0
    if user.count() >= 1:
        first_user = current_user
        second_user = user.first()
        second_user.is_waiting = False
        db_session.commit()

        created_games = db_session.query(GameT).filter(or_(GameT.w_player == first_user.id, 
                                                        GameT.b_player == first_user.id)).all()
        
        if created_games != None:
            for game in created_games:        
                game_details = db_session.query(gameDetails).filter_by(game_id = game.id).first()
                if game_details.winner == None:
                    second_user.is_waiting = True
                    aborting = 1
                    break
        
        if not aborting:
            game_id = get_random_string(7)
            gameT = GameT(game_id, first_user.id, second_user.id)
            db_session.add(gameT)
            game_details = gameDetails(game_id)
            db_session.add(game_details)

            first_user.is_waiting = False
            first_user.is_playing = True

            second_user.is_playing = True

            db_session.commit()
            variables = dict(game_id=game_id)
            return variables
    
    current_user.is_waiting = 1
    db_session.commit()
    return abort(405)