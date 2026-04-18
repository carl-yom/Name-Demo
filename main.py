from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base, SessionLocal
import models
import schemas
import clients

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request,exc):
    status_string = "502" if exc.status_code == 502 else "error"   
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status":status_string,
            "message":exc.detail
        }
    )

# endpoints
@app.post("/api/profiles",response_model=schemas.SuccessResponse)
async def create_profile(profile_in:schemas.ProfileCreate, db:Session = Depends(get_db)):
    clean_name = profile_in.name.strip().lower()

    external_data = await clients.fetch_profile_data(clean_name)

    # Age Group
    age = external_data["age"]
    if age < 18:
        age_group = "child"
    elif age <= 35:
        age_group = "young adult"
    elif age <= 60:
        age_group = "adult"
    else:
        age_group = "senior"

    external_data["age_group"] = age_group
    new_profile = models.Profile(**external_data)

    # Database Transaction (Ensures Idempotency & Safety)

    try:
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return{"message": "Profile created successfully", "data": new_profile}
    
    except IntegrityError:
        db.rollback()
        existing_profile = db.query(models.Profile).filter(models.Profile.name == clean_name).first()
        return{"message": "Profile already exists", "data": existing_profile}
    

@app.get("/api/profiles/{profile_id}", response_model=schemas.SuccessResponse)
def get_profile(profile_id:str, db:Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()

    if not profile:
        raise HTTPException(status_code = 404, detail = "Profile not found")
    
    return {"message": "Profile retrieved sucessfully", "data": profile}


@app.get("/api/profiles")
def list_profiles(
    gender: str = None, 
    country_id: str = None, 
    age_group: str = None, 
    db: Session = Depends(get_db)
):
    # base query
    query = db.query(models.Profile)

    if gender:
        query = query.filter(models.Profile.gender == gender.strip().lower())
    if country_id:
        # Country IDs remain upercase uppercase
        query = query.filter(models.Profile.country_id == country_id.strip().upper()) 
    if age_group:
        query = query.filter(models.Profile.age_group == age_group.strip().lower())

    results = query.all()
    return {"status": "success", "message": "Profiles retrieved successfully", "data": results}