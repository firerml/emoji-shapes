from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Token(Base):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(30), nullable=False, index=True, unique=True)
    token = Column(String(30), nullable=False)


engine = create_engine('sqlite:///artmoji.db')
DB = sessionmaker(bind=engine)()
if not engine.dialect.has_table(engine, Token.__tablename__):
    Base.metadata.create_all(engine)


def get_token_obj(user_id):
    token_rows = DB.query(Token).filter(Token.user_id == user_id).all()
    if token_rows:
        return token_rows[0]
    return None


def get_token_str(user_id):
    token_obj = get_token_obj(user_id)
    if token_obj:
        return token_obj.token
    return ''


def add_token(user_id, token):
    DB.add(Token(user_id=user_id, token=token))
    DB.commit()


def delete_token(user_id):
    token_obj = get_token_obj(user_id)
    if token_obj:
        DB.delete(token_obj)
