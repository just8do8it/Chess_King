from init import get_app, create_app, get_random_string
from flask import Flask, jsonify, request, render_template, abort, session, redirect, url_for
from flask_login import login_required, current_user
from flask_session import Session
from sqlalchemy import or_, and_, update, delete, insert
from database import db_session
from models import User, GameT, gameDetails, userStats, Tournament, Message
import os, ast, models, pdb, string, random, copy
import auth, game_base

app = get_app()

@app.route('/tournament_end_waiting', methods=['POST'])
@login_required
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
    
    return abort(409)


@app.route('/tournament_getting_players', methods=['GET'])
@login_required
def tournament_getting_players():
    tour_query = db_session.query(Tournament)
    tournaments = tour_query.all()
    curr_tour = None
    if tournaments != None:
        for tournament in tournaments:
            if tournament.semi_final == "":
                curr_tour = tournament
                break
            else:
                if tournament.winner == None:
                    if tournament.final != "":
                        if current_user.id in ast.literal_eval(tournament.final):
                            return abort(409)
                    elif tournament.semi_final != "":
                        if current_user.id in ast.literal_eval(tournament.semi_final):
                            return abort(409)
                    elif tournament.quarter_final != "":
                        if current_user.id in ast.literal_eval(tournament.quarter_final):
                            return abort(409)
                
    if tournaments == None or curr_tour == None:
        tournament = Tournament()
        db_session.add(tournament)

    waiting = []

    if tournament.waiting_users != "":
        waiting = ast.literal_eval(tournament.waiting_users)
        if len(waiting) > 7:
            return abort(409)
    
    current_user.is_waiting = 1
    if tournament.quarter_final != "":
        return abort(409)
    
    waiting.append(current_user.id)
    tournament.waiting_users = str(waiting)
    db_session.commit()
    return "OK"
    
    
@app.route("/tournament_matchmaking", methods=['GET'])
@login_required
def tournament_matchmaking():
    tournaments = db_session.query(Tournament).all()
    curr_tour = None

    for tournament in tournaments:
        games = db_session.query(GameT).filter_by(tournament_id = tournament.id).all()
        for game in games:
            if (current_user.id == game.w_player or current_user.id == game.b_player) and \
                (tournament.winner == None or type(tournament.winner) is float):
                    curr_tour = tournament
                    break
                
        if curr_tour != None:
            break

    if curr_tour == None:
        for tournament in tournaments:
            if tournament.waiting_users != "":
                return start_quarter_final(tournament)    
    
    else:
        games = db_session.query(GameT).filter_by(tournament_id = curr_tour.id).all()
        
        if curr_tour.semi_final == "":
            tournament.semi_final = "Calculating..."
            db_session.commit()
            return start_semi_final(curr_tour, games)
        
        elif curr_tour.final == "" and curr_tour.semi_final != "Calculating..." and curr_tour.semi_final != "":
            tournament.final = "Calculating..."
            db_session.commit()
            return start_final(curr_tour, games)

        elif curr_tour.winner == None and curr_tour.final != "Calculating..." and curr_tour.final != "":
            return determine_winner(curr_tour, games)

        elif curr_tour.winner != None:
            return winner_notifier(curr_tour, games)
    
    return abort(409)


def start_quarter_final(tournament):
    waiting = copy.deepcopy(ast.literal_eval(tournament.waiting_users))
    if len(waiting) == 8:
        tournament.waiting_users = ""
        for i in range(0, 8, 2):
            game_id = get_random_string(7)
            gameT = GameT(game_id, waiting[i], waiting[i + 1], tournament.id)
            db_session.add(gameT)
            game_details = gameDetails(game_id)
            db_session.add(game_details)

        tournament.quarter_final = str(waiting)
        db_session.commit()
        return "OK"

    return abort(409)


def start_semi_final(tournament, games):
    semi_finalists = []
    for game in games:
        game_details = db_session.query(gameDetails).filter_by(game_id = game.id).first()
        if game_details.winner != None:
            if type(game_details.winner) is float:
                semi_finalists.append(int(abs(game_details.winner) / 1.11))
            else:
                semi_finalists.append(abs(game_details.winner))

    if len(semi_finalists) < 4:
        tournament.semi_final = ""
        db_session.commit()
        return abort(409)
    
    tournament.semi_final = str(semi_finalists)
    db_session.commit()
    
    for i in range(0, 4, 2):
        game_id = get_random_string(7)
        player_one = db_session.query(User).filter_by(id = semi_finalists[i]).first()
        player_two = db_session.query(User).filter_by(id = semi_finalists[i + 1]).first()
        gameT = GameT(game_id, player_one.id, player_two.id, tournament.id)
        db_session.add(gameT)
        game_details = gameDetails(game_id)
        db_session.add(game_details)
    
    db_session.commit()
    return "OK"


def start_final(tournament, games):
    semi_finalists = ast.literal_eval(tournament.semi_final)
    winners = []
    finalists = []
    for game in games:
        game_details = db_session.query(gameDetails).filter_by(game_id = game.id).first()
        if game_details.winner:
            if abs(game_details.winner) in semi_finalists or int(abs(game_details.winner) / 1.11) in semi_finalists:
                if type(game_details.winner) is float:
                    winners.append(int(abs(game_details.winner) / 1.11))
                else:
                    winners.append(abs(game_details.winner))

    for winner in winners:
        num_of_games = 0
        winner_games = db_session.query(gameDetails).filter(or_(gameDetails.winner == winner,
                                                                gameDetails.winner == -1 * winner)).all()
        for details in winner_games:
            game = db_session.query(GameT).filter_by(id = details.game_id).first()
            if tournament.id == game.tournament_id:
                num_of_games += 1
        
        if num_of_games > 1 and abs(winner) not in finalists:
            finalists.append(abs(winner))

    if len(finalists) < 2:
        tournament.final = ""
        db_session.commit()
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


def determine_winner(tournament, games):
    finalists = ast.literal_eval(tournament.final)
                
    for game in games:
        if (finalists[0] == game.w_player or finalists[0] == game.b_player) and \
            (finalists[1] == game.w_player or finalists[1] == game.b_player):

            game_details = db_session.query(gameDetails).filter_by(game_id = game.id).first()
            if game_details.winner != None:
                winner_id = None
                if type(game_details.winner) is float:
                    winner_id = int(abs(game_details.winner) / 1.11)
                else:
                    winner_id = abs(game_details.winner)
                
                tournament.winner = winner_id
                db_session.commit()
                winner = db_session.query(User).filter_by(id = winner_id).first()
                variable = dict(winner = "The winner is " + winner.username + "!")
                return variable
            else:
                return abort(409)
    
    return abort(409)

def winner_notifier(tournament, games):
    if tournament.winner < 0:
        tournament.winner *= -1
        db_session.commit()
        winner = db_session.query(User).filter_by(id = tournament.winner).first()
        variable = dict(winner = "The winner is " + winner.username + "!")
        return variable
    
    return abort(409)
    
                    