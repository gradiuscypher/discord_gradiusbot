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


class PunishLog(Base):
    __tablename__ = "PunishLog"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    user_name = Column(String)
    comment = Column(String)
    moderator_id = Column(String)
    moderator_name = Column(String)
    new_level = Column(Integer)
    timestamp = Column(DateTime, default=func.now())


class Moderation:

    def __init__(self):
        self.engine = create_engine("sqlite:///moderation.sqlite")
        self.session_obj = sessionmaker()
        self.session_obj.configure(bind=self.engine)
        self.session = self.session_obj()
        Base.metadata.create_all(self.engine)

    def punish(self, user_id, user_name, comment, moderator_id, moderator_name):
        # Adds one to punish level and returns current punish level
        query = self.session.query(PunishStats).filter(PunishStats.user_id == user_id)

        if query.count() == 0:
            # User was previously never punished, create an entry
            punishment = PunishStats(user_id=user_id, level=1)
            self.session.add(punishment)
            self.session.commit()
            # Add an entry to the punishment log
            punish_log = PunishLog(user_id=user_id, user_name=user_name, comment=comment, moderator_id=moderator_id,
                                   moderator_name=moderator_name, new_level=1)
            self.session.add(punish_log)
            self.session.commit()
            return 1
        else:
            # Increase punishment level by 1
            result = query.one()
            old_level = result.level
            result.level = old_level + 1
            self.session.commit()
            # Add an entry to the punishment log
            punish_log = PunishLog(user_id=user_id, user_name=user_name, comment=comment, moderator_id=moderator_id,
                                   moderator_name=moderator_name, new_level=old_level+1)
            self.session.add(punish_log)
            self.session.commit()
            return old_level+1

    def clean_up(self):
        # Cleans up punishment DBs:
        # Reduces punishment level by 1 every 7 days
        # Unbans those who's bans have been served
        # Cleans up timeout multipliers
        # Reduce spam points by 1 every 24 hours
        pass
