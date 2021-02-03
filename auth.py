from flask import Flask, jsonify, request, render_template, redirect, url_for, abort, session, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_api import status
from werkzeug.security import generate_password_hash, check_password_hash
from init import get_app
from database import db_session
from init import login_manager
from models import User, GameT, gameDetails, userStats
import pdb
import os
import models

app = get_app()

@app.route('/signUp')
def signup():
    return render_template('signUp.html')

@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).filter_by(id = user_id).first()

@app.route('/login')
def login():
    if redirect(url_for('is_logged')) != "OK":
        return render_template('login.html')
    return abort(401)

@app.route('/logout')
def logout():
    redirect(url_for('is_logged'))
    return render_template('logout.html')

@app.route('/signupDB', methods=['POST'])
def signup_session():
    username = request.form.get('username')
    password = request.form.get('password')
    if db_session.query(User).filter_by(username = username).count() == 0:
        user = User(username, generate_password_hash(password, method='sha256'))
        db_session.add(user)
        db_session.commit()
        return "OK"
    
    return abort(409)


@app.route('/loginDB', methods=['POST'])
def login_session():
    username = request.form.get('username')
    password = request.form.get('password')
    if db_session.query(User).filter_by(username = username).count() == 1:
        user = db_session.query(User).filter_by(username = username).first()
        if user and user.verify_password(password):
            if not db_session.query(userStats).filter_by(user_id = user.id).count():
                user_stats = userStats(user.id)
                db_session.add(user_stats)

            login_user(user, remember=True)
            user.is_logged = True
            db_session.commit()
            return "OK"
    
    return abort(409)

@app.route('/logoutDB')
def logout_session():
    current_user.is_logged = False
    db_session.commit()
    logout_user()
    return "OK"


@app.route('/islogged', methods=['GET'])
def is_logged():
    if hasattr(current_user, 'is_logged'):
        if not current_user.is_logged:
            return abort(401)
        else:
            return "OK"
    else:
        return abort(401)