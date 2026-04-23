COUNTRY_CACHE: dict[str, str] = {}


def clean_and_split(query: str) -> list[str]:
    # 1. Standardize the case first
    clean_query = query.lower() 
    
    # 2. Swap punctuation for spaces
    punctuation_to_remove = [",", "-", ".", "!"]
    for char in punctuation_to_remove:
        clean_query = clean_query.replace(char, " ")
        
    # 3. Split on the spaces
    return clean_query.split()

def extract_filters(tokens: list[str]) -> dict:
    filters = {}
    
    gender_map = {
    "men": "male",
    "males": "male",
    "boys": "male",
    "women": "female",
    "females": "female",
    "girls": "female"
}
    
    age_map = {
    "adults": {"age_group": "adult"},
    "adult": {"age_group": "adult"},
    "young": {"min_age": 16, "max_age": 24},
    "teens": {"age_group": "teenager"},
    "teenagers": {"age_group": "teenager"}
}
    
    for word in tokens:
        if word in gender_map:
            filters["gender"] = gender_map[word]
        elif word in COUNTRY_CACHE:
            filters["country_id"] = COUNTRY_CACHE[word]
        elif word in age_map:
            filters.update(age_map[word]) 
            
    return filters