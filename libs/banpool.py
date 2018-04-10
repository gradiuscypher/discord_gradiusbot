from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

Base = declarative_base()
engine = create_engine('sqlite:///banpool.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()


class BanPoolManager:
    def add_user_to_banpool(self, banpool_name, user_id):
        """
        Add a User ID to the banpool
        :param banpool_name:
        :param user_id: Discord User ID
        :return:
        """

    def add_userlist_to_banpool(self, banpool_name, user_id_list):
        """
        Add a list of User IDs separated by comma to the banpool
        :param banpool_name:
        :param user_id_list:
        :return:
        """

    def add_user_to_exceptions(self, user_id, server_id):
        """
        Add a User ID+Server ID to the ban exceptions list
        :param user_id: Discord User ID
        :param server_id: Discord Server ID
        :return:
        """

    def banpool_list(self, banpool_name):
        """
        Return a list of User IDs in a banpool
        :param banpool_name:
        :return:
        """

    def build_db(self):
        Base.metadata.create_all(engine)

    def create_banpool(self, banpool_name):
        """
        Creates a banpool with banpool_name
        :param banpool_name:
        :return:
        """
        query = session.query(BanPool).filter(BanPool.pool_name==banpool_name)

        if query.count() == 0:
            # BanPool name wasn't found so create it
            pass

    def is_user_in_banpool(self, banpool_name, user_id):
        """
        Checks if the User ID is in the banpool
        :param banpool_name:
        :param user_id:
        :return:
        """

    def is_user_in_exceptions(self, user_id, server_id):
        """
        Checks if a User ID is in the exception list for server_id
        :param user_id:
        :param server_id:
        :return:
        """

    def remove_user_from_banpool(self, banpool_name, user_id):
        """
        Removes a User ID from the banpool
        :param banpool_name:
        :param user_id:
        :return:
        """


class BanPool(Base):
    __tablename__ = 'banpool'
    id = Column(Integer, primary_key=True)
    pool_name = Column(String)
    pool_description = Column(String)
    banned_users = relationship('DiscordUser')

    def __repr__(self):
        return '<BanPool(id={}, pool_name={}, pool_description={}>'.format(
            self.id, self.pool_name, self.pool_description
        )


class BanExceptions(Base):
    __tablename__ = 'banexceptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    server_id = Column(Integer)
    exception_date = Column(DateTime)

    def __repr__(self):
        return '<BanExceptions(id={}, user_id={}, server_id={}, exception_date={}>'.format(
            self.id, self.user_id, self.server_id, self.exception_date
        )


class DiscordUser(Base):
    __tablename__ = 'discordusers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_name = Column(String)
    user_discrim = Column(Integer)
    ban_date = Column(DateTime)
    banpool_id = Column(Integer, ForeignKey('banpool.id'))

    def __repr__(self):
        return '<DiscordUser(id={}, user_id={}, user_name={}, user_discrim={}, ban_date={}, banpool_id={}>'.format(
            self.id, self.user_id, self.user_name, self.user_discrim, self.ban_date, self.banpool_id
        )
