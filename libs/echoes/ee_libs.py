# TODO: capitalize words or the bot is fired.

#! /usr/bin/env python3

import traceback
import csv
import requests
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
    richness = Column(String)
    planet = Column(String)
    const = Column(String)
    system = Column(String)
    output = Column(Integer)
    start = Column(String)


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


def best_planets():
    best_locations_dict = {}
    jump_lookup = {}
    all_system_set = set()

    # iterate over every product and find locations that have either Rich or Perfect for the product
    for product in product_strings:
        query = session.query(Planet).filter((Planet.region == 'Catch') | (Planet.region == 'Stain') | (Planet.region == 'Impass'), func.lower(Planet.resource) == product, (Planet.richness == 'Rich') | (Planet.richness == 'Perfect'))

        for r in query:
            all_system_set.add(r.system)

            if product not in best_locations_dict.keys():
                best_locations_dict[product] = [r]
            else:
                best_locations_dict[product].append(r)

    # iterate over the all system set and calculate jump distance and store
    print("Getting jump values...")
    r = requests.post('https://everest.kaelspencer.com/jump/batch/', json={'source': 'V2-VC2', 'destinations': list(all_system_set)})
    for destination in r.json()['destinations']:
        jump_lookup[destination['destination']] = destination['jumps']

    # Create the DB entries for every product, location, and jump value
    for product in product_strings:
        for planet in best_locations_dict[product]:
            new_resource_location = ResourceLocation(pid=planet.pid, resource=product, jumps=jump_lookup[planet.system],
                                                     richness=planet.richness, planet=planet.name, const=planet.const,
                                                     system=planet.system, output=planet.output, start='V2-VC2')
            session.add(new_resource_location)
            session.commit()


def get_best_planets(resource, max_locations=10, start='V2-VC2'):
    return_list = []
    query = session.query(ResourceLocation).filter(ResourceLocation.resource == resource, ResourceLocation.start == start).order_by(ResourceLocation.jumps)

    jump_amount = None
    result_count = 1

    for result in query:
        if not jump_amount:
            jump_amount = result.jumps
            return_list.append(result)
            result_count += 1

        elif jump_amount == result.jumps:
            return_list.append(result)

        elif jump_amount != result.jumps and result_count <= max_locations:
            jump_amount = result.jumps
            return_list.append(result)
            result_count += 1

        elif jump_amount != result.jumps and result_count > max_locations:
            break

    return return_list


if __name__ == '__main__':
    if argv[1] == 'build':
        Base.metadata.create_all(engine)
    if argv[1] == 'fill':
        fill_db()
    if argv[1] == 'lookup':
        planet_lookup()
    else:
        print('working')
