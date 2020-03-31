import logging
import traceback
from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

logger = logging.getLogger('gradiusbot')

Base = declarative_base()
engine = create_engine('sqlite:///animal_crossing.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()


class AcManager:
    def build_db(self):
        Base.metadata.create_all(engine)

    def add_user(self, discord_id, server_id):
        """
        Create an animal crossing user
        :param discord_id
        :param server_id
        :return:
        """
        try:
            new_user = AcUser(discord_id=discord_id, friend_code='', fruit='', island_open=False, dodo_code='', time_zone='')
            session.add(new_user)
            session.commit()
        except:
            logger.error(traceback.format_exc())


class TurnipEntry(Base):
    __tablename__ = 'turnip_price'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('ac_user.id'))
    price = Column(Integer)
    time = Column(DateTime)
    time_zone = Column(String)


class DiscordServer(Base):
    __tablename__ = 'discord_server'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('ac_user.id'))
    server_id = Column(Integer)


class AcUser(Base):
    __tablename__ = 'ac_user'
    id = Column(Integer, primary_key=True)
    turnip_prices = relationship("TurnipEntry", cascade="all, delete-orphan")
    discord_servers = relationship("DiscordServer", cascade="all, delete-orphan")
    discord_id = Column(Integer)
    server_id = Column(Integer)
    friend_code = Column(String)
    fruit = Column(String)
    island_open = Column(Boolean)
    dodo_code = Column(String)
    time_zone = Column(String)

    def add_price(self, price, timezone=None):
        """
        Add a turnip price to a user's list of prices
        :return:
        """
        try:
            new_price = TurnipEntry(user_id=self.id, price=price, timezone=timezone, time=datetime.utcnow())
            session.add(new_price)
            session.commit()
        except:
            logger.error(traceback.format_exc())

    def register_discord_server(self, server_id):
        """
        Adds a Discord ID to a user object for server-based messaging.
        :param server_id:
        :return:
        """
        # TODO: implement

    def update_island(self, island_open):
        """
        Update the user's island to either be open or closed
        :return:
        """
        try:
            self.island_open = island_open
            session.commit()
        except:
            logger.error(traceback.format_exc())

    def update_friend_code(self, friend_code):
        """
        Update the user's friend code
        :return:
        """
        try:
            self.friend_code = friend_code
            session.commit()
        except:
            logger.error(traceback.format_exc())

    def update_fruit(self, fruit):
        """
        Update the user's fruit
        :return:
        """
        try:
            self.fruit = fruit
            session.commit()
        except:
            logger.error(traceback.format_exc())

    def update_timezone(self, timezone):
        """
        Update the user's timezone string
        :return:
        """
        try:
            self.time_zone = timezone
            session.commit()
        except:
            logger.error(traceback.format_exc())
