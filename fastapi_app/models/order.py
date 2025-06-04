import csv
from datetime import datetime
import os

class Order:
    def __init__(self, order_id, customer_name, user_email, items, total_price, mode, order_type, timestamp, status="pending"):
        self.order_id = order_id
        self.customer_name = customer_name
        self.user_email = user_email
        self.items = items  # List of dicts or string
        self.total_price = total_price
        self.mode = mode
        self.order_type = order_type
        self.timestamp = timestamp
        self.status = status

    @staticmethod
    def save_to_csv(order_id, customer_name, user_email, items, total_price, mode, order_type, timestamp, status="pending"):
        try:
            file_path = os.path.join("database", "orders.csv")
            file_exists = os.path.isfile(file_path)

            # Convert items list to string
            items_str = "; ".join(
                [f"{item['name']} x{item['quantity']} @ ₹{item['price']}" for item in items]
            )

            with open(file_path, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                if not file_exists or os.path.getsize(file_path) == 0:
                    writer.writerow([
                        "order_id", "customer_name", "user_email", "items",
                        "total_price", "mode", "order_type", "timestamp", "status"
                    ])

                writer.writerow([
                    order_id,
                    customer_name,
                    user_email,
                    items_str,
                    total_price,
                    mode,
                    order_type,
                    timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    status
                ])

            return True
        except Exception as e:
            print(f"❌ Error saving order to CSV: {e}")
            return False

    @staticmethod
    def get_order_by_id(order_id):
        try:
            file_path = os.path.join("database", "orders.csv")
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["order_id"] == order_id:
                        return Order(
                            order_id=row["order_id"],
                            customer_name=row["customer_name"],
                            user_email=row["user_email"],
                            items=row["items"],
                            total_price=float(row["total_price"]),
                            mode=row["mode"],
                            order_type=row["order_type"],
                            timestamp=datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"),
                            status=row.get("status", "pending")
                        )
            return None
        except Exception as e:
            print(f"❌ Error reading order: {e}")
            return None
