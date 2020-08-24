#! /usr/bin/env python3
import traceback
import csv
from sys import argv
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from datetime import datetime


Base = declarative_base()
engine = create_engine('sqlite:///planets.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

product_strings = [
    "base metals",
    "condensates",
    "heavy water",
    "fiber composite",
    "smartfab units",
    "lustering alloy",
    "toxic metals",
    "coolant",
    "noble gas",
    "opulent compound",
    "silicate glass",
    "motley compound",
    "heavy metals",
    "reactive gas",
    "noble metals",
    "condensed alloy",
    "sheen compound",
    "supertensile plastics",
    "suspended plasma",
    "industrial fibers",
    "lucent compound",
    "liquid ozone",
    "polyaramids",
    "construction blocks",
    "reactive metals",
    "plasmoids",
    "gleaming alloy",
    "crystal compound",
    "glossy compound",
    "ionic solutions",
    "dark compound",
    "precious alloy",
    "oxygen isotopes",
    "nanites"
]


class Planet(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    pid = Column(String)
    region = Column(String)
    const = Column(String)
    system = Column(String)
    name = Column(String)
    ptype = Column(String)
    resource = Column(String)
    richness = Column(String)
    output = Column(Integer)
    security = Column(Integer)


class ResourceLocation(Base):
    __tablename__ = 'resourcelocations'
    id = Column(Integer, primary_key=True)
    pid = Column(Integer)
    resource = Column(String)
    jumps = Column(Integer)
    quality = Column(String)
    planet = Column(String)
    const = Column(String)
    system = Column(String)
    output = Column(Integer)


def planet_lookup():
    lookup = {}
    with open('pdata.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row[12] != "None":
                lookup[row[0]] = round(float(row[12]), 1)
            else:
                lookup[row[0]] = None
    return lookup


def fill_db():
    print("Building lookup...")
    lookup = planet_lookup()
    print("Done building lookup!")

    print("Building DB...")
    with open('planets.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row[0] in lookup.keys():
                security = lookup[row[0]]
            else:
                security = None

            new_planet = Planet(region=row[1], pid=row[0], const=row[2], system=row[3], name=row[4], ptype=row[5], resource=row[6], richness=row[7], output=float(row[8]), security=security)
            session.add(new_planet)
            session.commit()


def best_planets(region):
    for product in product_strings:
        print(f"Building lookup for {product}")
        # query = session.query(Planet).filter(Planet.region == region, func.lower(Planet.resource) == product, Planet.richness == 'Rich', Planet.richness == 'Perfect')
        query = session.query(Planet).filter(Planet.region == region, func.lower(Planet.resource) == product, (Planet.richness == 'Rich') | (Planet.richness == 'Perfect'))
        print(query.count())
        # for r in query:
        #     print(r)


if __name__ == '__main__':
    if argv[1] == 'build':
        Base.metadata.create_all(engine)
    if argv[1] == 'fill':
        fill_db()
    if argv[1] == 'lookup':
        planet_lookup()
    else:
        print('working')
