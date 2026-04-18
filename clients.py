import httpx
import asyncio
from fastapi import HTTPException

async def fetch_profile_data(name: str)->dict:
    # endpoints
    urls = {
        "genderize": f"https://api.genderize.io/?name={name}",
        "agify": f"https://api.agify.io/?name={name}",
        "nationalize": f"https://api.nationalize.io/?name={name}"
    }

    async with httpx.AsyncClient() as client:
        try:
            gender_resp, age_resp, nation_resp = await asyncio.gather(
                client.get(urls["genderize"]),
                client.get(urls["agify"]),
                client.get(urls["nationalize"])

            )
        except httpx.RequestError:
            #network-level failures (e.g., DNS issues, timeout)
            raise HTTPException(status_code=502, detail="External API network failiure")
        
    gender_data = gender_resp.json()
    age_data = age_resp.json()
    nation_data = nation_resp.json()

    # strict edge cases
    if gender_data.get("gender") is None or gender_data.get("count", 0) == 0:
        raise HTTPException(status_code=502, detail="Genderize returned an invalid response")
        
    if age_data.get("age") is None:
        raise HTTPException(status_code=502, detail="Agify returned an invalid response")
        
    if not nation_data.get("country"): 
        raise HTTPException(status_code=502, detail="Nationalize returned an invalid response")
    
    top_country = nation_data["country"][0]

    return{
        "name": name,
        "gender": gender_data["gender"],
        "gender_probability": float(gender_data["probability"]),
        "sample_size": int(gender_data["count"]),
        "age": int(age_data["age"]),
        "country_id": top_country["country_id"],
        "country_probability": float(top_country["probability"])
    }