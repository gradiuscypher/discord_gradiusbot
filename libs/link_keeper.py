from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class LinkKeeper:

    def __init__(self):
        self.engine = create_engine('sqlite:///link.db')
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)

    def build_db(self):
        Base.metadata.create_all(self.engine)

    def add_link(self, link, description):
        session = self.DBSession()
        link = Link(link=link, description=description)
        session.add(link)
        session.commit()

    def add_tag(self, link_id, tag_text):
        session = self.DBSession()
        tag = Tag(link_id=link_id, tag_text=tag_text)
        session.add(tag)
        session.commit()

    def get_link(self, tag):
        session = self.DBSession()
        return session.query(Link).join(Tag).filter(Tag.tag_text == tag)

    def get_all_links(self):
        session = self.DBSession()
        return session.query(Link).all()

    def remove_link(self, link_id):
        session = self.DBSession()
        target_link = session.query(Link).filter_by(id=link_id).first()
        session.delete(target_link)
        session.commit()

    def remove_tag(self, link_id, tag_text):
        session = self.DBSession()
        target_tag = session.query(Tag).filter_by(link_id=link_id, tag_text=tag_text).first()
        session.delete(target_tag)
        session.commit()


class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    link = Column(String)
    description = Column(String)
    tags = relationship('Tag')

    def __repr__(self):
        return "<Link(id='{}', link='{}', description='{}' tags='{}')>"\
            .format(self.id, self.link, self.description, self.tags)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag_text = Column(String)
    link_id = Column(Integer, ForeignKey('links.id'))

    def __repr__(self):
        return "<Tag(id='{}', tag_text='{}', link_id='{}')>" \
            .format(self.id, self.tag_text, self.link_id)
