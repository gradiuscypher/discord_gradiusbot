import traceback
from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session


Base = declarative_base()
engine = create_engine('sqlite:///pi_ledger.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()


class LedgerManager:
    def build_db(self):
        Base.metadata.create_all(engine)

    def parse_ledger_string(self, ledger_text):
        try:
            ledger_list = []
            split_text = ledger_text.split('\n')

            for line in split_text:
                ledger_list.append(line.split("    "))

            return ledger_list
        except:
            print(traceback.format_exc())

    def reset_stock(self, stock_string):
        """
        Copy/paste string from cargo and set that as the new stock. Useful for messed up incoming/outgoing entries
        :param stock_string:
        :return:
        """
        try:
            # delete the old 'stock' ledger so that there's only one
            stock_query = session.query(PiLedger).filter(PiLedger.ledger_type=='stock').first()

            if stock_query:
                session.delete(stock_query)
                session.commit()

            # build a new ledger out of pasted data
            new_ledger = PiLedger(ledger_date=datetime.utcnow(), ledger_type='stock')
            session.add(new_ledger)
            session.commit()

            # add entries from parsed data
            ledger_list = self.parse_ledger_string(stock_string)
            for entry in ledger_list:
                ledger_entry = LedgerEntry(ledger_id=new_ledger.id,
                                           item_name=entry[0],
                                           item_quantity=int(entry[1].replace(',', '')),
                                           item_group=entry[2],
                                           item_vol=float(entry[5].strip(' m3').replace(',', '')),
                                           item_price=float(entry[6].strip(' ISK').replace(',', ''))
                                           )
                session.add(ledger_entry)
                session.commit()

        except:
            print(traceback.format_exc())


class PiLedger(Base):
    __tablename__ = 'ledger'
    id = Column(Integer, primary_key=True)

    # when the ledger page was created
    ledger_date = Column(DateTime)

    # the type of ledger page it is:
    # harvest (collecting from resource planets); incoming; multiple pages
    # factory (moving resources to factory planet) outgoing; multiple pages
    # stock (the current stock ledger, kept up to date with incoming/outgoing); single page
    ledger_type = Column(String)

    entries = relationship("LedgerEntry", cascade="all, delete-orphan")


class LedgerEntry(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True)
    ledger_id = Column(Integer, ForeignKey('ledger.id'))
    item_name = Column(String)
    item_quantity = Column(Integer)
    item_group = Column(String)
    item_vol = Column(Float)
    item_price = Column(Float)


