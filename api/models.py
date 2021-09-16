import datetime

from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app import db
from services.logging_funcs import (
    after_request_log,
    before_request_log,
    before_rollback_log,
    session_handler,
)


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(
        db.DateTime, default=datetime.datetime.utcnow(), nullable=False
    )
    update_time = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Category(BaseModel):
    __tablename__ = "category"
    bots = db.relationship("Bot", backref="category", lazy=True)
    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()


class Bot(BaseModel):
    __tablename__ = "bot"
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", ondelete="SET NULL"),
        nullable=True,
    )
    name = db.Column(db.String(100), nullable=False)
    add_by_user = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )
    comments = db.relationship("Comment", backref="bot", lazy=True)
    likes = db.relationship("Like", backref="bot", lazy=True)

    def __str__(self):
        return f"{self.name} by {self.author}"

    def __repr__(self):
        return self.__str__()


class User(BaseModel):
    __tablename__ = "user"
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return self.__str__()


class Comment(BaseModel):
    __tablename__ = "comment"
    to_bot_id = db.Column(
        db.Integer, db.ForeignKey("bot.id", ondelete="CASCADE"), nullable=False
    )
    add_by_user = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    content = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f"Comment to bot {self.to_bot_id} by user {self.add_by_user}"

    def __repr__(self):
        return self.__str__()


class Like(BaseModel):
    __tablename__ = "like"
    to_bot_id = db.Column(
        db.Integer, db.ForeignKey("bot.id", ondelete="CASCADE"), nullable=False
    )
    add_by_user = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )

    def __str__(self):
        return f"like to {self.to_bot_id} by {self.author}"

    def __repr__(self):
        return self.__str__()


class Video(BaseModel):
    __tablename__ = "video"
    file_key = db.Column(db.String(100), unique=True, nullable=False)
    add_by_user = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    s3_link = db.Column(db.String(200), unique=True, nullable=False)
    glacier_link = db.Column(db.String(200), unique=True, nullable=True)

    def __str__(self):
        return f"video {self.file_key}"

    def __repr__(self):
        return self.__str__()


@event.listens_for(Session, "before_flush")
def session_before_flush(session, flush_context, instanses):
    about_session = session_handler(session)
    before_request_log(
        about_session["model"],
        about_session["user_id"],
        about_session["method"],
        about_session["raw_id"],
    )


@event.listens_for(Session, "after_flush")
def session_after_flush(session, flush_context):
    about_session = session_handler(session)
    after_request_log(
        about_session["model"],
        about_session["user_id"],
        about_session["method"],
        about_session["raw_id"],
    )


@event.listens_for(Session, "after_rollback")
def session_after_rollback(session):
    about_session = session_handler(session)
    before_rollback_log(
        about_session["model"],
        about_session["user_id"],
        about_session["method"],
        about_session["raw_id"],
    )
