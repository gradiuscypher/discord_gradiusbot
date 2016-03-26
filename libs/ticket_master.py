from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class TicketMaster:

    def __init__(self):
        self.engine = create_engine('sqlite:///tickets.db')
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)

    def build_db(self):
        Base.metadata.create_all(self.engine)

    def close_ticket(self):
        pass

    def comment_ticket(self, ticket_id, author, comment_text):
        session = self.DBSession()
        now = datetime.now()
        comment = Comment(comment_text=comment_text, author=author, ticket_id=ticket_id, timestamp=now)
        session.add(comment)
        session.commit()

    def create_ticket(self, author, content):
        # TODO: remember to check how many open tickets author has
        session = self.DBSession()
        now = datetime.now()
        ticket = Ticket(author=author, content=content, timestamp=now, status="Open")
        session.add(ticket)
        session.commit()

    def delete_ticket(self):
        pass

    def get_all_tickets(self):
        session = self.DBSession()
        return session.query(Ticket).all()


class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    author = Column(String)
    content = Column(String)
    comments = relationship('Comment')
    timestamp = Column(DateTime)
    status = Column(String)

    def __repr__(self):
        return "<Ticket(id='{}', author='{}', content='{}', timestamp='{}', status='{}', comments='{}')>" \
            .format(self.id, self.author, self.content, self.timestamp, self.status, self.comments)


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String)
    author = Column(String)
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    timestamp = Column(DateTime)

    def __repr__(self):
        return "<Comment(id='{}', comment_text='{}', author='{}', ticket_id='{}', timestamp='{}')>" \
            .format(self.id, self.comment_text, self.author, self.ticket_id, self.timestamp)
