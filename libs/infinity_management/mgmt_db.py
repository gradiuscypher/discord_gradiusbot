import traceback
import requests
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from datetime import datetime


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
        new_pilot = Pilot(discord_id=discord_id, discord_name=discord_name, discord_discriminator=discord_discriminator)

        if character_names and len(character_names) > 0:
            for character in character_names:
                # TODO: add characters to the pilot
                pass


class Pilot(Base):
    __tablename__ = 'pilots'
    id = Column(Integer, primary_key=True)
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

    def add_attribute_group(self, name, description):
        """
        Adds an attribute group to a pilot
        :param name:
        :param description:
        :return:
        """


class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    pilot_id = Column(Integer, ForeignKey('pilots.id'))
    name = Column(String)


class AttributeGroup(Base):
    __tablename__ = 'attributegroups'
    id = Column(Integer, primary_key=True)
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
