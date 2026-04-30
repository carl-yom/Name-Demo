import uuid6
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer,Float, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from database import Base

def generate_uuid7():
    return str(uuid6.uuid7())

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=generate_uuid7)  

    name = Column(String, unique=True, nullable=False, index=True)

# index=True added to fields users are likely to filter by to prevent "full-table scan" penalty.
    gender = Column(String, nullable=False, index=True)
    gender_probability = Column(Float, nullable = False)
    # sample_size = Column(Integer, nullable = False)

# Indexed because the requirements mention min_age and max_age
    age = Column(Integer, nullable=False, index=True)
    age_group = Column(String, nullable=False, index=True)

    country_id = Column(String, nullable=False, index = True)
    # THE NEW FIELD
    country_name = Column(String, nullable=False)
    country_probability = Column(Float, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class User(Base):
    __tablename__ = "users"
    
    # Primary Key
    id = Column(String, primary_key=True, index=True, default=generate_uuid7)
    
    # GitHub Identity
    github_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    avatar_url = Column(String, nullable=True) # TRD requirement
    
    # Permissions & Status
    role = Column(
        Enum("analyst", "admin", name="user_roles"),
        default="analyst",
        nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps (TRD requirements)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)