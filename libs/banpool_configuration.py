import traceback
import logging
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from datetime import datetime

from libs import banpool

Base = declarative_base()
engine = create_engine('sqlite:///banpool_configuration.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

# Setup Logging
logger = logging.getLogger('banpool_configuration')

# Setup banpool manager
bpm = banpool.BanPoolManager()


class BanpoolConfigManager:
    def build_db(self):
        Base.metadata.create_all(engine)

    def banpool_is_deleted(self, pool_name):
        """
        This is called when a banpool is deleted by the banpool manager, to safely remove subscriptions
        :param pool_name:
        :return:
        """
        try:
            target_subscriptions = session.query(PoolSubscription).filter(PoolSubscription.pool_name==pool_name).all()

            for subscription in target_subscriptions:
                session.delete(subscription)
                session.commit()
            return True
        except:
            logger.error(traceback.format_exc())
            return False

    def is_guild_subscribed(self, guild_id, pool_name):
        if pool_name == 'global':
            return True

        else:
            pool_config = session.query(BanpoolConfig).filter(BanpoolConfig.server_id==guild_id).first()

            if pool_config:
                subscriptions = pool_config.subscriptions
                return len([x for x in subscriptions if x.pool_name == pool_name]) > 0
            else:
                return False

    def set_admin_role_id(self, server_id, admin_role_id, author, author_id):
        """
        Sets the admin role that's allowed to run !bpc commands
        :param server_id:
        :param admin_role_id:
        :param author:
        :param author_id:
        :return:
        """
        try:
            now = datetime.now()
            target_server = session.query(BanpoolConfig).filter(BanpoolConfig.server_id==server_id).first()

            # the server exists, set its channel
            if target_server:
                target_server.admin_role_id = admin_role_id
                session.add(target_server)
                session.commit()
                return True

            # the server doesn't exist, create it and set its channel
            else:
                new_server = BanpoolConfig(server_id=server_id, admin_role_id=admin_role_id, last_edit_date=now,
                                           last_edit_author=author, last_edit_id=author_id)
                session.add(new_server)
                session.commit()
                return True

        except:
            logger.error(traceback.format_exc())
            return False

    def get_admin_role_id(self, server_id):
        target_config = session.query(BanpoolConfig).filter(BanpoolConfig.server_id==server_id).first()

        if target_config:
            return target_config.admin_role_id
        else:
            return None

    def set_announce_chan(self, server_id, channel_id, author, author_id):
        try:
            now = datetime.now()
            target_server = session.query(BanpoolConfig).filter(BanpoolConfig.server_id==server_id).first()

            # the server exists, set its channel
            if target_server:
                target_server.announce_chan = channel_id
                session.add(target_server)
                session.commit()
                return True

            # the server doesn't exist, create it and set its channel
            else:
                new_server = BanpoolConfig(server_id=server_id, announce_chan=channel_id, last_edit_date=now,
                                           last_edit_author=author, last_edit_id=author_id)
                session.add(new_server)
                session.commit()
                return True

        except:
            logger.error(traceback.format_exc())
            return False

    def get_announce_chan(self, server_id):
        target_config = session.query(BanpoolConfig).filter(BanpoolConfig.server_id==server_id).first()

        if target_config:
            return target_config.announce_chan
        else:
            return None

    def set_pool_level(self, server_id, pool_name, level, author, author_id):
        try:
            now = datetime.now()
            target_config = session.query(BanpoolConfig).filter(BanpoolConfig.server_id==server_id).first()

            # get the list of existing banpools
            current_pools = [name.pool_name for name in bpm.banpool_list()]

            # check to make sure the provided pool name exists in the pool list
            if pool_name in current_pools:
                if target_config:
                    target_pool = session.query(PoolSubscription).filter(PoolSubscription.pool_name==pool_name, PoolSubscription.banpool_config_id==target_config.id).first()

                    if target_pool:
                        target_pool.sub_level = level
                        session.add(target_pool)
                        session.commit()
                        return True

                    else:
                        new_pool = PoolSubscription(banpool_config_id=target_config.id, pool_name=pool_name,
                                                    sub_level=level)
                        session.add(new_pool)
                        session.commit()
                        return True
                else:
                    # create the new server coniguration
                    new_server = BanpoolConfig(server_id=server_id, last_edit_date=now, last_edit_author=author,
                                               last_edit_id=author_id)
                    session.add(new_server)
                    session.commit()

                    # set the new pool subscription level
                    new_pool = PoolSubscription(banpool_config_id=new_server.id, pool_name=pool_name,
                                                sub_level=level)
                    session.add(new_pool)
                    session.commit()
                    return True
            else:
                return False

        except:
            logger.error(traceback.format_exc())
            return False

    def get_pool_level(self, server_id, pool_name):
        try:
            target_config = session.query(BanpoolConfig).filter(BanpoolConfig.server_id==server_id).first()

            if target_config:
                target_subscription = session.query(PoolSubscription).filter(PoolSubscription.pool_name==pool_name).\
                    first().sub_level
                return target_subscription
            else:
                return None
        except:
            logger.error(traceback.format_exc())

    def get_configured_pools(self, server_id):
        pool_config = session.query(BanpoolConfig).filter(BanpoolConfig.server_id==server_id).first()

        if pool_config:
            return pool_config.subscriptions
        else:
            return None

    def unsubscribe(self, server_id, banpool_name):
        target_config = session.query(BanpoolConfig).filter(BanpoolConfig.server_id==server_id).first()

        target_subscription = [s for s in target_config.subscriptions if s.pool_name == banpool_name]

        if len(target_subscription) > 0:
            session.delete(target_subscription[0])
            session.commit()
            return True
        else:
            return False


class BanpoolConfig(Base):
    __tablename__ = 'banpoolconfig'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    announce_chan = Column(Integer)
    admin_role_id = Column(Integer)
    last_edit_date = Column(DateTime)
    last_edit_author = Column(String)
    last_edit_id = Column(Integer)
    subscriptions = relationship('PoolSubscription')


class PoolSubscription(Base):
    __tablename__ = 'poolsubscription'
    id = Column(Integer, primary_key=True)
    banpool_config_id = Column(Integer, ForeignKey('banpoolconfig.id'))
    pool_name = Column(String)
    sub_level = Column(String)
