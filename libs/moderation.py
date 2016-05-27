from sqlalchemy import Column, String, DateTime, Integer, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()


class PunishStats(Base):
    __tablename__ = "PunishStats"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    level = Column(Integer)
    last_changed_timestamp = Column(DateTime, default=func.now())


class TimeoutStats(Base):
    __tablename__ = "TimeoutStats"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    level = Column(Integer)
    last_changed_timestamp = Column(DateTime, default=func.now())


class ModerationPunish(Base):
    __tablename__ = "ModerationPunish"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    user_name = Column(String)
    comment = Column(String)
    moderator_id = Column(String)
    moderator_name = Column(String)
    level = Column(Integer)
    timestamp = Column(DateTime, default=func.now())


class ModerationTimeout(Base):
    __tablename__ = "ModerationTimeout"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    user_name = Column(String)
    comment = Column(String)
    moderator_id = Column(String)
    moderator_name = Column(String)
    level = Column(Integer)
    timestamp = Column(DateTime, default=func.now())


class Moderation:

    def __init__(self):
        self.engine = create_engine("sqlite:///moderation.sqlite")
        self.session_obj = sessionmaker()
        self.session_obj.configure(bind=self.engine)
        self.session = self.session_obj()
        Base.metadata.create_all(self.engine)
