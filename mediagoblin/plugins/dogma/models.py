from mediagoblin.db.base import Base
from mediagoblin.db.models import (MediaEntry, Collection)
from sqlalchemy import (Column, Float,  Integer, Unicode, ForeignKey, Table, LargeBinary,DateTime, Boolean)
from sqlalchemy.orm import relationship, backref
from sqlalchemy import event

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
    get_member_global = relationship("DogmaMemberDB", backref=backref("get_band_relationships", cascade="all, delete-orphan"), uselist=False)
    get_band = relationship("DogmaBandDB", backref=backref("get_member_relationships", cascade="all, delete-orphan"), uselist=False)

class BandAlbumRelationship(Base):
    __tablename__ = "dogma__band_album__relation"
    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey("dogma__band.id"))
    album_id = Column(Integer , ForeignKey("dogma__album.id"))
    get_album = relationship("DogmaAlbumDB", backref="get_band_relationships", uselist=False)
    get_band = relationship("DogmaBandDB", backref=backref("get_album_relationships", cascade="all, delete-orphan"), uselist=False)

#TABLES
class DogmaBandDB(Base):
    def delete(self, **kwargs):
        for album in self.get_album_relationships:
            #check if the albums of this band isn't listed elsewhere
            if len(album.get_album.get_band_relationships) == 1:
                album.get_album.delete(commit=False)
        super(DogmaBandDB, self).delete(**kwargs)

    __tablename__ = "dogma__band"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True)
    description = Column(Unicode)
    place = Column(Unicode)
    country = Column(Unicode)
    latitude = Column(Float)
    longitude = Column(Float)
    creator = Column(Integer)
    since = Column(DateTime)
    subscribed_since = Column(DateTime)

#Global member's data (as opposed to "per band" data, see BandMemberRelationship for this)
class DogmaMemberDB(Base):
    __tablename__ = "dogma__member"
    id = Column(Integer, primary_key=True)
    username = Column(Unicode)
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
    def delete(self, **kwargs):
        for item in self.get_collection.get_collection_items():
            #check if the albums of this band isn't listed elsewhere
            track = item.get_media_entry
            if len(track.collections) == 1:
                track.delete(commit=False)
        super(DogmaAlbumDB, self).delete(**kwargs)

    __tablename__ = "dogma__album"
    id = Column(Integer, ForeignKey(Collection.id), primary_key=True)
    release_date = Column(DateTime)
    get_collection = relationship(Collection, backref=backref("get_album", uselist=False), uselist=False, single_parent=True,  cascade="all, delete-orphan")

class DogmaAuthorDB(Base):
    __tablename__="dogma__author"
    id = Column(Integer, primary_key=True)
    media_entry = Column(Integer, ForeignKey(MediaEntry.id))
    member = Column(Integer, ForeignKey(DogmaMemberDB.id))
    get_member = relationship("DogmaMemberDB", backref="get_author", uselist=False)
    get_media_entry = relationship("MediaEntry",
                                   backref=backref("get_authors",
                                                    cascade="all, delete-orphan"))

class DogmaComposerDB(Base):
    __tablename__="dogma__composer"
    id = Column(Integer, primary_key=True)
    media_entry = Column(Integer, ForeignKey(MediaEntry.id))
    member = Column(Integer, ForeignKey(DogmaMemberDB.id))
    get_member = relationship("DogmaMemberDB", backref="get_composer", uselist=False)
    get_media_entry = relationship("MediaEntry",
                                   backref=backref("get_composers",
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
    get_album= relationship("DogmaAlbumDB", primaryjoin="DogmaAlbumDB.id == DogmaKeywordDataDB.album",
            backref="get_keywords", uselist=False)
    get_member = relationship("DogmaMemberDB", primaryjoin="DogmaMemberDB.id == DogmaKeywordDataDB.member",
            backref="get_keywords", uselist=False)
    get_band = relationship("DogmaBandDB", primaryjoin="DogmaBandDB.id == DogmaKeywordDataDB.band",
            backref="get_keywords", uselist=False)
    get_media_entry = relationship(MediaEntry, primaryjoin="MediaEntry.id == DogmaKeywordDataDB.media_entry",
                                   backref=backref("get_keywords", cascade="all, delete-orphan"), uselist=False)


            




MODELS = [DogmaBandDB, DogmaMemberDB, DogmaAlbumDB, DogmaKeywordDataDB, DogmaComposerDB, 
        DogmaAuthorDB, BandMemberRelationship, BandAlbumRelationship]
