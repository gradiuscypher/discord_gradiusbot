import logging
import pickle
import pytz
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

help_str = """Here's how to use the Animal Crossing bot, all commands start with `!ac`:

Optional input is surrounded by `[]`, required input is surrounded by `<>`. Please do not include the `[]<>` symbols, though.

**DM Commands (use in a DM with the bot):**

```
!ac help - this command.

!ac turnip add <PRICE> - set the current price that Turnips are for on your island. On Sundays this will be the buy price, all other days will be the sell price.

!ac friendcode <FRIEND CODE> - set your Nintendo friend code if you'd like others to be able to add you.

!ac island open [DODO CODE] - set your island to appear as open on the status chart. Include the DODO CODE if you'd like anyone to be able to join you.

!ac island close - set your island to appear as closed on the status chart.

!ac fruit <apple, pear, cherry, peach, orange> - set your native fruit for the status chart. Please use the names listed.

!ac timezone help - get more information about the timezone command, as well as a list of valid time zones.

!ac timezone set <TIME ZONE> - set your time zone to the provided time zone. Please copy/paste directly from the list.
```

**Channel Commands (use in the Animal Crossing channel):**

```
!ac stonks - show the turnip prices that have been registered

!ac social - show the friend codes that have been registered

!ac travel - show the islands that are open for travel and the native fruits
```
"""


def migrate_data(filename):
    """
    Migrate old AC bot data from the pickle file to a database.
    :param filename:
    :return:
    """
    am = AcManager()
    am.build_db()
    tz = pytz.timezone("America/Los_Angeles")

    with open(filename, 'rb') as ac_file:
        ac_data = pickle.load(ac_file)

    # create the users
    for user in ac_data['users']:
        userblob = ac_data['users'][user]
        new_user = am.add_user(user)
        new_user.update_fruit(userblob['fruit'])
        new_user.update_friend_code(userblob['friend_code'].replace('SW-', ''))

    # add the users turnip prices
    for entry in ac_data['turnips']:
        user = am.user_exists(entry['discord_id'])
        price = entry['price']
        old_time = entry['time']

        if user and price and old_time:
            time = tz.normalize(tz.localize(old_time)).astimezone(pytz.utc)
            user.add_price(price, time)


class AcManager:
    def build_db(self):
        Base.metadata.create_all(engine)

    def add_user(self, discord_id):
        """
        Create an animal crossing user
        :param discord_id
        :return:
        """
        try:
            new_user = AcUser(discord_id=discord_id, friend_code='', fruit='', island_open=False, dodo_code='', time_zone='')
            session.add(new_user)
            session.commit()
            return new_user
        except:
            logger.error(traceback.format_exc())

    def user_exists(self, discord_id):
        try:
            query = session.query(AcUser).filter(AcUser.discord_id==discord_id).first()

            if query:
                return query
            else:
                return None
        except:
            logger.error(traceback.format_exc())

    def user_list(self):
        try:
            return session.query(AcUser).all()
        except:
            logger.error(traceback.format_exc())

    def is_island_open(self, server_id):
        try:
            return session.query(AcUser).filter(AcUser.island_open==True).first()
        except:
            logger.error(traceback.format_exc())


class TurnipEntry(Base):
    __tablename__ = 'turnip_price'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('ac_user.id'))
    price = Column(Integer)
    time = Column(DateTime)


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

    def add_price(self, price, time=datetime.utcnow()):
        """
        Add a turnip price to a user's list of prices
        :return:
        """
        try:
            new_price = TurnipEntry(user_id=self.id, price=price, time=time)
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
        try:
            new_server = DiscordServer(user_id=self.id, server_id=server_id)
            session.add(new_server)
            session.commit()
        except:
            logger.error(traceback.format_exc())

    def update_island(self, island_open, dodo_code=''):
        """
        Update the user's island to either be open or closed
        :return:
        """
        try:
            self.island_open = island_open
            self.dodo_code = dodo_code
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
