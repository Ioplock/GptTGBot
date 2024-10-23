from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine
import datetime
from bot.config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

user_model_access = Table(
    'user_model_access', Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('model_id', ForeignKey('models.model_id'), primary_key=True)
)

user_prompt_access = Table(
    'user_prompt_access', Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('prompt_id', ForeignKey('prompts.prompt_id'), primary_key=True)
)

models_endpoint = Table(
    'models_endpoint', Base.metadata,
    Column('model_id', ForeignKey('models.model_id'), primary_key=True),
    Column('endpoint_id', ForeignKey('api_endpoints.endpoint_id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)

class Prompt(Base):
    __tablename__ = 'prompts'
    prompt_id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    users = relationship('User', secondary=user_prompt_access, backref='prompts')

class Model(Base):
    __tablename__ = 'models'
    model_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    endpoint_id = Column(Integer, ForeignKey('api_endpoints.endpoint_id'))
    users = relationship('User', secondary=user_model_access, backref='models')

class APIEndpoint(Base):
    __tablename__ = 'api_endpoints'
    endpoint_id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    models = relationship('Model', secondary=models_endpoint, backref='api_endpoints')

class AccessToken(Base):
    __tablename__ = 'access_tokens'
    token_id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
    api_endpoint = Column(Integer, ForeignKey('api_endpoints.endpoint_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))

class UserSettings(Base):
    __tablename__ = 'user_settings'
    settings_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    selected_model = Column(Integer, ForeignKey('models.model_id'))
    api_endpoint = Column(Integer, ForeignKey('api_endpoints.endpoint_id'))
    access_token = Column(Integer, ForeignKey('access_tokens.token_id'))
    
    # Relationships
    user = relationship('User', backref='settings')
    model = relationship('Model')
    endpoint = relationship('APIEndpoint')
    token = relationship('AccessToken')

class PromtHistory(Base):
    __tablename__ = 'promt_history'
    history_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    input_text = Column(String, nullable=False)
    response = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

async def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
