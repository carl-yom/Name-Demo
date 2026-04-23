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
    genders_found = set() # Track genders to handle "male and female"
    
    gender_map = {"men": "male", "males": "male", "boys": "male", "male": "male",
                  "women": "female", "females": "female", "girls": "female", "female": "female"}
    
    age_map = {
        "young": {"min_age": 16, "max_age": 24},
        "adults": {"age_group": "adult"},
        "adult": {"age_group": "adult"},
        "teens": {"age_group": "teenager"},
        "teenagers": {"age_group": "teenager"},
        "children": {"age_group": "child"},
        "kids": {"age_group": "child"},
        "seniors": {"age_group": "senior"},
        "elderly": {"age_group": "senior"}
    }
    
    i = 0
    while i < len(tokens):
        word = tokens[i]

        # 1. Look-ahead logic for numeric ages (e.g., "above 30")
        if word in {"above", "over", "older"} and i + 1 < len(tokens) and tokens[i+1].isdigit():
            filters["min_age"] = int(tokens[i+1])
            i += 2  # Skip the number since we just consumed it
            continue
            
        elif word in {"under", "below", "younger"} and i + 1 < len(tokens) and tokens[i+1].isdigit():
            filters["max_age"] = int(tokens[i+1])
            i += 2
            continue

        # 2. Standard Dictionary Mappings
        if word in gender_map:
            genders_found.add(gender_map[word])
        elif word in COUNTRY_CACHE:
            filters["country_id"] = COUNTRY_CACHE[word]
        elif word in age_map:
            filters.update(age_map[word])
            
        i += 1

    # 3. Resolve Genders (If they query "male and female", drop the gender filter)
    if len(genders_found) == 1:
        filters["gender"] = genders_found.pop()

    return filters