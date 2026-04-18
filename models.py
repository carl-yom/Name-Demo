import uuid6
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer,Float, DateTime
from sqlalchemy.sql import func
from database import Base

def generate_uuid7():
    return str(uuid6.uuid7())

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=generate_uuid7)

    name = Column(String, unique=True, nullable=False, index=True)

    gender = Column(String, nullable=False)
    gender_probability = Column(Float, nullable = False)
    sample_size = Column(Integer, nullable = False)
    age = Column(Integer, nullable=False)
    age_group = Column(String, nullable=False)
    country_id = Column(String, nullable=False)
    country_probability = Column(Float, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))