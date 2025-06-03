from fastapi import APIRouter
import csv
import os
from collections import defaultdict

router = APIRouter()

ORDERS_CSV = os.path.join(os.path.dirname(__file__), "..", "database", "orders.csv")
MENU_CSV = os.path.join(os.path.dirname(__file__), "..", "database", "menu.csv")

@router.get("/summary")
def get_analytics_summary():
    total_orders = 0
    total_revenue = 0.0
    order_values = []

    item_sales = defaultdict(int)  # item_name -> quantity sold

    try:
        with open(ORDERS_CSV, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_orders += 1
                total = float(row.get("total_price", 0.0))
                total_revenue += total
                order_values.append(total)

                # Assuming each order has a comma-separated list of item names
                items = row.get("items", "").split(",")
                for item in items:
                    item = item.strip()
                    item_sales[item] += 1

    except FileNotFoundError:
        return {
            "total_orders": 0,
            "total_revenue": 0.0,
            "average_order_value": 0.0,
            "top_items": []
        }

    top_items = sorted(item_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    avg_order_value = total_revenue / total_orders if total_orders else 0.0

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "average_order_value": round(avg_order_value, 2),
        "top_items": [{"item": k, "count": v} for k, v in top_items]
    }
