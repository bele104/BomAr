from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Substitua pelos seus detalhes de login do MySQL
DATABASE_URL = 'mysql+pymysql://usuario:senha@localhost/air_quality'

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_session():
    return Session()
