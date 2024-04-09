from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Moedas(Base):
    __tablename__ = "medias_moveis"

    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String, index=True)
    timestamp = Column(Float)
    mms_20d = Column(Float)
    mms_50d = Column(Float)
    mms_200d = Column(Float)
