from database import Base
from sqlalchemy import MetaData, Table, Column, Integer, Float, String, Boolean, Text, Date, DateTime, ForeignKey, MetaData
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(120), unique=True)
    password = Column(String(120), unique=True)
    is_logged = Column(Boolean)
    waiting = Column(Boolean)
    is_playing = Column(Boolean)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.is_logged = False
        self.waiting = False
        self.is_playing = False

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def is_authenticated(self):
        return self.is_logged

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.username)

class GameT(Base):
    __tablename__ = 'games'
    id = Column(String(120), primary_key=True, unique=True)
    w_player = Column(Integer, ForeignKey('users.id'))
    b_player = Column(Integer, ForeignKey('users.id'))
    user_one = relationship("User", foreign_keys=[w_player])
    users_two = relationship("User", foreign_keys=[b_player])

    def __init__(self, id=None, w_player=None, b_player=None):
        self.id = id
        self.w_player = w_player
        self.b_player = b_player

    def __repr__(self):
        return '<GameT %r>' % (self.id)

class gameDetails(Base):
    __tablename__ = 'game_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String(120), ForeignKey('games.id'))
    moves = Column(String(3000))
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean)
    winner = Column(String(120))
    game = relationship("GameT")

    def __init__(self, game_id=None, moves=None, board=None):
        self.game_id = game_id
        self.moves = moves
        self.board = board
        self.is_active = True
        self.winner = ""

    def __repr__(self):
        return '<gameDetails %r>' % (self.id)

class userStats(Base):
    __tablename__ = 'user_stats'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    played_games = Column(String(5000))
    win_rate = Column(Float)
    game = relationship("User")

    def __init__(self, user_id=None):
        self.user_id = user_id
        self.played_games = ""
        self.win_rate = 100

    def __repr__(self):
        return '<userStats %r>' % (self.user_id)