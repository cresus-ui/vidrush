import re
from loguru import logger
from app.services import llm

def extract_people(script: str) -> list:
    """
    Extract names of famous people from the script.
    """
    prompt = f"""
    Analyze the following video script and extract the names of any famous people or public figures mentioned.
    Return only a comma-separated list of names. If no names are found, return 'None'.

    Script:
    {script}
    """
    try:
        response = llm._generate_response(prompt)
        if "None" in response:
            return []
        return [p.strip() for p in response.split(",")]
    except Exception as e:
        logger.error(f"NLP entity extraction failed: {e}")
        return []

def classify_script_category(script: str) -> str:
    """
    Classify the script into one of: finance, biography, news, emotional.
    """
    prompt = f"""
    Analyze the following video script and classify it into EXACTLY ONE of these categories:
    - finance (also includes motivation, success, money, business)
    - biography (stories about people, history, achievements)
    - news (announcements, current events, reports)
    - emotional (stories, poetry, slow-paced reflections)

    Return ONLY the category name in lowercase.

    Script:
    {script}
    """
    try:
        category = llm._generate_response(prompt).strip().lower()
        valid_categories = ["finance", "biography", "news", "emotional"]
        for cat in valid_categories:
            if cat in category:
                return cat
        return "finance" # Default
    except Exception as e:
        logger.error(f"NLP classification failed: {e}")
        return "finance"

def extract_sfx_keywords(script: str) -> list:
    """
    Extract keywords for sound effects from the script.
    """
    # Simple keyword-based approach for now, could be enhanced with LLM
    sfx_map = {
        "money": "cash register",
        "argent": "coin",
        "dollar": "cash",
        "finance": "cash register",
        "success": "victory hit",
        "succès": "victory hit",
        "danger": "alarm",
        "alerte": "alarm",
        "technology": "digital static",
        "technologie": "digital static",
        "computer": "keyboard typing",
        "ordinateur": "keyboard typing",
        "innovation": "sparkle",
        "future": "cinematic whoosh",
        "futur": "cinematic whoosh",
        "explosion": "explosion",
        "boom": "boom",
        "laugh": "laughter",
        "rire": "laughter",
        "car": "car engine",
        "voiture": "car engine",
        "sports": "stadium crowd",
        "football": "stadium crowd",
        "goal": "cheering",
        "but": "cheering"
    }
    
    found_sfx = []
    script_lower = script.lower()
    for key, query in sfx_map.items():
        if key in script_lower:
            found_sfx.append(query)
            
    return list(set(found_sfx))
