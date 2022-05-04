import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Invite(SqlAlchemyBase):
    __tablename__ = 'invite_word'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    invite_word = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)

