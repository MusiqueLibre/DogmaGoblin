from mediagoblin.db.base import Base
from mediagoblin.db.models import (MediaEntry, Collection)
from sqlalchemy import (Column, Float,  Integer, Unicode, ForeignKey, Table, LargeBinary,DateTime, Boolean)
from sqlalchemy.orm import relationship, backref

#RELATIONSHIPS
#the global members' data are stored in DogmaMemberDB
class BandMemberRelationship(Base):
    __tablename__ = "dogma__band_member__relation"
    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey("dogma__band.id"))
    member_id = Column(Integer, ForeignKey("dogma__member.id"))
    since = Column(DateTime)
    until = Column(DateTime)
    former = Column(Boolean)
    main = Column(Boolean)
    member_global = relationship("DogmaMemberDB", backref="get_band_relationship")

class BandAlbumRelationship(Base):
    __tablename__ = "dogma__band_album__relation"
    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey("dogma__band.id"))
    album_id = Column(Integer , ForeignKey("dogma__album.id"))
    album = relationship("DogmaAlbumDB")

#TABLES
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
    members = relationship('BandMemberRelationship', backref="get_band")
    albums = relationship('BandAlbumRelationship', backref="get_band")
    since = Column(DateTime)
    subscribed_since = Column(DateTime)

#Global member's data (as opposed to "per band" data, see BandMemberRelationship for this)
class DogmaMemberDB(Base):
    __tablename__ = "dogma__member"
    id = Column(Integer, primary_key=True)
    username = Column(Unicode)
    slug = Column(Unicode)
    real_name = Column(Unicode)
    description = Column(Unicode)
    latitude = Column(Float)
    longitude = Column(Float)
    place = Column(Unicode)
    country = Column(Unicode)
    creator = Column(Integer)

#This table only store the ID of a collection that is considered as an album
#The collection system is used as is. This allow dogma to add custom collections "types"
#meanwhile mg still can be used as a stand alone (important to use dogma as a standard pod)
class DogmaAlbumDB(Base):
    __tablename__ = "dogma__album"
    id = Column(Integer, ForeignKey(Collection.id), primary_key=True)
    get_collection = relationship(Collection)

class DogmaAuthorDB(Base):
    __tablename__="dogma__author"
    id = Column(Integer, primary_key=True)
    media_entry = Column(Integer, ForeignKey(MediaEntry.id))
    member = Column(Integer, ForeignKey(DogmaMemberDB.id))
    is_author = Unicode(Boolean)
    get_media_entry = relationship(MediaEntry,
                                   backref=backref("get_author", uselist=False,
                                                    cascade="all, delete-orphan"))

class DogmaComposerDB(Base):
    __tablename__="dogma__composer"
    id = Column(Integer, primary_key=True)
    media_entry = Column(Integer, ForeignKey(MediaEntry.id))
    member = Column(Integer, ForeignKey(DogmaMemberDB.id))
    is_composer = Unicode(Boolean)
    get_media_entry = relationship(MediaEntry,
                                   backref=backref("get_composer", uselist=False,
                                                    cascade="all, delete-orphan"))

#This table strores individual data that can be used as a key word, and can be link to
#our 4 types (Band, Album, Member, track)
class DogmaKeywordDataDB(Base):
    __tablename__ = "dogma__keyword_data"
    id = Column(Integer, primary_key=True)
    band = Column(Integer, ForeignKey(DogmaBandDB.id))
    member = Column(Integer, ForeignKey(DogmaMemberDB.id))
    album = Column(Integer, ForeignKey(DogmaAlbumDB.id))
    media_entry = Column(Integer, ForeignKey(MediaEntry.id))
    data = Column(Unicode)
    slug = Column(Unicode)
    type = Column(Unicode)
    get_album = relationship("DogmaAlbumDB", primaryjoin="DogmaAlbumDB.id == DogmaKeywordDataDB.album", backref="get_keywords")
    get_member = relationship("DogmaMemberDB", primaryjoin="DogmaMemberDB.id == DogmaKeywordDataDB.member", backref="get_keywords")
    get_band = relationship("DogmaBandDB", primaryjoin="DogmaBandDB.id == DogmaKeywordDataDB.band", backref="get_keywords")
    get_media_entry = relationship(MediaEntry, primaryjoin="MediaEntry.id == DogmaKeywordDataDB.media_entry",
                                   backref=backref("get_keywords", uselist=False,
                                                    cascade="all, delete-orphan"))


MODELS = [DogmaBandDB, DogmaMemberDB, DogmaAlbumDB, DogmaKeywordDataDB, DogmaComposerDB, 
        DogmaAuthorDB, BandMemberRelationship, BandAlbumRelationship]
