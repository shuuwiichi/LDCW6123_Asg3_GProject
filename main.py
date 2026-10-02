from movies import movies
from name import NAMES
from recommender import recommend_with_details
from similarity import closest_option
from history import add_search_record, show_history, clear_history

OPTIONS = {
    "genre": ["action", "scifi", "comedy", "animation", "romance", "fantasy", "thriller", "drama", "any"],
    "mood": ["funny", "touching", "thrilling", "any"],
    "era": ["new", "classic", "any"],
    "duration": ["short", "long", "any"],
    "rating": ["high", "any"],
}



def get_choice(prompt, options):
    while True:
        print("Options:", ", ".join(NAMES[x] for x in options))
        value = input(prompt).strip().lower()
        if value == "cancel":
            return "CANCEL"
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
        raw = input(f"Your preference for {label} (0-5): ").strip().lower()
        if raw == "cancel":
            return "CANCEL"
        try:
            value = int(raw)
            if 0 <= value <= 5:
                return value
        except ValueError:
            pass
        print("Please enter a WHOLE number from 0 to 5.")

def collect_preferences():
    """Ask the user for preferences and weights.
    Returns (None, None) if the user typed 'cancel' at any point to cancel."""
    print("\n********VIEWING PREFERENCES********")
    print("(Type 'cancel' at any time to cancel and return to the main menu.)")

    prefs = {}
    for key in OPTIONS:
        value = get_choice(f"{key.title()}: ", OPTIONS[key])
        if value == "CANCEL":
            return None, None               # cancel process
        prefs[key] = value

    print("\n********IMPORTANCE OF PREFERENCE********")
    weights = {}
    for key in OPTIONS:
        value = get_weight(key)
        if value == "CANCEL":
            return None, None               # cancel process
        weights[key] = value

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

def main():
    while True:
        print("\n********FILMMATCHER********")
        print("1. Find movies for me")
        print("2. View catalogue")
        print("3. How this program works")
        print("4. View recommendation history")
        print("5. Clear recommendation history")
        print("6. Exit")
        choice = input("Choose 1-6: ").strip()

        if choice == "1":
            prefs, weights = collect_preferences()
            if prefs is None:
                print("Search cancelled. Returning to main menu.")
            elif sum(weights.values()) == 0:
                print("Please give at least one preference a weight above 0.")
            else:
                results = recommend_with_details(movies, prefs, weights, 3)
                show_results(results)
                add_search_record(prefs, weights, results)
        elif choice == "2":
            show_catalogue()
        elif choice == "3":
            print("\nThis program compares genre, mood, era, duration and rating.")
            print("Each criteria uses if/elif matching.")
            print("Weights from 0-5 control how important each criteria is.")
            print("The final score is normalized to 0-100 and the top 3 are shown.")
        elif choice == "4":
            show_history()
        elif choice == "5":
            confirm = input("Are you sure you want to clear all history? [y/n]: ").strip().lower()
            if confirm in ("y", "yes"):
                clear_history()
        elif choice == "6":
            print("Thank you for using Filmmatcher!")
            break
        else:
            print("Invalid choice bro.")

if __name__ == "__main__":
    main()
