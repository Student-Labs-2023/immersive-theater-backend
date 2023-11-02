from sqlalchemy import create_engine, Integer, String, Double, Boolean, ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os


load_dotenv()

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))

Base = declarative_base()

class Authors(Base):
    __tablename__ = 'Authors'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(250), nullable=False)
    thumbnail_link = Column(String(300), nullable=False)

    PerformanceAuthor = relationship("PerformanceAuthors")

class Performances(Base):
    __tablename__ = 'Performances'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300), nullable=False)
    duration = Column(Integer, nullable=False)
    cover_image_link = Column(String(300), nullable=False)
    thumbnail_link = Column(String(300), nullable=False)
    tag = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)

    PerformanceAuthor = relationship("PerformanceAuthors")
    PerformanceImage = relationship("PerformanceImages")
    Audio = relationship("Audios")
    Payment = relationship("Payments")

class PerformanceAuthors(Base):
    __tablename__ = 'PerformanceAuthors'

    author_id = Column(Integer, ForeignKey("Authors.id"), primary_key=True)
    performance_id = Column(Integer, ForeignKey("Performances.id"), primary_key=True)
    role = Column(String(60), nullable=False)

    Author = relationship("Authors")
    Performance = relationship("Performances")

class PerformanceImages(Base):
    __tablename__ = 'PerformanceImages'

    performance_id = Column(Integer, ForeignKey("Performances.id"), primary_key=True)
    image_link = Column(String(300), nullable=False, primary_key=True)

    Performance = relationship("Performances")

class Places(Base):
    __tablename__ = 'Places'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    address = Column(String(100), nullable=False)

    Audio = relationship("Audios")

class Audios(Base):
    __tablename__ = 'Audios'

    performance_id = Column(Integer, ForeignKey("Performances.id"), primary_key=True)
    order = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False, unique=True)
    place_id = Column(Integer, ForeignKey("Places.id"))
    name = Column(String(100), nullable=False)
    audio_link = Column(String(300), nullable=False)
    short_audio_link = Column(String(300), nullable=False)
    description = Column(String(300), nullable=False)

    Performance = relationship("Performances")
    Place = relationship("Places")
    AudioImage = relationship("AudioImages")

class AudioImages(Base):
    __tablename__ = 'AudioImages'

    audio_id = Column(Integer, ForeignKey("Audios.id"), primary_key=True)
    image_link = Column(String(300), nullable=False, primary_key=True)

    Audio = relationship("Audios")

class Payments(Base):
    __tablename__ = 'Payments'

    user_id = Column(String(50), primary_key=True)
    performance_id = Column(Integer, ForeignKey("Performances.id"))
    operation_id = Column(String(50), nullable=False)
    sender = Column(String(50), nullable=False)
    amount = Column(String(10), nullable=False)
    performance_used = Column(Boolean, nullable=False, default=False)

    Performance = relationship("Performances")

Base.metadata.create_all(engine)
