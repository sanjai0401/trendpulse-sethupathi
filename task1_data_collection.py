import requests
import time
import json
import os
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required header
headers = {"User-Agent": "TrendPulse/1.0"}

# Categories with keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Function to assign category based on title
def get_category(title):
    title = title.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title:
                return category
    return None  # ignore if no category matched


def main():
    print("Fetching top stories...")

    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        response.raise_for_status()
        story_ids = response.json()[:500]  # first 500
    except Exception as e:
        print("Failed to fetch top stories:", e)
        return

    collected_data = []
    category_count = {cat: 0 for cat in categories}

    for story_id in story_ids:
        try:
            url = ITEM_URL.format(story_id)
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            story = res.json()
        except Exception as e:
            print(f"Failed to fetch story {story_id}: {e}")
            continue

        if not story or "title" not in story:
            continue

        title = story.get("title", "")
        category = get_category(title)

        # skip if no category
        if category is None:
            continue

        # limit 25 per category
        if category_count[category] >= 25:
            continue

        # Extract required fields
        record = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", ""),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_data.append(record)
        category_count[category] += 1

        # Stop if all categories filled
        if all(count >= 25 for count in category_count.values()):
            break

    # Sleep per category (as required)
    for cat in categories:
        time.sleep(2)

    # Create data folder if not exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # File name with date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print(f"Collected {len(collected_data)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()
