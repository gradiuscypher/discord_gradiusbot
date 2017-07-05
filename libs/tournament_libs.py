from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///tournament.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


class TournamentManager:
    def __init__(self):
        self.engine = create_engine('sqlite:///tournament.db')
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)

    def build_db(self):
        Base.metadata.create_all(self.engine)

    def start_tournament(self, name, provider_id, tournament_id, extra=""):
        # query = self.session.query(PunishStats).filter(PunishStats.user_id == user_id)
        session = self.DBSession()
        query = session.query(Tournament).filter(Tournament.completed==False)

        if query.count() == 0:
            new_tournament = Tournament(tournament_id=tournament_id, extra=extra, name=name, completed=False,
                                        provider_id=provider_id)
            session.add(new_tournament)
            session.commit()
        else:
            print("There is already an active tournament.")

    def complete_tournament(self):
        pass

    def create_game(self):
        pass

    def join_game(self):
        pass

    def store_game(self):
        pass


class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True)
    tournament_id = Column(String)
    extra = Column(String)
    name = Column(String)
    completed = Column(Boolean)
    provider_id = Column(Integer)
    participants = relationship('Participant')
    game_instances = relationship('GameInstance')

    def join_season(self, discord_id):
        session = DBSession()
        new_participant = Participant(discord_id=discord_id, tournament_id=self.id)
        session.add(new_participant)
        session.commit()

    def __repr__(self):
        return "<Tournament(id={} tournament_id={} extra={} name={} completed={} provider_id={})>"\
            .format(self.id, self.tournament_id, self.extra, self.name, self.completed, self.provider_id)


class GameInstance(Base):
    __tablename__ = "gameinstances"
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime)
    start_date = Column(DateTime)
    finish_date = Column(DateTime)
    creator_discord_id = Column(String)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    eog_json = Column(String)


class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True)
    discord_id = Column(String)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))

    def __repr__(self):
        return "<Participant(id={} discord_id={} tournament_id={})>"\
            .format(self.id, self.discord_id, self.tournament_id)
