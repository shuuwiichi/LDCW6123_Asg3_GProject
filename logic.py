#movie list
movies = [
    {"title": "ABC",        "genre": "scifi",     "year": 2010, "rating": 1.0, "duration": 148, "mood": "thrilling"},
]

#logic
def match_genre(movie, pref):
    """Compare the movie genre with the user's preferred genre"""
    if pref == "any":
        return 0.5                      # no preference
    elif movie["genre"] == pref:
        return 1.0                      # exact match
    elif pref == "action" and movie["genre"] == "scifi":
        return 0.4                      # related genres get partial credit
    elif pref == "scifi" and movie["genre"] == "action":
        return 0.4
    elif pref == "comedy" and movie["genre"] == "animation":
        return 0.4
    elif pref == "animation" and movie["genre"] == "comedy":
        return 0.4
    elif pref == "romance" and movie["genre"] == "comedy":
        return 0.3
    else:
        return 0.0


def match_mood(movie, pref):
    """Compare the movie mood with the user's preferred mood"""
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
    """Movie 'new' or 'classic'"""
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
    else:                               # "any"
        return 0.5


def match_duration(movie, pref):
    """Time 'short' or 'long'"""
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
    else:                               # "any"
        return 0.5


def match_rating(movie, pref):
    """Reward higher-rated movies if user cares about quality."""
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
    else:                               # "any"
        return 0.5


# WEIGHTED SCORING
# prefs   : dict of the user's preferred value for each aspect
# weights : dict of importance (0-5) for each aspect（keyin)
# Returns final score 0 to 100.
def calculate_score(movie, prefs, weights):
    """Combine all match values using the user's weights."""
    total = 0.0
    total += match_genre(movie, prefs["genre"])       * weights["genre"]
    total += match_mood(movie, prefs["mood"])         * weights["mood"]
    total += match_era(movie, prefs["era"])           * weights["era"]
    total += match_duration(movie, prefs["duration"]) * weights["duration"]
    total += match_rating(movie, prefs["rating"])     * weights["rating"]

    max_possible = sum(weights.values())              # best possible total
    if max_possible == 0:
        return 0.0                                    # avoid division by zero
    return total / max_possible * 100                 # normalize to 0-100


def get_level(score):
    """Convert a numeric score into a recommendation label."""
    if score >= 80:
        return "Highly recommended!"
    elif score >= 60:
        return "Recommended"
    elif score >= 40:
        return "Worth a look"
    else:
        return "Not a great fit"



#RECOMMEND: score all movies, sort, return the top n
def recommend(movie_list, prefs, weights, top_n=3):
    """Return the top N movies as (score, movie) pairs, best first."""
    results = []
    for movie in movie_list:
        score = calculate_score(movie, prefs, weights)
        results.append((score, movie))

    results.sort(key=lambda pair: pair[0], reverse=True)   #lamda=get input and return #reverst=from high to low
    return results[:top_n]


#TEST
if __name__ == "__main__":
    test_prefs = {"genre": "scifi", "mood": "thrilling", "era": "new",
                  "duration": "any", "rating": "high"}
    test_weights = {"genre": 5, "mood": 3, "era": 2,
                    "duration": 1, "rating": 4}

    for score, m in recommend(movies, test_prefs, test_weights, top_n=3):
        print(f"{m['title']:<15} {score:5.1f}  {get_level(score)}")