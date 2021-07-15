import datetime

from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app import db
from services.logging_funcs import (after_request_log, before_request_log,
                                    before_rollback_log, session_handler)


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


class Category(BaseModel):
    __tablename__ = "category"
    bots = db.relationship("Bot", backref="category", lazy=True)
    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


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

    def __str__(self):
        return f"{self.name} by {self.author}"

    def __repr__(self):
        return f"{self.name} by {self.author}"


class User(BaseModel):
    __tablename__ = "user"
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return f"{self.username}"


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
