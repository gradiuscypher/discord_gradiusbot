from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class ServerList(Base):
    __tablename__ = "ServerList"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    default_server = Column(String)


class ServerManagement:

    def __init__(self):
        self.engine = create_engine("sqlite:///server_list.sqlite")
        self.session_obj = sessionmaker()
        self.session_obj.configure(bind=self.engine)
        self.session = self.session_obj()
        Base.metadata.create_all(self.engine)

    def set_default_server(self, user_id, server_id):
        sl = self.session.query(ServerList).filter_by(user_id=user_id).first()

        if not sl:
            sl = ServerList(user_id=user_id, default_server=server_id)
        else:
            sl.default_server = server_id

        self.session.add(sl)
        self.session.commit()

    def get_default_server(self, user_id):
        sl = self.session.query(ServerList).filter_by(user_id=user_id).first()

        if not sl:
            return None
        else:
            return sl.default_server
