import traceback
import logging
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///banpool_configuration.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

# Setup Logging
logger = logging.getLogger('banpool_configuration')


class BanpoolConfigManager:
    def build_db(self):
        Base.metadata.create_all(engine)

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

            if target_config:
                target_pool = session.query(PoolSubscription).filter(PoolSubscription.pool_name==pool_name).first()

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


class BanpoolConfig(Base):
    __tablename__ = 'banpoolconfig'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    announce_chan = Column(Integer)
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
