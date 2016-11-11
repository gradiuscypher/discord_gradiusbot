"""
Wallet controller class for Discord servers. This tracks a user's currency as well as provides functions to use that
currency.
"""
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class WalletDatabase(Base):
    __tablename__ = "WalletDatabase"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    balance = Column(Integer)


class Wallet:

    def __init__(self):
        self.engine = create_engine("sqlite:///wallet_database.sqlite")
        self.session_obj = sessionmaker()
        self.session_obj.configure(bind=self.engine)
        self.session = self.session_obj()
        Base.metadata.create_all(self.engine)

    def get_balance(self, target):
        """Return the target's balance"""
        wallet = self.session.query(WalletDatabase).filter_by(user_id=target).first()

        if not wallet:
            wallet = WalletDatabase(user_id=target, balance=0)
            self.session.add(wallet)
            self.session.commit()
            return 0

        else:
            return wallet.balance

    def modify_balance(self, target, amount):
        """Modify the target's balance by the amount, either positive or negative"""
        wallet = self.session.query(WalletDatabase).filter_by(user_id=target).first()

        if not wallet:
            wallet = WalletDatabase(user_id=target, balance=amount)

        else:
            wallet.balance += amount

        self.session.add(wallet)
        self.session.commit()

    def spend(self, target, amount):
        """Validate that the target has the amount in their wallet. If so, remove that amount and return True.
        Otherwise, return False and do not remove the amount.
        """
        wallet = self.session.query(WalletDatabase).filter_by(user_id=target).first()

        if not wallet:
            wallet = WalletDatabase(user_id=target, balance=0)
            self.session.add(wallet)
            self.session.commit()
            return False

        else:
            if self.get_balance(target) >= amount:
                self.modify_balance(target, -amount)
                self.session.add(wallet)
                self.session.commit()
                return True

            else:
                return False


