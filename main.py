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

def get_weight(label):
    while True:
        raw = input(f"Your preference for {label} (0-5): ").strip()
        try:
            value = int(raw)
            if 0 <= value <= 5:
                return value
        except ValueError:
            pass
        print("Please enter a WHOLE number from 0 to 5.")

def collect_preferences():
    print("\n********VIEWING PREFERENCES********")
    prefs = {key: get_choice(f"{key.title()}: ", OPTIONS[key]) for key in OPTIONS}
    print("\n********IMPORTANCE OF PREFERENCE********")
    weights = {key: get_weight(key) for key in OPTIONS}
    return prefs, weights

def show_results(results):
    print("\n********RECOMMENDATIONS********")
    for i, result in enumerate(results, 1):
        m = result["movie"]
        print(f"\n{i}. {m['title']}")
        print(f"   Score: {result['score']:.1f}/100 - {result['level']}")
        print(f"   {NAMES[m['genre']]} | {m['year']} | {m['rating']:.1f}/10 | {m['duration']} min | {NAMES[m['mood']]}")
        print("   Why:", "; ".join(result["reasons"]))

def show_catalogue():
    print("\n********CATALOGUE********")
    for m in sorted(movies, key=lambda x: x["title"]):
        print(f"{m['title']:<35} {m['year']} | {m['rating']:.1f}/10 | {m['duration']:>3} min | {NAMES[m['genre']]} | {NAMES[m['mood']]}")