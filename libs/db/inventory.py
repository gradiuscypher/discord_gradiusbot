import json
import logging
import traceback
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from libs.db.base import Base, session

logger = logging.getLogger(__name__)


class ItemManager:
    def generate_item_db(self, json_file: str):
        with open(json_file, 'r') as item_file:
            item_json = json.loads(item_file.read())

        for item in item_json:
            new_item = Item(system_name=item['system_name'], name=item['name'], description=item['description'], script=item['script'])
            session.add(new_item)
            session.commit()

            for attribute in item['attributes']:
                for attribute_key in attribute:
                    new_attribute = ItemAttribute(item_id=new_item.id, name=attribute_key, value=attribute[attribute_key])
                    session.add(new_attribute)
        session.commit()

    def get_item(self, system_name):
        try:
            query = session.query(Item).filter(Item.system_name == system_name)

            if query.count() > 0:
                return query.first()
            else:
                return None
        except:
            logger.error(traceback.format_exc())


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    attributes = relationship('ItemAttribute')
    system_name = Column(String)
    name = Column(String)
    description = Column(String)
    script = Column(String)


class ItemAttribute(Base):
    __tablename__ = 'itemattribute'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'))
    name = Column(String)
    value = Column(String)
