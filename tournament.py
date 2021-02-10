from init import get_app, create_app, get_random_string
from flask import Flask, jsonify, request, render_template, abort, session, redirect, url_for
from flask_login import login_required, current_user
from flask_session import Session
from sqlalchemy import or_, and_, update, delete, insert
from flask_sqlalchemy import SQLAlchemy
from database import db_session
from models import User, GameT, gameDetails, userStats, Tournament, Message
import os, ast, models, pdb, string, random
import auth, game_base

app = get_app()

@app.route('/tournament_end_waiting', methods=['POST'])
def tournament_end_waiting():
    tour_query = db_session.query(Tournament)
    tournaments = tour_query.all()
    for tournament in tournaments:
        if tournament.waiting_users != "":
            waiting = ast.literal_eval(tournament.waiting_users)
            if current_user.id in waiting:
                waiting.remove(current_user.id)
                tournament.waiting_users = str(waiting)
                if len(waiting) == 0:
                    tour_query.filter_by(id = tournament.id).delete()
                db_session.commit()
                return "OK"


@app.route('/tournament_getting_players', methods=['GET'])
def tournament():
    tour_query = db_session.query(Tournament)
    tournaments = tour_query.all()
    curr_tour = None
    if tournaments != None:
        for tournament in tournaments:
            if tournament.semi_final == "":
                curr_tour = tournament
            else:
                if tournament.winner == None:
                    if tournament.final != "":
                        if current_user.id in ast.literal_eval(tournament.final):
                            return abort(409)
                    elif tournament.semi_final != "":
                        if current_user.id in ast.literal_eval(tournament.semi_final):
                            return abort(409)
                
    if tournaments == None or curr_tour == None:
        print(len(tournaments))
        tournament = Tournament()
        db_session.add(tournament)

    waiting = []

    if tournament.waiting_users != "":
        waiting = ast.literal_eval(tournament.waiting_users)
        if len(waiting) > 7:
            return abort(409)
    
    current_user.is_waiting= 1
    waiting.append(current_user.id)
    tournament.waiting_users = str(waiting)
    db_session.commit()
    return "OK"
    
    
@app.route("/tournament_matchmaking", methods=['GET'])
def tournament_matchmaking():
    tournaments = db_session.query(Tournament).all()
    for tournament in tournaments:
        if tournament.waiting_users != "":
            waiting = ast.literal_eval(tournament.waiting_users)
            if len(waiting) == 4:
                for i in range(0, 4, 2):
                    game_id = get_random_string(7)
                    gameT = GameT(game_id, waiting[i], waiting[i + 1], tournament.id)
                    db_session.add(gameT)
                    game_details = gameDetails(game_id)
                    db_session.add(game_details)

                tournament.waiting_users = ""
                tournament.semi_final = str(waiting)
                db_session.commit()
                return "OK"
        else:
            if tournament.final == "":
                finalists = []
                games = db_session.query(GameT).all()
                for game in games:
                    if game.tournament_id == tournament.id:
                        game_details = db_session.query(gameDetails).filter_by(game_id = game.id).first()
                        if game_details.winner != None:
                            finalists.append(game_details.winner)

                if len(finalists) < 2:
                    return abort(409)
                
                game_id = get_random_string(7)
                player_one = db_session.query(User).filter_by(id = finalists[0]).first()
                player_two = db_session.query(User).filter_by(id = finalists[1]).first()
                gameT = GameT(game_id, player_one.id, player_two.id, tournament.id)
                db_session.add(gameT)
                game_details = gameDetails(game_id)
                db_session.add(game_details)
                
                tournament.final = str(finalists)
                db_session.commit()
                return "OK"

            elif tournament.winner == None:
                finalists = ast.literal_eval(tournament.final)

                games = db_session.query(GameT).all()
                for game in games:
                    if game.tournament_id == tournament.id and \
                        (finalists[0] == game.w_player or finalists[0] == game.b_player) and \
                        (finalists[1] == game.w_player or finalists[1] == game.b_player):
                        game_details = db_session.query(gameDetails).filter_by(game_id = game.id).first()
                        if game_details.winner != None:
                            tournament.winner = game_details.winner
                            db_session.commit()
                            winner = db_session.query(User).filter_by(id = tournament.winner).first()
                            variable = dict(winner="The winner is " + winner.username + "!")
                            return variable
                        else:
                            return abort(409)
            # elif tournament.winner != None:
            #     winner = db_session.query(User).filter_by(id = tournament.winner).first()
            #     variable = dict(winner="The winner is " + winner.username + "!")
            #     return variable

    return abort(409)