import json
import logging
import traceback
from discord.colour import Color
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

    def get_inventory(self, owner_id):
        """Returns the inventory object of the owner.

        Args:
            owner_id (Integer): Discord ID of the owner

        Returns:
            Inventory: The inventory object of the owner, if one doesn't exist, it's created. If error, then None
        """        
        inventory_obj = session.query(Inventory).filter(Inventory.owner_id==owner_id).first()

        try:
            if inventory_obj:
                return inventory_obj
            else:
                new_inventory = Inventory(owner_id=owner_id)
                logger.info(f"Creating a new inventory for {owner_id}")
                session.add(new_inventory)
                session.commit()
                return new_inventory
        except:
            logger.error(traceback.format_exc())
            return None
        

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
    instances = relationship('ItemInstance', backref='item')
    system_name = Column(String)
    name = Column(String)
    description = Column(String)
    script = Column(String)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_attribute(self, attribute_name):
        return session.query(ItemAttribute).filter(ItemAttribute.item_id==self.id, ItemAttribute.name==attribute_name).first()


class ItemAttribute(Base):
    __tablename__ = 'itemattribute'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'))
    name = Column(String)
    value = Column(String)


class ItemInstance(Base):
    __tablename__ = 'iteminstance'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'))
    inventory_id = Column(Integer, ForeignKey('inventory.id'))
    system_name = Column(String)
    count = Column(Integer)


class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    items = relationship('ItemInstance', backref='inventory')
    owner_id = Column(Integer)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_item(self, system_name, amount):
        """Adds a number of items to an inventory

        Args:
            system_name (String): The system_name of the item
            amount (Integer): The number of items you want to add

        Returns:
            bool: Whether the action succeeded or not
        """
        try:
            target_item = ItemManager().get_item(system_name)
            logger.debug(f"target_item: {target_item}")

            if target_item:
                inventory_item = self.get_inventory_item(system_name)
                logger.debug(f"[add_item] inventory_item: {inventory_item}")

                if inventory_item:
                    inventory_item.count += amount
                    session.add(inventory_item)
                    session.commit()
                else:
                    item_instance = ItemInstance(system_name=system_name, item=target_item, inventory_id=self.id, count=amount)
                    logger.debug(f"item_instance: {item_instance.item.name}, {item_instance.count}")
                    session.add(item_instance)
                    session.commit()

                logger.info(f"Added {amount} of {system_name} to {self.owner_id}")
                return True

            else:
                logger.error(f"Unable to find item with system_id: {system_name}")
                return False

        except:
            logger.error(traceback.format_exc())
            return False

    def get_inventory_item(self, system_name):
        """Gets the ItemInstance of an item in the user's inventory

        Args:
            system_name (String): The Item system_name

        Returns:
            ItemInstance: Returns an ItemInstance or None
        """        
        try:
            logger.debug(f"[get_inventory_item] - self.id: {self.id} system_name: {system_name}")
            inventory_item = session.query(ItemInstance).filter(ItemInstance.inventory_id==self.id, ItemInstance.system_name==system_name).first()
            return inventory_item

        except:
            logger.error(traceback.format_exc())
            return None

    def remove_item(self, system_name, amount, dry_run=False):
        """Removes the provided amount of item_id from the inventory

        Args:
            system_name (String): The system_name of the item
            amount (Integer): The amount of the item to remove
            dry_run (bool, optional): If True, only verifies whether the inventory has at least the amount provided. Defaults to False.

        Returns:
            bool: Whether the action succeeded or not
        """        
        try:
            inventory_item = self.get_inventory_item(system_name)
            if inventory_item and inventory_item.count >= amount and amount > 0:
                if dry_run:
                    return True

                else:
                    keep_at_zero = inventory_item.item.get_attribute('keepatzero')

                    if inventory_item.count - amount <= 0 and not keep_at_zero:
                        session.delete(inventory_item)
                        session.commit()
                        return True

                    else:
                        result = self.add_item(system_name, -amount)
                        return result

            else:
                return False

        except:
            logger.error(traceback.format_exc())
            return False
