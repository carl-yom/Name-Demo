from sqlalchemy.orm import Session
import models

def get_profiles_from_db(
    db: Session,
    gender: str | None = None,
    country_id: str | None = None,
    min_age: int | None = None,
    max_age: int | None = None,
    age_group: str | None = None,
    sort_by: str = "created_at",
    page=1, limit=10
):
    # 1. Start the base query
    query = db.query(models.Profile)
    
    # 2. Apply the extracted filters
    if gender:
        query = query.filter(models.Profile.gender == gender)
    if country_id:
        query = query.filter(models.Profile.country_id == country_id)
    if min_age is not None:
        query = query.filter(models.Profile.age >= min_age)
    if max_age is not None:
        query = query.filter(models.Profile.age <= max_age)
    if age_group:
        query = query.filter(models.Profile.age_group == age_group)
        
    # 3. Apply the dynamic sorting
    sort_column = getattr(models.Profile, sort_by, models.Profile.created_at)
    query = query.order_by(sort_column.desc())

    total_count = query.count()
    offset = (page - 1) * limit
    profiles = query.offset(offset).limit(limit).all()
    return total_count, profiles