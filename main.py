from python_game.game import Game
from init import create_app
from flask import Flask, jsonify, request, render_template, abort, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_, and_, update, delete, insert
from database import db_session
from models import User, GameT, gameDetails, userStats, Tournament, Message
import os, ast, models, pdb, string, random
import auth, game_base, multiplayer, tournament

app = create_app()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/play')
def playroom():
    return render_template('play.html')

@app.route('/end_waiting', methods=['POST'])
def end_waiting():
    current_user.is_waiting = False
    db_session.commit()
    return "OK"

@app.route('/profile')                   
def profile():
    stats_query = db_session.query(userStats).filter_by(user_id = current_user.id)
    stats = stats_query.first()
    
    if stats.played_games == "":
        return render_template('profile.html', username=current_user.username,
                                            game_count=0,
                                            win_rate=stats.win_rate)

    game_ids = ast.literal_eval(stats.played_games)
    game_count = len(game_ids)
    game_desc = []
    game_dates = []
    game_endings = []
    win_count = 0
    draw_count = 0
    
    if game_count > 0:
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
            if details.winner == current_user.id:
                game_endings.append("win")
                win_count += 1
            elif details.winner == "draw":
                game_endings.append("draw")
                draw_count += 1
            else:
                game_endings.append("loss")
    
    win_rate = (win_count + (0.5 * draw_count)) / len(game_ids) * 100
    
    win_rate = float("{:.2f}".format(win_rate))

    stats_query.update({"win_rate": win_rate})
    db_session.commit()
    
    return render_template('profile.html', username=current_user.username,
                                            game_count=game_count,
                                            game_ids=game_ids,
                                            games=game_desc,
                                            game_dates=game_dates,
                                            game_endings=game_endings,
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
                        all_figures=py_game.all_figures,
                        w_won_figures=w_won_figs,
                        b_won_figures=b_won_figs,
                        move_counter=move_counter,
                        w_player=w_player,
                        b_player=b_player)

        return variables

if __name__=='__main__':
    app.run(debug=True)