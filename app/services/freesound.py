import os
import requests
from loguru import logger
from app.config import config
from app.utils import utils

def search_sfx(query: str, limit: int = 1) -> list:
    """
    Search Freesound for SFX based on a query.
    Returns a list of dictionaries with sound metadata.
    """
    api_key = config.app.get("freesound_api_key", "").strip()
    if not api_key:
        logger.warning("Freesound API key not configured. SFX search skipped.")
        return []

    url = "https://freesound.org/apiv2/search/text/"
    params = {
        "query": query,
        "token": api_key,
        "fields": "id,name,previews,duration",
        "page_size": limit,
        "filter": "duration:[0.1 TO 10.0]"  # Short sounds only
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        logger.error(f"Freesound search failed for '{query}': {e}")
        return []

def download_sfx(sound_id: int, preview_url: str, task_id: str) -> str:
    """
    Download a Freesound preview and return the local path.
    """
    sfx_dir = os.path.join(utils.task_dir(task_id), "sfx")
    if not os.path.exists(sfx_dir):
        os.makedirs(sfx_dir)

    file_path = os.path.join(sfx_dir, f"sfx_{sound_id}.mp3")
    
    if os.path.exists(file_path):
        return file_path

    try:
        response = requests.get(preview_url, timeout=20)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    except Exception as e:
        logger.error(f"Failed to download SFX {sound_id}: {e}")
        return ""
