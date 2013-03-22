from mediagoblin.db.base import Base
from mediagoblin.db.models import (MediaEntry, Collection)
from sqlalchemy import (Column, Float,  Integer, Unicode, ForeignKey, Table, LargeBinary,DateTime, Boolean)
from sqlalchemy.orm import relationship, backref

band_member =  Table("dogma__band_member_relation", Base.metadata,
    Column('band_id', Integer, ForeignKey('dogma__band.id')),
    Column('member_id', Integer, ForeignKey('dogma__member.id')),
    )
band_member_data =  Table("dogma__band_member_data_relation", Base.metadata,
    Column('member_id', Integer, ForeignKey('dogma__member.id')),
    Column('data_id', Integer, ForeignKey('dogma__member__band_data.id')),
    )
band_album =  Table("dogma__band_album_relation", Base.metadata,
    Column('band_id', Integer, ForeignKey('dogma__band.id')),
    Column('album_id', Integer, ForeignKey('dogma__album.id'))
    )

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
    latitude = Column(Float)
    longitude = Column(Float)
    created_by = Column(Unicode)
    members = relationship('DogmaMemberDB', secondary=band_member, backref="get_band_member")
    albums = relationship('DogmaAlbumDB', secondary=band_album, backref="get_albums")
    date = Column(DateTime)

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
    bands_data = relationship('DogmaMemberBandDataDB', secondary=band_member_data, backref="get_member_band_data")

#The member's data that is related to a specific band
class DogmaMemberBandDataDB(Base):
    __tablename__ = "dogma__member__band_data"
    id = Column(Integer, primary_key=True)
    since = Column(DateTime)
    until = Column(DateTime)
    roles = Column(Unicode)
    former = Column(Boolean)
    band = Column(Integer, ForeignKey(MediaEntry.id))

MODELS = [DogmaExtraDataDB, DogmaBandDB, DogmaMemberDB, DogmaAlbumDB, DogmaMemberBandDataDB]
