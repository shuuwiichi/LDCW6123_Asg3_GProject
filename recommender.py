from logic import (
    calculate_score, get_level,
    match_genre, match_mood, match_era, match_duration, match_rating
)

CRITERIA = (
    ("genre", "Genre", match_genre), ("mood", "Mood", match_mood), ("era", "Era", match_era),   
    ("duration", "Duration", match_duration), ("rating", "Rating", match_rating),
)