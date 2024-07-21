import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USERNAME = os.getenv('VEHICLES_DB_USERNAME')
DB_PASSWORD = os.getenv('VEHICLES_DB_PASSWORD')
DB_NAME = os.getenv('VEHICLES_DB_NAME')
DB_HOST = os.getenv('VEHICLES_DB_HOST')

DATABASE_URL = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

Base = declarative_base()

class ObjectsDetection(Base):
    __tablename__ = 'objects_detection'
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(String(50), nullable=False)
    detection_time = Column(DateTime, nullable=False)
    object_type = Column(String(50), nullable=False)
    object_value = Column(Integer, nullable=False)

class VehiclesStatus(Base):
    __tablename__ = 'vehicles_status'
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(String(50), nullable=False)
    report_time = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)

def configure_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
