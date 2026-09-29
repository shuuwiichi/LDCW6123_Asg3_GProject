from logic import (
    calculate_score, get_level,
    match_genre, match_mood, match_era, match_duration, match_rating
)

CRITERIA = (
    ("genre", "Genre", match_genre), ("mood", "Mood", match_mood), ("era", "Era", match_era),   
    ("duration", "Duration", match_duration), ("rating", "Rating", match_rating),
)

def explain_match(movie, prefs, weights):
    reasons = []
    for key, label, matcher in CRITERIA:
        value = matcher(movie, prefs[key])
        if weights[key] > 0:
            if value >= 0.7:
                reasons.append(f"{label} matches your preference, check it out!")
            elif value > 0:
                reasons.append(f"{label} is a partial match, give it a chance maybe?")
    if not reasons:
        reasons.append("It received the highest score among the available titles")
    return reasons

def recommend_with_details(movie_list, prefs, weights, top_n=3):
    results = []
    for movie in movie_list:
        score = calculate_score(movie, prefs, weights)
        results.append({
            "score": score,
            "movie": movie,
            "level": get_level(score),
            "reasons": explain_match(movie, prefs, weights),
        })
    results.sort(key=lambda item: (-item["score"], item["movie"]["title"]))
    return results[:top_n]