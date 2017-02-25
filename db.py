import base64
import logging
import os

from Crypto.Cipher import AES
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ENCRYPTION_KEY = os.environ.get('ARTMOJI_ENCRYPTION_KEY', '1234567890123456')
BLOCK_SIZE = 16
PADDING = '{'

DB_URL = os.environ.get('DATABASE_URL', 'sqlite:///artmoji.db')
Base = declarative_base()


class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(40), nullable=False, index=True, unique=True)
    token = Column(String(250), nullable=False)


class Database:
    def __init__(self):
        engine = create_engine(DB_URL)
        self.sessionmaker = sessionmaker(bind=engine)
        self._session = self.sessionmaker()

        # Create Token table if it does not exist.
        if not engine.dialect.has_table(engine, Token.__tablename__):
            Base.metadata.create_all(engine)

    @property
    def session(self):
        if not self._session.is_active:
            self._session = self.sessionmaker()
        return self._session

    def commit(self):
        session = self.session
        try:
            session.commit()
            return True
        except Exception as e:
            logging.error(e)
            session.rollback()
            return False

    def get_token_obj(self, user_id):
        token_rows = self.session.query(Token).filter(Token.user_id == user_id).all()
        if token_rows:
            return token_rows[0]
        return None

    def get_token_str(self, user_id):
        token_obj = self.get_token_obj(user_id)
        if token_obj:
            return decrypt_token(token_obj.token)
        return ''

    def add_token(self, user_id, token):
        # Returns success boolean
        self.session.add(Token(user_id=user_id, token=encrypt_token(token)))
        return self.commit()

    def delete_token(self, user_id):
        # Returns success boolean
        token_obj = self.get_token_obj(user_id)
        if token_obj:
            self.session.delete(token_obj)
            return self.commit()

DB = Database()


def encrypt_token(token):
    padded_token = token + (BLOCK_SIZE - len(token) % BLOCK_SIZE) * PADDING
    return base64.b64encode(AES.new(ENCRYPTION_KEY).encrypt(padded_token)).decode()


def decrypt_token(encrypted_token):
    return AES.new(ENCRYPTION_KEY).decrypt(base64.b64decode(encrypted_token.encode())).decode().rstrip(PADDING)
