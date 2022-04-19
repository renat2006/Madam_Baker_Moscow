import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image_file_path = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    status_color = sqlalchemy.Column(sqlalchemy.String, nullable=True)
