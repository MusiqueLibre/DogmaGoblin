from mediagoblin.db.base import Base
from sqlalchemy import Column, Integer, Unicode, ForeignKey

class DogmaGenresDB(Base):
    __tablename__ = "dogma__genres_medias_data"

    media_entry = Column(Integer, ForeignKey('core__media_entries.id'),primary_key=True)
    genre_ref = Column(Unicode)

MODELS = [DogmaGenresDB]
