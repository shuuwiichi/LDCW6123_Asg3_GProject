def match_genre(movie, pref):
    #separated by which ones are allowed to overlap
    """compare genre with user preference"""
    if pref == "any":
        return 0.5

    elif movie["genre"] == pref:
        return 1.0

    elif pref == "action" and movie["genre"] == "scifi":
        return 0.4
    elif pref == "scifi" and movie["genre"] == "action":
        return 0.4
    
    elif pref == "fantasy" and movie["genre"] == "action":
        return 0.4
    elif pref == "action" and movie["genre"] == "fantasy":
        return 0.4

    elif pref == "fantasy" and movie["genre"] == "scifi":
        return 0.3
    elif pref == "scifi" and movie["genre"] == "fantasy":
        return 0.3

    elif pref == "comedy" and movie["genre"] == "animation":
        return 0.4
    elif pref == "animation" and movie["genre"] == "comedy":
        return 0.4

    elif pref == "romance" and movie["genre"] == "comedy":
        return 0.3
    elif pref == "comedy" and movie["genre"] == "romance":
        return 0.3
    
    elif pref == "romance" and movie["genre"] == "drama":
        return 0.4
    elif pref == "drama" and movie["genre"] == "romance":
        return 0.4
    
    elif pref == "thriller" and movie["genre"] == "action":
        return 0.4
    elif pref == "action" and movie["genre"] == "thriller":
        return 0.4
    
    elif pref == "thriller" and movie["genre"] == "scifi":
        return 0.3
    elif pref == "scifi" and movie["genre"] == "thriller":
        return 0.3
    
    elif pref == "thriller" and movie["genre"] == "drama":
        return 0.3
    elif pref == "drama" and movie["genre"] == "thriller":
        return 0.3
    
    elif pref == "fantasy" and movie["genre"] == "romance":
        return 0.3
    elif pref == "romance" and movie["genre"] == "fantasy":
        return 0.3

    else:
        return 0.0

def match_mood(movie, pref):
    """compare mood with user pref"""
    if pref == "any":
        return 0.5
    elif movie["mood"] == pref:
        return 1.0
    elif pref == "funny" and movie["mood"] == "touching":
        return 0.3
    elif pref == "touching" and movie["mood"] == "funny":
        return 0.3
    else:
        return 0.0

def match_era(movie, pref):
    """compare era with user pref"""
    year = movie["year"]
    if pref == "new":
        if year >= 2015:
            return 1.0
        elif year >= 2005:
            return 0.6
        elif year >= 1995:
            return 0.3
        else:
            return 0.0
    elif pref == "classic":
        if year < 2000:
            return 1.0
        elif year < 2010:
            return 0.5
        else:
            return 0.0
    else:
        return 0.5

def match_duration(movie, pref):
    """compare duration with user pref"""
    minutes = movie["duration"]
    if pref == "short":
        if minutes < 100:
            return 1.0
        elif minutes < 130:
            return 0.5
        else:
            return 0.0
    elif pref == "long":
        if minutes >= 150:
            return 1.0
        elif minutes >= 120:
            return 0.5
        else:
            return 0.0
    else:
        return 0.5

def match_rating(movie, pref):
    """compare ratings with user pref"""
    rating = movie["rating"]
    if pref == "high":
        if rating >= 8.5:
            return 1.0
        elif rating >= 8.0:
            return 0.7
        elif rating >= 7.5:
            return 0.4
        else:
            return 0.1
    else:
        return 0.5

def calculate_score(movie, prefs, weights):
    """calc matching score"""
    total = 0.0
    total += match_genre(movie, prefs["genre"]) * weights["genre"]
    total += match_mood(movie, prefs["mood"]) * weights["mood"]
    total += match_era(movie, prefs["era"]) * weights["era"]
    total += match_duration(movie, prefs["duration"]) * weights["duration"]
    total += match_rating(movie, prefs["rating"]) * weights["rating"]
    max_possible = sum(weights.values())
    if max_possible == 0:
        return 0.0
    return total / max_possible * 100

def get_level(score):
    """calc rec level"""
    if score >= 80:
        return "Highly recommended!"
    elif score >= 60:
        return "Recommended"
    elif score >= 40:
        return "Worth a look"
    else:
        return "Not a great fit"

def recommend(movie_list, prefs, weights, top_n=3):
    """show rec list"""
    results = []
    for movie in movie_list:
        score = calculate_score(movie, prefs, weights)
        results.append((score, movie))
    results.sort(key=lambda pair: pair[0], reverse=True)
    return results[:top_n]

if __name__ == "__main__":
    test_movie = {
        "title": "Test Movie", "genre": "scifi", "year": 2020,
        "rating": 8.8, "duration": 148, "mood": "thrilling"
    }
    prefs = {"genre": "scifi", "mood": "thrilling", "era": "new",
             "duration": "any", "rating": "high"}
    weights = {"genre": 5, "mood": 3, "era": 2, "duration": 1, "rating": 4}
    score = calculate_score(test_movie, prefs, weights)
    print(f"{test_movie['title']:<15} {score:5.1f}  {get_level(score)}")

    #ggfuckingez heydontsaythat really fugginez loginnewskin