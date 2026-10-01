"""
1 Search History Module
2 Stores every movie search (preferences, weights, top results) into a JSON file,
so the user can review what they searched for before.
"""

import json
import os
from datetime import datetime
from name import NAMES
HISTORY_FILE = "search_history.json"


# 1. LOAD existing history from the JSON file
def load_history():
    """Read the history file and return a list of past searches.
    If the file doesn't exist yet, return an empty list."""
    if not os.path.exists(HISTORY_FILE):
        return []                                   # no history yet

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # file exists but is empty or corrupted -> start fresh
        print("Warning: history file was corrupted. Starting a new one.")
        return []


# 2. SAVE the full history list back to the JSON file
def save_history(history_list):
    """Write the given list of search records to the JSON file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_list, f, indent=4)        # indent=4 makes it readable


# 3. ADD a new search record
def add_search_record(prefs, weights, top_results):
    """Create one record for this search and append it to the history file.

    top_results: list of dicts, as returned by recommend_with_details().
    Each dict looks like:
        {"movie": {...}, "score": 88.6, "level": "Highly recommended",
         "reasons": ["...", "..."]}
    """
    # Keep only the fields we actually want saved (JSON-friendly, no clutter)
    results_summary = []
    for result in top_results:
        results_summary.append({
            "title": result["movie"]["title"],
            "score": round(result["score"], 1),
            "level": result["level"],
            "reasons": result["reasons"]
        })

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "preferences": prefs,
        "weights": weights,
        "results": results_summary
    }

    history = load_history()        # read what's already there
    history.append(record)          # add the new record
    save_history(history)           # write everything back


# 4. VIEW history (for a "view recommended historys"option)
def show_history():
    """Print all past recommandations in a readable way."""
    history = load_history()

    if not history:
        print("No search history yet.")
        return

    for i, record in enumerate(history, start=1):
        print(f"\nSearch #{i} - {record['timestamp']}")
        print(f"  Preferences: {record['preferences']}")
        print("  Top results:")
        for r in record["results"]:
            print(f"    - {r['title']} ({r['score']}) - {r['level']}")
            print(f"      Why: {'; '.join(r['reasons'])}")


# 5. CLEAR history (optional reset option)
def clear_history():
    """Delete all saved search records."""
    save_history([])
    print("History cleared.")


# QUICK TEST
if __name__ == "__main__":
    fake_prefs = {"genre": "scifi", "mood": "thrilling", "era": "new",
                  "duration": "any", "rating": "high"}
    fake_weights = {"genre": 5, "mood": 3, "era": 2, "duration": 1, "rating": 4}
    fake_results = [
        {"movie": {"title": "Inception"}, "score": 88.6,
         "level": "Highly recommended", "reasons": ["Genre matches", "High rating"]},
        {"movie": {"title": "Die Hard"}, "score": 62.3,
         "level": "Recommended", "reasons": ["Mood matches"]},
    ]

    add_search_record(fake_prefs, fake_weights, fake_results)
    show_history()
