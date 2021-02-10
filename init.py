from flask import Flask, jsonify, request, render_template, session
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, Column, Integer, String, MetaData
from database import init_db
import os

login_manager = LoginManager()
app = Flask(__name__)
#db = SQLAlchemy(app)

def create_app():
    app.secret_key = 'Str0ng_Super_Secret_Key'
    app.config['SESSION_TYPE'] = 'filesystem'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CHESS_DATABASE')

    sess = Session()
    sess.init_app(app)

    login_manager.init_app(app)

    init_db()
    return app

def get_app():
    return app

def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str