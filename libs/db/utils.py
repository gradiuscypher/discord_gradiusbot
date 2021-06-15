import logging
from libs.db.base import Base, engine
from libs.db.inventory import Item, ItemManager, ItemAttribute

logger = logging.getLogger(__name__)


def build_db():
    Base.metadata.create_all(engine)
    logger.debug("Database has been initialized.")