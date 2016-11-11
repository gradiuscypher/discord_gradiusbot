"""
Basic item functions. Other packages could contain more specific item functions.
"""
from .basic import *
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class ItemDefinition(Base):
    __tablename__ = "itemdefinition"
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer)
    name = Column(String)
    description = Column(String)
    use_description = Column(String)
    function_id = Column(Integer)


class Item:
    def __init__(self):
        self.engine = create_engine("sqlite:///item_definitions.sqlite")
        self.session_obj = sessionmaker()
        self.session_obj.configure(bind=self.engine)
        self.session = self.session_obj()
        Base.metadata.create_all(self.engine)

    def lookup_table(self, id):
        item_ids = {
            1: dice_action
        }

        try:
            return item_ids[id]
        except:
            return None

    def create_item(self, item_name, item_description, use_description, function_id):
        item = ItemDefinition()
        item.name = item_name
        item.description = item_description
        item.use_description = use_description
        item.function_id = function_id
        self.session.add(item)
        self.session.commit()

    def get_item_details(self, item_id):
        item = self.session.query(ItemDefinition).filter_by(id=item_id).first()

        if not item:
            return {}

        else:
            function = self.lookup_table(item_id)
            return {"name": item.name, "description": item.description, "use": item.use_description,
                    "function": function}
