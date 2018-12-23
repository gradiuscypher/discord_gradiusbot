import traceback
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from datetime import datetime


Base = declarative_base()
engine = create_engine('sqlite:///banpool.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()


class BanPoolManager:
    def add_user_to_banpool(self, banpool_name, user_id, reason):
        """
        Add a User ID to the banpool
        :param banpool_name:
        :param user_id: Discord User ID
        :param reason:
        :return:
        """
        try:
            # Identify the banpool that the User ID will be added to
            banpool_query = session.query(BanPool).filter(BanPool.pool_name==banpool_name)

            if banpool_query.count() > 0:
                banpool = banpool_query.one()

                # The banpool name existed
                if banpool:
                    # Determine if the user has already been added to the banpool
                    user_query = session.query(DiscordUser).filter(DiscordUser.banpool_id==banpool.id, DiscordUser.user_id==user_id)

                    if user_query.count() == 0:
                        ban_date = datetime.now()
                        new_discord_user = DiscordUser(user_id=user_id, ban_date=ban_date, banpool_id=banpool.id, reason=reason)
                        session.add(new_discord_user)
                        session.commit()
                        return "User has been added to the banpool.", True
                    else:
                        return "This user is already a part of this banpool.", False

            else:
                # The banpool name did not exist
                return "This banpool does not exist.", False

        except:
            print(traceback.format_exc())
            return "An error has occurred", False

    def add_userlist_to_banpool(self, banpool_name, user_id_list, reason):
        """
        Add a list of User IDs separated by comma to the banpool
        :param banpool_name:
        :param user_id_list:
        :param reason:
        :return:
        """

        # Process the list and turn it to a python list
        try:
            user_list = user_id_list.split(',')

        except:
            print(traceback.format_exc())
            return "Your userlist wasn't properly formatted. Separate each ID with a comma.", False

        try:
            for user in user_list:
                self.add_user_to_banpool(banpool_name, user, reason)
            return "Users have been processed. Non-duplicates have been added to the ban list.", True

        except:
            print(traceback.format_exc())
            return "An error has occurred.", False

    def add_user_to_exceptions(self, user_id, server_id):
        """
        Add a User ID+Server ID to the ban exceptions list
        :param user_id: Discord User ID
        :param server_id: Discord Server ID
        :return:
        """
        try:
            user_exception_query = session.query(BanExceptions).filter(BanExceptions.user_id==user_id, BanExceptions.server_id==server_id)

            # This user doesn't have an exception for this server
            if user_exception_query.count() == 0:
                exception_date = datetime.now()
                new_exception = BanExceptions(user_id=user_id, server_id=server_id, exception_date=exception_date)
                session.add(new_exception)
                session.commit()
                return "The user has been added to exceptions for this server", True

            # This user already has an exception for this server
            else:
                return "This user already has an exception for this server.", False

        except:
            print(traceback.format_exc())
            return "An error has occurred.", False

    def banpool_list(self):
        try:
            banpool_list = session.query(BanPool)
            list_result = []

            for result in banpool_list:
                list_result.append(result)

            return list_result
        except:
            print(traceback.format_exc())
            return None

    def banpool_user_list(self, banpool_name):
        """
        Return a list of User IDs in a banpool
        :param banpool_name:
        :return:
        """
        try:
            # Identify the banpool that the User ID will be added to
            # TODO BUG: This could actually end up being no users, so we should check that we have results first
            banpool = session.query(BanPool).filter(BanPool.pool_name==banpool_name).one()

            if banpool:
                user_list = []

                # The banpool name existed
                for user in banpool.banned_users:
                    user_list.append(user)

                return user_list
            else:
                return None

        except:
            print(traceback.format_exc())
            return None

    def build_db(self):
        Base.metadata.create_all(engine)

    def create_banpool(self, banpool_name, banpool_description):
        """
        Creates a banpool with banpool_name
        :param banpool_name:
        :return:
        """
        try:
            query = session.query(BanPool).filter(BanPool.pool_name==banpool_name)

            if query.count() == 0:
                # BanPool name wasn't found so create it
                new_banpool = BanPool(pool_name=banpool_name, pool_description=banpool_description)
                session.add(new_banpool)
                session.commit()
                return "The banpool has been created.", True
            else:
                return "This banpool name already exists", False

        except:
            print(traceback.format_exc())
            return "An error has occurred.", False

    def exception_list(self):
        try:
            exceptions_list = session.query(BanExceptions)
            list_result = []

            for result in exceptions_list:
                list_result.append(result)

            return list_result
        except:
            print(traceback.format_exc())

    def is_user_in_banpool(self, banpool_name, user_id):
        """
        Checks if the User ID is in the banpool
        :param banpool_name:
        :param user_id:
        :return:
        """
        try:
            # Identify the banpool
            banpool = session.query(BanPool).filter(BanPool.pool_name==banpool_name).one()

            if banpool:
                user_query = session.query(DiscordUser).filter(DiscordUser.user_id==user_id, DiscordUser.banpool_id==banpool.id)

                if user_query.count() > 0:
                    return True
                else:
                    return False
        except:
            print(traceback.format_exc())
            return False

    def is_user_banned(self, user_id):
        """
        Checks if the user is in any banpool
        :param user_id:
        :return:
        """
        try:
            user_query = session.query(DiscordUser).filter(DiscordUser.user_id==user_id)

            if user_query.count() > 0:
                user = user_query.one()
                banpool = session.query(BanPool).filter(BanPool.id==user.banpool_id).one()

                return banpool.pool_name, True, user.reason, user.last_name, user.last_discrim
            else:
                return "User is not in any banpool.", False, None, None, None
        except:
            print(traceback.format_exc())
            return "An error has occurred.", False, None

    def is_user_in_exceptions(self, user_id, server_id):
        """
        Checks if a User ID is in the exception list for server_id
        :param user_id:
        :param server_id:
        :return:
        """
        try:
            query = session.query(BanExceptions).filter(BanExceptions.server_id==server_id, BanExceptions.user_id==user_id)

            if query.count() > 0:
                return True
            else:
                return False
        except:
            print(traceback.format_exc())
            return False

    def remove_user_from_banpool(self, banpool_name, user_id):
        """
        Removes a User ID from the banpool
        :param banpool_name:
        :param user_id:
        :return:
        """
        try:
            # Identify the banpool that the User ID will be added to
            banpool = session.query(BanPool).filter(BanPool.pool_name==banpool_name).one()

            if banpool:
                # Find if the user is in the banpool
                user_query = session.query(DiscordUser).filter(DiscordUser.banpool_id==banpool.id, DiscordUser.user_id==user_id)

                if user_query.count() > 0:
                    user = user_query.one()
                    if user:
                        session.delete(user)
                        session.commit()
                        return "User has been removed from the banpool.", True
                else:
                    return "User not found in banpool.", False
            else:
                return "This banpool does not exist.", False

        except:
            print(traceback.format_exc())
            return "An error has occurred.", False

    def remove_user_from_exceptions(self, user_id, server_id):
        """
        Removes a User ID and Server ID combination from exceptions
        :param user_id:
        :param server_id:
        :return:
        """
        try:
            user_exception = session.query(BanExceptions).filter(BanExceptions.user_id==user_id, BanExceptions.server_id==server_id)

            if user_exception.count() > 0:
                user = user_exception.one()
                session.delete(user)
                session.commit()
                return "User has been removed from exception list", True

            else:
                return "User wasn't found in exception list", False

        except:
            print(traceback.format_exc())
            return "An error has occurred.", False

    def set_last_knowns(self, user_id, user_name, user_discrim):
        """
        Sets the last known identification info of the user banned. Is collected on a ban.
        :param user_id:
        :param user_name:
        :param user_discrim:
        :return:
        """
        try:
            user_query = session.query(DiscordUser).filter(DiscordUser.user_id==user_id)

            if user_query.count() > 0:
                user = user_query.one()
                user.last_name = user_name
                user.last_discrim = user_discrim
                session.commit()

        except:
            print(traceback.format_exc())


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
    ban_date = Column(DateTime)
    banpool_id = Column(Integer, ForeignKey('banpool.id'))
    reason = Column(String)
    last_name = Column(String)
    last_discrim = Column(String)

    def __repr__(self):
        return '<DiscordUser(id={}, user_id={}, ban_date={}, banpool_id={}> reason={}'.format(
            self.id, self.user_id, self.ban_date, self.banpool_id, self.reason
        )
