from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine
from bot.config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

user_model_access = Table(
    'user_model_access',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('model_id', ForeignKey('models.id'), primary_key=True)
)

user_prompt_access = Table(
    'user_prompt_access',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('prompt_id', ForeignKey('prompts.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # Telegram user ID
    username = Column(String)
    models = relationship('Model', secondary=user_model_access, back_populates='users')
    prompts = relationship('Prompt', secondary=user_prompt_access, back_populates='users')

class Model(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship('User', secondary=user_model_access, back_populates='models')

class Prompt(Base):
    __tablename__ = 'prompts'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    users = relationship('User', secondary=user_prompt_access, back_populates='prompts')

async def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
