from flask import Flask, jsonify, request, render_template, redirect, url_for, \
            abort, redirect, url_for, session
from datetime import datetime, timedelta
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, login_url
from flask_api import status
from werkzeug.security import generate_password_hash, check_password_hash
from init import get_app
from database import db_session
from init import login_manager
from models import User, GameT, gameDetails, userStats
import pdb, os, models

app = get_app()


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).filter_by(id = user_id).first()

@app.route('/signUp')
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('signUp.html')

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/loginDB', methods=['POST'])
def login_session():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    username = request.form.get('username')
    password = request.form.get('password')
    if db_session.query(User).filter_by(username = username).count() == 1:
        user = db_session.query(User).filter_by(username = username).first()
        if user and user.verify_password(password):
            if not db_session.query(userStats).filter_by(user_id = user.id).count():
                user_stats = userStats(user.id)
                db_session.add(user_stats)
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=5)
            session.modified = True
            login_user(user, remember=True)
            user.is_logged = True
            db_session.commit()
            return "OK"
    
    return abort(409)

@app.route('/logout')
@login_required
def logout():
    return render_template('logout.html')

@app.route('/logoutDB')
@login_required
def logout_session():
    current_user.is_logged = False
    db_session.commit()
    logout_user()
    return "OK"

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

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(login_url('login', request.url))