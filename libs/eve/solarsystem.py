import logging
import traceback
import sqlite3
from sqlalchemy import Column, Integer, String, create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session


logger = logging.getLogger('gradiusbot')

Base = declarative_base()
engine = create_engine('sqlite:///wh_alerts.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

# try and set up the sqlite data db
try:
    connection = sqlite3.connect('libs/eve/sqlite-latest.sqlite')
except:
    logger.error("Unable to load Eve sqlite file.")
    logger.error(traceback.format_exc())


class Manager():
    def build_db(self):
        Base.metadata.create_all(engine)


class WhAlert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer)
    start_system_id = Column(Integer)
    end_system_id = Column(Integer)
    start_system_name = Column(String)
    end_system_name = Column(String)

    def add_alert(self, discord_id, start_system_name, end_system_name):
        try:
            start_system = get_system_by_name(start_system_name)
            end_system = get_system_by_name(end_system_name)

            if start_system and end_system:
                start_system_id = start_system[2]
                end_system_id = end_system[2]
                start_system_db_name = start_system[3]
                end_system_db_name = end_system[3]

                new_alert = WhAlert(discord_id=discord_id, start_system_id=start_system_id, end_system_id=end_system_id, start_system_name=start_system_db_name, end_system_name=end_system_db_name)
                session.add(new_alert)
                session.commit()
                return "ADDED"
            else:
                return "NO_SYSTEM"
        except:
            logger.error("Unable to add alert.")
            logger.error(traceback.format_exc())
            return "ERROR"


    def remove_alert(self, discord_id, alert_id):
        try:
            alert = session.query(WhAlert).filter(WhAlert.discord_id==discord_id, WhAlert.id==alert_id).first()
            if alert:
                session.delete(alert)
                session.commit()
                return "REMOVED"
            else:
                return "NO_ALERT"

        except:
            logger.error("Unable to remove alert.")
            logger.error(traceback.format_exc())
            return "ERROR"
    
    def list_alerts(self, discord_id):
        try:
            alerts = session.query(WhAlert).filter(WhAlert.discord_id==discord_id)

            if alerts.count > 0:
                alert_string = ""
                for alert in alerts:
                    alert_string += f"{alert.id}) {alert.start_system_name} > {alert.end_system_name}\n"
            else:
                return None
        except:
            logger.error("Unable to list alerts.")
            logger.error(traceback.format_exc())
            return "ERROR"


def load_thera_holes():
    pass


def get_system_by_name(system_name):
    wildcards = {
        'hs': 1,
        'ls': 2,
        '*': 3
    }

    try:
        if system_name.lower() in wildcards.keys():
            return ('', '', wildcards[system_name], system_name)

        else:
            query = 'select * from mapSolarSystems where solarSystemName == (?) COLLATE NOCASE'
            cursor = connection.cursor()
            result = cursor.execute(query, (system_name,)).fetchone()

            return result

    except:
        logger.error(f"Error while searching for system by name.")
        logger.error(traceback.format_exc())


def get_number_of_jumps(start_system, end_system):
    pass