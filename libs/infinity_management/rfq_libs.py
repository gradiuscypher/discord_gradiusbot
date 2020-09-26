import configparser
from airtable import Airtable
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session


Base = declarative_base()
engine = create_engine('sqlite:///infinity_rfq.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

emoji_dict = {
    'refresh': '🔄',
    'confirm': '✅'
}


class RfqManager:
    def build_db(self):
        """
        Creates the database and tables
        :return:
        """
        Base.metadata.create_all(engine)

    class Request(Base):
        __tablename__ = 'requests'
        id = Column(Integer, primary_key=True)
        requester_id = Column(Integer)
        requester_name = Column(String)
        materials = relationship('Material')
        time_submitted = Column(DateTime)

    class Material(Base):
        __tablename__ = 'materials'
        id = Column(Integer, primary_key=True)
        request_id = Column(Integer, ForeignKey('requests.id'))
        name = Column(String)
        amount = Column(Integer)


def update_rfq_order(request_id, airtable_obj):
    materials = {}
    requests = airtable_obj.search('Requester ID', request_id)

    for request in requests:
        resource_name = request['fields']['Resource (from Resource List)'][0]
        if resource_name in materials.keys():
            materials[resource_name] += request['fields']['Amount']
        else:
            materials[resource_name] = request['fields']['Amount']

        airtable_obj.delete(request['id'])
    return materials
