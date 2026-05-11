import random
from loguru import logger

# Mapping of script categories to FFmpeg xfade transition types
# Only use universally supported transition names.
# Full list: fade, wipeleft, wiperight, wipeup, wipedown, slideleft, slideright,
# slideup, slidedown, circlecrop, rectcrop, distance, fadeblack, fadewhite,
# radial, smoothleft, smoothright, smoothup, smoothdown, circleopen, circleclose,
# vertopen, vertclose, horzopen, horzclose, dissolve, pixelize, diagtl, diagtr,
# diagbl, diagbr, hlslice, hrslice, vuslice, vdslice, hblur
TRANSITION_MAP = {
    "finance": [
        "radial", "circleopen", "distance", "dissolve", "pixelize", "wipeleft", "wiperight"
    ],
    "biography": [
        "fade", "dissolve", "smoothleft", "smoothright", "rectcrop", "fadeblack"
    ],
    "news": [
        "slideleft", "slideright", "slideup", "slidedown", "pixelize", "hlslice", "diagtl"
    ],
    "emotional": [
        "fade", "hblur", "dissolve", "fadewhite", "fadeblack", "smoothleft"
    ]
}

def get_random_transition(category: str) -> str:
    """
    Get a random transition name suitable for the given category.
    """
    category = category.lower()
    if category not in TRANSITION_MAP:
        category = "finance" # Default
    
    transitions = TRANSITION_MAP[category]
    return random.choice(transitions)

def get_zoom_speed(category: str) -> float:
    """
    Return appropriate zoom speed for the category (TikTok-style).
    """
    speeds = {
        "finance": 0.005,    # Dynamic and fast
        "biography": 0.002,  # Cinematic/Slow
        "news": 0.004,       # Engaging
        "emotional": 0.0015  # Very slow and deep
    }
    return speeds.get(category.lower(), 0.002)

def generate_xfade_filter_complex(video_count: int, transition_names: list, durations: list, offset_step: float):
    """
    Generates a complex filter string for concatenating videos with xfade.
    Note: xfade is complex for multiple clips. For N clips, we need N-1 xfade filters.
    """
    # This is a complex logic that will be implemented in video.py
    pass
