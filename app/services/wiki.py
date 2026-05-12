import os
import requests
from loguru import logger
from app.utils import utils

def search_person(name: str) -> dict:
    """
    Step 1: Use Wikipedia API to detect if the person exists and get their exact canonical name.
    """
    search_url = "https://en.wikipedia.org/w/api.php"
    headers = {
        "User-Agent": "Davi-vidrush/1.0 (https://github.com/cresus-ui/vidrush; contact@example.com)"
    }
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": name,
        "srlimit": 1
    }

    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        results = response.json().get("query", {}).get("search", [])
        
        if not results:
            logger.warning(f"No Wikipedia entry found for '{name}'")
            return {}

        exact_name = results[0].get("title")
        logger.info(f"Verified person: {name} => Exact name: {exact_name}")
        
        return {
            "title": exact_name,
            "exists": True
        }
    except Exception as e:
        logger.error(f"Wikipedia verification failed for '{name}': {e}")
    
    return {}

def get_wikimedia_images(title: str, limit: int = 5) -> list:
    """
    Step 2: Use Wikimedia Commons API to retrieve the best images using the exact name.
    Focuses on high-quality photos.
    """
    # 1. First find images on the Wikipedia page
    search_url = "https://en.wikipedia.org/w/api.php"
    headers = {
        "User-Agent": "Davi-vidrush/1.0 (https://github.com/cresus-ui/vidrush; contact@example.com)"
    }
    params = {
        "action": "query",
        "format": "json",
        "prop": "images",
        "titles": title,
        "imlimit": 20
    }

    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        pages = response.json().get("query", {}).get("pages", {})
        
        image_titles = []
        for page_data in pages.values():
            images = page_data.get("images", [])
            for img in images:
                t = img.get("title", "")
                # Skip icons and small graphics
                if any(ext in t.lower() for ext in [".jpg", ".jpeg", ".png"]):
                    if not any(skip in t.lower() for skip in ["icon", "logo", "flag", "stub"]):
                        image_titles.append(t)
        
        if not image_titles:
            return []

        # 2. Get high-quality URLs from Commons for these image titles
        commons_url = "https://commons.wikimedia.org/w/api.php"
        image_urls = []
        
        # Batch query for imageinfo
        image_batch = "|".join(image_titles[:10])
        commons_params = {
            "action": "query",
            "format": "json",
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": 1024, # Request high-res thumbnail
            "titles": image_batch
        }
        
        res = requests.get(commons_url, params=commons_params, headers=headers, timeout=10)
        res_pages = res.json().get("query", {}).get("pages", {})
        for img_page in res_pages.values():
            info = img_page.get("imageinfo", [{}])[0]
            url = info.get("url") # Or get thumburl if preferred
            if url:
                image_urls.append(url)
        
        return image_urls[:limit]
        
    except Exception as e:
        logger.error(f"Wikimedia Commons retrieval failed for '{title}': {e}")
        return []

def download_image(url: str, task_id: str, filename: str) -> str:
    """
    Download an image and return the local path.
    """
    img_dir = os.path.join(utils.task_dir(task_id), "people")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    # Clean the URL from query parameters (like ?utm_source...)
    if "?" in url:
        url = url.split("?")[0]

    # Sanitize filename
    safe_filename = "".join([c for c in filename if c.isalnum() or c in "._- "]).strip()
    ext = os.path.splitext(url)[1].lower() or ".jpg"
    file_path = os.path.join(img_dir, f"{safe_filename}{ext}")

    if os.path.exists(file_path):
        return file_path

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
        }
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    except Exception as e:
        logger.error(f"Failed to download image {url}: {e}")
        return ""
