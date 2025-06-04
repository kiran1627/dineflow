import csv
import math
import os
from datetime import datetime

ITEMS_PER_PAGE = 10

# Resolve the path to menu.csv relative to this file's location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # goes up two levels from models/
CSV_PATH = os.path.join(BASE_DIR, "database", "menu.csv")

STATIC_URL_PATH = "/static/images"

print(f"DEBUG: Loading menu items from: {CSV_PATH}")

def load_items():
    items = []
    try:
        with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['price'] = int(row['price'])
                image_filename = row.get("image", "")
                if image_filename:
                    row["image_url"] = f"{STATIC_URL_PATH}/{image_filename}"
                else:
                    row["image_url"] = None
                items.append(row)
    except Exception as e:
        print(f"Error loading items: {e}")
    return items

def get_recommended_items():
    items = load_items()
    if not items:
        return []

    total_pages = math.ceil(len(items) / ITEMS_PER_PAGE)

    now = datetime.utcnow()
    minutes_since_epoch = int(now.timestamp() // 60)
    page_index = (minutes_since_epoch // 10) % total_pages

    start = page_index * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    return items[start:end]
