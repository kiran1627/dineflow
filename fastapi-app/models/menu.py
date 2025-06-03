import csv
import os

# Path to the CSV file
MENU_CSV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "database", "menu.csv")
)

class MenuItem:
    def __init__(self, item_id, name, price, category, description, image_filename=None):
        self.item_id = int(item_id)
        self.name = name
        self.price = float(price)
        self.category = category
        self.description = description
        self.image = f"/static/images/{image_filename.strip()}" if image_filename else "/static/images/default.jpg"

    def to_dict(self):
        return {
            "id": self.item_id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "description": self.description,
            "image": self.image
        }

    @staticmethod
    def get_all_items():
        items = []
        try:
            with open(MENU_CSV_PATH, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        item = MenuItem(
                            item_id=row.get("item_id", 0),
                            name=row.get("name", "Unknown"),
                            price=row.get("price", 0),
                            category=row.get("category", "Uncategorized"),
                            description=row.get("description", "No description available"),
                            image_filename=row.get("image", "")
                        )
                        items.append(item)
                    except Exception as e:
                        print(f"⚠️ Skipping row due to error: {e}")
        except FileNotFoundError:
            print("❌ menu.csv not found at:", MENU_CSV_PATH)
        except Exception as e:
            print("❌ Error reading menu.csv:", e)

        return items

    @staticmethod
    def get_menu_item_by_id(item_id: int):
        try:
            with open(MENU_CSV_PATH, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if int(row.get("item_id", -1)) == item_id:
                        return MenuItem(
                            item_id=row.get("item_id"),
                            name=row.get("name"),
                            price=row.get("price"),
                            category=row.get("category"),
                            description=row.get("description"),
                            image_filename=row.get("image")
                        )
        except Exception as e:
            print("❌ Error finding item by ID:", e)

        return None
