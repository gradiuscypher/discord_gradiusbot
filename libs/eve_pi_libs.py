import traceback
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session


Base = declarative_base()
engine = create_engine('sqlite:///pi_ledger.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()


class PiLedger(Base):
    __tablename__ = 'ledger'
    id = Column(Integer, primary_key=True)
    ledger_date = Column(DateTime)


class LedgerEntry(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True)
    ledger_id = Column(Integer, ForeignKey('ledger.id'))
    item_name = Column(String)
    item_quantity = Column(Integer)
    item_group = Column(String)
    item_vol = Column(Integer)
    item_price = Column(Integer)


def parse_pi_ledger(ledger_text):
    try:
        return_str = ""
        split_text = ledger_text.split('\n')

        for line in split_text:
            return_str += str(line.split()) + '\n'

        return return_str
    except:
        print(traceback.format_exc())
