import logging
import traceback
from airtable import Airtable
from configparser import RawConfigParser
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session


Base = declarative_base()
engine = create_engine('sqlite:///infinity_mgmt.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()


# Setup Logging
logger = logging.getLogger('gradiusbot')


class PilotManager:
    def __init__(self):
        config = RawConfigParser()
        config.read('infinity_mgmt.conf')
        self.airtable_basekey = config.get('airtable', 'airtable_basekey')
        self.airtable_apikey = config.get('airtable', 'airtable_apikey')

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
        if pilot_query.count() == 1:
            target_pilot = pilot_query.first()

            for name in character_names:
                character_query = session.query(Character).filter(Character.name == name, Character.pilot_id == target_pilot.id)

                if character_query.count() == 0:
                    new_character = Character(pilot_id=target_pilot.id, name=name)
                    session.add(new_character)
            session.commit()

    def copy_to_airtable(self):
        """
        copies the DB to airtables
        """
        try:
            logger.debug('Starting Airtable copy...')

            # set the ready state to false to indicate that it's not ready
            state_table = Airtable(self.airtable_basekey, 'State', self.airtable_apikey)
            ready_id = state_table.match('key', 'ready')['id']
            fields = {'key': 'ready', 'value': 'false'}
            state_table.replace(ready_id, fields)

            # delete previous table entries
            logger.debug("Deleting previous table entries...")
            pilot_table = Airtable(self.airtable_basekey, 'Pilots', self.airtable_apikey)
            character_table = Airtable(self.airtable_basekey, 'Characters', self.airtable_apikey)
            attribute_table = Airtable(self.airtable_basekey, 'Attributes', self.airtable_apikey)
            attribute_groups_table = Airtable(self.airtable_basekey, 'AttributeGroups', self.airtable_apikey)
            pilot_table.batch_delete([entry['id'] for entry in pilot_table.get_all()])
            character_table.batch_delete([entry['id'] for entry in character_table.get_all()])
            attribute_table.batch_delete([entry['id'] for entry in attribute_table.get_all()])
            attribute_groups_table.batch_delete([entry['id'] for entry in attribute_groups_table.get_all()])
            logger.debug("Previous table entries deleted!")

            # copy pilots table
            logger.debug("Copying Pilots table...")
            pilots = session.query(Pilot)
            pilot_records = []
            for pilot in pilots:
                pilot_records.append({
                    'id': pilot.id,
                    'discord_id': pilot.discord_id,
                    'discord_name': pilot.discord_name,
                    'discord_discriminator': pilot.discord_discriminator
                })
            pilot_table.batch_insert(pilot_records)
            logger.debug("Pilots table copied!")

            # copy characters table
            logger.debug("Copying Characters table...")
            characters = session.query(Character)
            character_records = []
            for character in characters:
                character_records.append({
                    'id': character.id,
                    'pilot_id': character.pilot_id,
                    'name': character.name
                })
            character_table.batch_insert(character_records)
            logger.debug("Characters table copied!")

            # copy attributes
            logger.debug("Copying Attribute table...")
            attributes = session.query(Attribute)
            attribute_records = []
            for attribute in attributes:
                attribute_records.append({
                    'id': attribute.id,
                    'attribute_group_id': attribute.attribute_group_id,
                    'key': attribute.key,
                    'value': attribute.value,
                    'friendly_name': attribute.friendly_name
                })
            attribute_table.batch_insert(attribute_records)
            logger.debug("Attribute table copied!")

            # copy attributegroups
            logger.debug("Copying AttributeGroup table...")
            attribute_groups = session.query(AttributeGroup)
            attribute_group_records = []
            for attribute_group in attribute_groups:
                attribute_group_records.append({
                    'id': attribute_group.id,
                    'pilot_id': attribute_group.pilot_id,
                    'name': attribute_group.name,
                    'description': attribute_group.description
                })
            attribute_groups_table.batch_insert(attribute_group_records)
            logger.debug("AttributeGroup table copied!")

            # set the ready state to true to indicate that it's ready
            state_table = Airtable(self.airtable_basekey, 'State', self.airtable_apikey)
            ready_id = state_table.match('key', 'ready')['id']
            fields = {'key': 'ready', 'value': 'true'}
            state_table.replace(ready_id, fields)

            logger.debug('Airtable copy complete!')

        except:
            logger.error(f"Failed to copy to airtable:\n{traceback.format_exc()}")

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

    def remove_characters(self):
        for character in self.characters:
            session.delete(character)
        session.commit()


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
