import traceback
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session


Base = declarative_base()
engine = create_engine('sqlite:///infinity_mgmt.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()


class PilotManager:
    def build_db(self):
        """
        Creates the database and tables
        :return:
        """
        Base.metadata.create_all(engine)

    def add_pilot(self, discord_id, discord_name, discord_discriminator, character_names=None):
        """
        Adds a pilot to the database
        :return:
        """
        pilot_query = session.query(Pilot).filter(Pilot.discord_id == discord_id)

        if pilot_query.count() == 0:
            new_pilot = Pilot(discord_id=discord_id, discord_name=discord_name, discord_discriminator=discord_discriminator)
            session.add(new_pilot)
            session.commit()
            new_pilot.add_attribute_group('base', "A base attribute group included for all pilots.")
            session.commit()

            if character_names:
                for character in character_names:
                    new_character = Character(pilot_id=new_pilot.id, name=character)
                    session.add(new_character)
                session.commit()

    def get_pilot(self, discord_id):
        pilot_query = session.query(Pilot).filter(Pilot.discord_id == discord_id)

        if pilot_query.count() > 0:
            return pilot_query.first()
        else:
            return None


class Pilot(Base):
    __tablename__ = 'pilots'
    id = Column(Integer, primary_key=True)
    attribute_groups = relationship('AttributeGroup')
    characters = relationship('Character')
    discord_id = Column(Integer)
    discord_name = Column(String)
    discord_discriminator = Column(Integer)

    def add_attribute(self, key, value, friendly_name, attribute_group):
        """
        Adds an attribute to a pilot
        :param key:
        :param value:
        :param friendly_name:
        :param attribute_group:
        :return:
        """
        attr_group_query = session.query(AttributeGroup).filter(AttributeGroup.name == attribute_group)
        if attr_group_query.count() > 0:
            attr_group_id = attr_group_query.first().id
            new_attribute = Attribute(key=key, value=value, friendly_name=friendly_name, attribute_group_id=attr_group_id)
            session.add(new_attribute)
            session.commit()

    def add_attribute_group(self, name, description):
        """
        Adds an attribute group to a pilot
        :param name:
        :param description:
        :return:
        """
        new_attribute_group = AttributeGroup(name=name, description=description, pilot_id=self.id)
        session.add(new_attribute_group)
        session.commit()

    def add_character(self, character_name):
        """
        Adds a character to a pilot profile
        :param character_name:
        :return:
        """
        new_character = Character(pilot_id=self.id, name=character_name)
        session.add(new_character)
        session.commit()

    def get_attribute(self, attribute_group, attribute_name):
        attr_group_query = session.query(AttributeGroup).filter(AttributeGroup.name == attribute_group, AttributeGroup.pilot_id == self.id)

        if attr_group_query.count() > 0:
            attr_group = attr_group_query.first()
            attr_query = session.query(Attribute).filter(Attribute.attribute_group_id == attr_group.id, Attribute.key == attribute_name)

            if attr_query.count() > 0:
                return attr_query.first().value
            else:
                return None
        else:
            return None


class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    pilot_id = Column(Integer, ForeignKey('pilots.id'))
    name = Column(String)


class AttributeGroup(Base):
    __tablename__ = 'attributegroups'
    id = Column(Integer, primary_key=True)
    pilot_id = Column(Integer, ForeignKey('pilots.id'))
    attributes = relationship('Attribute')
    name = Column(String)
    description = Column(String)


class Attribute(Base):
    __tablename__ = 'attributes'
    id = Column(Integer, primary_key=True)
    attribute_group_id = Column(Integer, ForeignKey('attributegroups.id'))
    key = Column(String)
    value = Column(String)
    friendly_name = Column(String)
