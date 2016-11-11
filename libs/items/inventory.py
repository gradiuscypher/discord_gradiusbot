"""
Inventory class for managing a user's inventory
"""


from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from libs.items.items import Item

Base = declarative_base()


class InventoryDatabase(Base):
    __tablename__ = "inventorydatabase"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    items = relationship("ItemDatabase")


class ItemDatabase(Base):
    __tablename__ = "itemdatabase"
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer)
    inventory_id = Column(Integer, ForeignKey('inventorydatabase.id'), nullable=True)
    inventory = relationship("InventoryDatabase")

    def __repr__(self):
        lookup = Item()
        item_details = lookup.get_item_details(self.item_id)
        return "<Item id={} name={} function={}>".format(self.item_id, item_details['name'], item_details['function'])


class Inventory:
    def __init__(self):
        self.engine = create_engine("sqlite:///inventory_database.sqlite")
        self.session_obj = sessionmaker()
        self.session_obj.configure(bind=self.engine)
        self.session = self.session_obj()
        Base.metadata.create_all(self.engine)

    def add_item(self, user_id, item_id):
        new_item = ItemDatabase()
        new_item.item_id = item_id

        user_inventory = self.session.query(InventoryDatabase).filter_by(user_id=user_id).first()

        if not user_inventory:
            user_inventory = InventoryDatabase(user_id=user_id)
            user_inventory.items.append(new_item)

        else:
            user_inventory.items.append(new_item)

        self.session.add(user_inventory)
        self.session.commit()

    def get_items(self, user_id):
        user_inventory = self.session.query(InventoryDatabase).filter_by(user_id=user_id).first()

        if not user_inventory:
            user_inventory = InventoryDatabase(user_id=user_id)

        return user_inventory.items
