from sqlalchemy import Column, String, DateTime, Integer, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()


class RateLimit(Base):
    __tablename__ = "RateLimits"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    command = Column(String)
    last_used = Column(DateTime, default=func.now())


class Ratelimiter:

    def __init__(self):
        self.engine = create_engine("sqlite:///ratelimits.sqlite")
        self.session_obj = sessionmaker()
        self.session_obj.configure(bind=self.engine)
        self.session = self.session_obj()
        Base.metadata.create_all(self.engine)

    def add_rate_limit(self, user_id, command):
        rl = RateLimit(user_id=user_id, command=command)
        self.session.add(rl)
        self.session.commit()

    def is_rate_limited(self, user_id, command, time_length):
        query = self.session.query(RateLimit).filter(RateLimit.user_id == user_id).filter(RateLimit.command == command)

        if query.count() == 0:
            self.add_rate_limit(user_id, command)
            return False
        else:
            result = query.one()
            current_time = datetime.datetime.utcnow()
            timestamp = result.last_used

            if (current_time - timestamp).seconds > time_length:
                result.last_used = current_time
                self.session.commit()
                return False
            else:
                return True
