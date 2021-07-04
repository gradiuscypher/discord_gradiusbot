import logging
import random
import string

from sqlalchemy.sql.expression import desc
from libs.db.base import Base, engine, session
from libs.db.inventory import Item, ItemManager, ItemAttribute

logger = logging.getLogger(__name__)


def build_db():
    Base.metadata.create_all(engine)
    logger.debug("Database has been initialized.")


def create_demo_data():
    user_ids = [
        101103243991465984
    ]

    created_items = []
    letters = string.ascii_letters

    # Create some items
    for i in range(0, 100):
        item_name = ''.join(random.choice(letters) for i in range(8))
        description = ''.join(random.choice(letters) for i in range(64))
        new_item = Item(system_name=item_name.upper(), name=item_name, description=description, usable=random.choice([True, False]))
        created_items.append(item_name.upper())
        session.add(new_item)
        session.commit()

    # Create user inventories
    for user_id in user_ids:
        user_inven = ItemManager().get_inventory(user_id)

        # Fill user inventories with items
        for item in created_items:
            user_inven.add_item(item, random.choice(range(0,1000)))