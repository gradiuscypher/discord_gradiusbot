from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///tournament.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class TournamentManager:
    def build_db(self):
        Base.metadata.create_all(engine)

    def get_active_tournaments(self):
        """
        Return a list of active Tournaments
        :return: list of Tournament
        """
        tournament_list = []
        query = session.query(Tournament).filter(Tournament.completed==False)

        for result in query:
            tournament_list.append(result)

        return tournament_list

    def start_tournament(self, name, provider_id, tournament_id, map_type, extra=""):
        """
        Starts a new Tournament. Will not start if an active tournament (completed==False) already exists.
        :param name: The tournament name. User-friendly value.
        :param provider_id: The Tournament API Provider ID
        :param tournament_id: The Tournament API Tournament ID
        :param map_type: The map type: SUMMONERS_RIFT, HOWLING_ABYSS
        :param extra: Any extra data about the tournament. Can be empty.
        :return: boolean if creation succeeds or fails
        """
        query = session.query(Tournament).filter(Tournament.completed==False).filter(Tournament.map_type==map_type)

        if query.count() == 0:
            new_tournament = Tournament(tournament_id=tournament_id, extra=extra, name=name, map_type=map_type,
                                        completed=False, provider_id=provider_id)
            session.add(new_tournament)
            session.commit()
            return True
        else:
            print("There is already an active tournament.")
            return False


class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True)
    tournament_id = Column(String)
    extra = Column(String)
    name = Column(String)
    completed = Column(Boolean)
    provider_id = Column(Integer)
    map_type = Column(String)
    participants = relationship('Participant')
    game_instances = relationship('GameInstance')

    def complete_tournament(self):
        """
        Marks the Tournament as complete.
        :return:
        """
        self.completed = True
        session.commit()

    def clean_stale_games(self):
        """
        Cleans up games that are starting but don't have enough players. Compares create_date vs a timeout period.
        :return:
        """
        pass

    def create_game(self, creator_discord_id, map_name):
        """
        When a user requests a new game is created. Creates an GameInstance. Will only start if map type isn't
        already starting
        :param creator_discord_id:
        :param map_name:
        :return:
        """
        now = datetime.now()
        new_game = GameInstance(tournament_id=self.id, creator_discord_id=creator_discord_id, map_name=map_name,
                                create_date=now)
        session.add(new_game)
        session.commit()

    def get_active_games(self):
        """
        Return a list of active Games
        :return: list of GameInstance
        """
        game_list = []
        query = session.query(GameInstance).filter(GameInstance.finish_date is not None)

        for result in query:
            game_list.append(result)

        return game_list

    def join_game(self):
        pass

    def start_game(self):
        pass

    def finish_game(self):
        pass

    def join_season(self, discord_id):
        new_participant = Participant(discord_id=discord_id, tournament_id=self.id)
        session.add(new_participant)
        session.commit()

    def __repr__(self):
        return "<Tournament(id={} tournament_id={} extra={} name={} completed={} provider_id={} map_type={})>"\
            .format(self.id, self.tournament_id, self.extra, self.name, self.completed, self.provider_id, self.map_type)


class GameInstance(Base):
    __tablename__ = "gameinstances"
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime)
    start_date = Column(DateTime)
    finish_date = Column(DateTime)
    creator_discord_id = Column(String)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    map_name = Column(String)
    eog_json = Column(String)


class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True)
    discord_id = Column(String)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))

    def __repr__(self):
        return "<Participant(id={} discord_id={} tournament_id={})>"\
            .format(self.id, self.discord_id, self.tournament_id)
