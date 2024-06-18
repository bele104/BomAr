from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class AirQuality(Base):
    __tablename__ = 'air_quality'
    id = Column(Integer, primary_key=True)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    aqius = Column(Integer, nullable=False)
    mainus = Column(String, nullable=False)
    aqicn = Column(Integer, nullable=False)
    maincn = Column(String, nullable=False)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
