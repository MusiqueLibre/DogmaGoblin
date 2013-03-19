from mediagoblin.db.base import Base
from sqlalchemy import Column, Float,  Integer, Unicode, ForeignKey, Table, LargeBinary
from sqlalchemy.orm import relationship, backref

band_member =  Table("dogma__band_member_relation", Base.metadata,
    Column('band_id', Integer, ForeignKey('dogma__band.id')),
    Column('member_id', Integer, ForeignKey('dogma__member.id'))
    )
band_album =  Table("dogma__band_album_relation", Base.metadata,
    Column('band_id', Integer, ForeignKey('dogma__band.id')),
    Column('album_id', Integer, ForeignKey('dogma__album.id'))
    )

class DogmaExtraDataDB(Base):
    __tablename__ = "dogma__extra_data"

    media_entry = Column(Integer, ForeignKey('core__media_entries.id'),primary_key=True)
    composers = Column(Unicode)
    authors = Column(Unicode)
    performers = Column(Unicode)
    genre_ref = Column(Unicode)
    get_media_entry = relationship("MediaEntry",
                                   backref=backref("get_dogma_data", uselist=False,
                                                    cascade="all, delete-orphan"))

class DogmaAlbumDB(Base):
    __tablename__ = "dogma__album"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    cover = Column(LargeBinary(270000))
    cover_small = Column(LargeBinary(13000))
    slug = Column(Unicode)
    created = Column(Unicode)
    description = Column(Unicode)
    items = Column(Unicode)

class DogmaBandDB(Base):
    __tablename__ = "dogma__band"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    description = Column(Unicode)
    picture = Column(LargeBinary(270000))
    picture_small = Column(LargeBinary(13000))
    latitude = Column(Float)
    longitude = Column(Float)
    place = Column(Unicode)
    created = Column(Unicode)
    members = relationship('DogmaMemberDB', secondary=band_member, backref="get_band_member")
    albums = relationship('DogmaAlbumDB', secondary=band_album, backref="get_albums")

class DogmaMemberDB(Base):
    __tablename__ = "dogma__member"

    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode)
    last_name = Column(Unicode)
    nickname = Column(Unicode)
    picture = Column(LargeBinary(270000))
    picture_small = Column(LargeBinary(13000))
    roles = Column(Unicode)
    description = Column(Unicode)
    latitude = Column(Float)
    longitude = Column(Float)
    place = Column(Unicode)
 

MODELS = [DogmaExtraDataDB, DogmaBandDB, DogmaMemberDB, DogmaAlbumDB]
