from movies import movies
from recommender import recommend_with_details
from similarity import closest_option

OPTIONS = {
    "genre": ["action", "scifi", "comedy", "animation", "romance", "fantasy", "thriller","any"],
    "mood": ["funny", "touching", "thrilling", "any"],
    "era": ["new", "classic", "any"],
    "duration": ["short", "long", "any"],
    "rating": ["high", "any"],
}

NAMES = {
    "scifi": "Sci-Fi", "any": "Any", "action": "Action", "comedy": "Comedy",
    "animation": "Animation", "romance": "Romance", "fantasy": "Fantasy", "thriller": "Thriller", "funny": "Funny",
    "touching": "Touching", "thrilling": "Thrilling", "new": "New",
    "classic": "Classic", "short": "Short", "long": "Long", "high": "High-rated",
}

def get_choice(prompt, options):
    while True:
        print("Options:", ", ".join(NAMES[x] for x in options))
        value = input(prompt).strip().lower()
        if value in options:
            return value
        corrected, score = closest_option(value, options)
        if corrected:
            answer = input(f'Sorry, did you mean "{NAMES[corrected]}"? [y/n]: ').strip().lower()
            if answer in ("y", "yes"):
                return corrected
        print("Invalid choice. Please try again.")