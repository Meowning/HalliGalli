from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    user_id    = db.Column(db.String(36), primary_key=True)
    nickname   = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatLog(db.Model):
    __tablename__ = "chat_logs"
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id   = db.Column(db.String(36), nullable=False)
    user_id   = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)
    nickname  = db.Column(db.String(50), nullable=False)
    text      = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class VisitLog(db.Model):
    __tablename__ = "visit_logs"
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id   = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)
    path      = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
