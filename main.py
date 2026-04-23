from fastapi import FastAPI, Depends, HTTPException,Response, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import json

from database import engine, Base, SessionLocal
import models
import schemas
import clients
import crud
import nlp_parser

@asynccontextmanager
async def lifespan(app:FastAPI):
    # 1. Boot up: Load the JSON file into the parser's cache
    try:
        with open("countries.json", "r") as f:
            countries_data = json.load(f)
            nlp_parser.COUNTRY_CACHE.update(countries_data)
        print(f"Loaded {len(nlp_parser.COUNTRY_CACHE)} country mappings into memory.")
    except FileNotFoundError:
        print("WARNING: countries.json not found. Country parsing will fail.")
        
    yield # Server runs here
    
    # 2. Shut down
    nlp_parser.COUNTRY_CACHE.clear()
app = FastAPI(lifespan = lifespan)
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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400, # Translating 422 to a standard 400 Bad Request
        content={"status": "error", "message": "Invalid request data format"},
    )

# endpoints
@app.post("/api/profiles",response_model=schemas.SuccessResponse,status_code=status.HTTP_201_CREATED)
async def create_profile(profile_in: schemas.ProfileCreate, response: Response, db: Session = Depends(get_db)):
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
        response.status_code = status.HTTP_200_OK
        return {"message": "Profile already exists", "data": existing_profile}
    


@app.get("/api/profiles/search")
def search_profiles(q:str, db: Session = Depends(get_db)):
    tokens = nlp_parser.clean_and_split(q)
    filters = nlp_parser.extract_filters(tokens)

    # Uninterpretable Queries
    if not filters:
        raise HTTPException(status_code=400, detail="Unable to interpret query")
    # unpack filters of the dictionary directly in the query builder
    profiles = crud.get_profiles_from_db(db = db, **filters)

    return{
        "status": "success",
        "data": profiles
    }

@app.get("/api/profiles", response_model=schemas.PaginatedProfileResponse)
def get_all_profiles(
    gender: str|None = None, 
    age_group: str| None = None, country_id : str |None = None,min_age:int|None = None, 
    max_age:int|None = None,
    min_gender_probability: float | None = None,
    min_country_probability : float | None = None ,
    sort_by : str = Query("created_at"),
    order:str = Query("desc"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le= 50),
    db: Session = Depends(get_db)
):
    if page < 1 or limit < 1 or limit > 50:
        raise HTTPException(status_code=400, detail="Invalid query parameters")
    query = db.query(models.Profile)
    if gender:
        query = query.filter(models.Profile.gender == gender.strip().lower())
    if age_group:
        query = query.filter(models.Profile.age_group == age_group.strip().lower())
    if country_id:
        query = query.filter(models.Profile.country_id == country_id.strip().upper())
    
    if min_age is not None:
        query = query.filter(models.Profile.age >= min_age)
    if max_age is not None:
        query = query.filter(models.Profile.age <= max_age)
        
    if min_gender_probability is not None:
        query = query.filter(models.Profile.gender_probability >= min_gender_probability)
    if min_country_probability is not None:
        query = query.filter(models.Profile.country_probability >= min_country_probability)

    # total matching records
    total_records = query.count()

    # sorting
    valid_sort_columns = {"age", "created_at","gender_probability"}

    if sort_by and sort_by not in valid_sort_columns:
        raise HTTPException(status_code=400, detail="Invalid query parameters")

    if sort_by in valid_sort_columns:
        column = getattr(models.Profile, sort_by)
        if order.lower() == "asc":
            query= query.order_by(asc(column))
        else:
            query = query.order_by(desc(column))

    # pagination
    offset_value = (page -1) * limit
    results = query.offset(offset_value).limit(limit).all()

    return{
        "status": "success",
        "page":page,
        "limit" : limit,
        "total" : total_records,
        "data": results
    }

@app.get("/api/profiles/{profile_id}", response_model=schemas.SuccessResponse)
def get_profile(profile_id:str, db:Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()

    if not profile:
        raise HTTPException(status_code = 404, detail = "Profile not found")
    
    return {"message": "Profile retrieved sucessfully", "data": profile}




@app.delete("/api/profiles/{profile_id}", status_code=204)
def delete_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    db.delete(profile)
    db.commit()
    return 