from mediagoblin.db.base import Base
from mediagoblin.db.models import (MediaEntry, Collection)
from sqlalchemy import (Column, Float,  Integer, Unicode, ForeignKey, Table, LargeBinary,DateTime, Boolean)
from sqlalchemy.orm import relationship, backref

#Relationship
class BandMemberRelationship(Base):
    __tablename__ = "dogma__band_member__relation"
    band_id = Column(Integer, ForeignKey("dogma__band.id"), primary_key=True)
    member_id = Column(Integer, ForeignKey("dogma__member.id"), primary_key=True)
    since = Column(DateTime)
    until = Column(DateTime)
    roles = Column(Unicode)
    former = Column(Boolean)
    member = relationship("DogmaMemberDB")

class BandAlbumRelationship(Base):
    __tablename__ = "dogma__band_album__relation"
    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey("dogma__band.id"))
    album_id = Column(Integer , ForeignKey("dogma__album.id"))
    album = relationship("DogmaAlbumDB")

class DogmaExtraDataDB(Base):
    __tablename__ = "dogma__extra_data"
    media_entry = Column(Integer, ForeignKey(MediaEntry.id),primary_key=True)
    composers = Column(Unicode)
    authors = Column(Unicode)
    performers = Column(Unicode)
    genre_ref = Column(Unicode)
    get_media_entry = relationship(MediaEntry,
                                   backref=backref("get_dogma_data", uselist=False,
                                                    cascade="all, delete-orphan"))

#This table only store the ID of a collection that is considered as an album
#The collection system is used as is. This allow dogma to add custom collections "types"
#meanwhile mg still can be used as a stand alone (important to use dogma as a standard pod)
class DogmaAlbumDB(Base):
    __tablename__ = "dogma__album"
    id = Column(Integer, ForeignKey(Collection.id), primary_key=True)

class DogmaBandDB(Base):
    __tablename__ = "dogma__band"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    description = Column(Unicode)
    postalcode = Column(Unicode)
    place = Column(Unicode)
    country = Column(Unicode)
    latitude = Column(Float)
    longitude = Column(Float)
    creator = Column(Integer)
    members = relationship('BandMemberRelationship', backref="get_band_member")
    albums = relationship('BandAlbumRelationship', backref="get_albums")
    since = Column(DateTime)
    subscribed_since = Column(DateTime)

#Global member's data
class DogmaMemberDB(Base):
    __tablename__ = "dogma__member"

    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode)
    last_name = Column(Unicode)
    nickname = Column(Unicode)
    picture_path = Column(Unicode)
    description = Column(Unicode)
    latitude = Column(Float)
    longitude = Column(Float)
    place = Column(Unicode)
    country = Column(Unicode)
    creator = Column(Unicode)


MODELS = [DogmaExtraDataDB, DogmaBandDB, DogmaMemberDB,
          DogmaAlbumDB, BandMemberRelationship, BandAlbumRelationship]
