import json
from sqlalchemy.dialects.postgresql import insert
from database import SessionLocal
import models

def seed_database():
    print("Loading JSON data ...")
    with open("seed_profiles.json", "r") as file:
        raw_data = json.load(file)
        profile_data = raw_data["profiles"]

    db = SessionLocal()

    try:
        (print(f"Attempting to insert {len(profile_data)} records in one batch ..."))

        stmt = insert(models.Profile).values(profile_data)

        # Idempotency Shield
        stmt = stmt.on_conflict_do_nothing(index_elements=["name"])

        db.execute(stmt)
        db.commit()
        print ("Database seeding complete!, Data is safe and indexed")
    except Exception as e:
        print(f"Database error occurred : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":      seed_database()