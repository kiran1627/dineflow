import csv
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

DATABASE_DIR = "database"
CSV_FILE = os.path.join(DATABASE_DIR, "orders.csv")


class OrderTrack:
    FLOW = {
        "dinein": ["pending", "confirmed", "preparing", "ready", "served"],
        "online": ["pending", "confirmed", "preparing", "ready", "delivered"],
    }

    @staticmethod
    def _normalize_mode(mode: str) -> str:
        return mode.lower().replace("-", "").replace(" ", "")

    @staticmethod
    def _normalize_status(status: str) -> str:
        return status.lower().strip()

    @staticmethod
    def _ensure_file() -> None:
        os.makedirs(DATABASE_DIR, exist_ok=True)
        if not os.path.isfile(CSV_FILE):
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "order_id", "customer_name", "user_email", "items",
                    "total_price", "mode", "order_type", "timestamp", "status"
                ])

    @staticmethod
    def _read_all() -> List[Dict[str, str]]:
        OrderTrack._ensure_file()
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    @staticmethod
    def _write_all(rows: List[Dict[str, str]]) -> None:
        OrderTrack._ensure_file()
        if not rows:
            return
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def list_all() -> List[Dict[str, str]]:
        return OrderTrack._read_all()

    @staticmethod
    def list_by_mode(mode: str) -> List[Dict[str, str]]:
        norm_mode = OrderTrack._normalize_mode(mode)
        if norm_mode not in OrderTrack.FLOW:
            raise ValueError("mode must be 'dine-in' or 'online'")
        return [r for r in OrderTrack._read_all() if OrderTrack._normalize_mode(r["mode"]) == norm_mode]

    @staticmethod
    def get_one(order_id: str) -> Optional[Dict[str, str]]:
        for row in OrderTrack._read_all():
            if row["order_id"] == order_id:
                return row
        return None

    @staticmethod
    def set_status(order_id: str, new_status: str) -> bool:
        new_status = OrderTrack._normalize_status(new_status)
        rows = OrderTrack._read_all()
        updated = False
        for row in rows:
            if row["order_id"] == order_id:
                mode = OrderTrack._normalize_mode(row["mode"])
                flow = OrderTrack.FLOW.get(mode, [])
                if new_status != "cancelled" and new_status not in flow:
                    raise ValueError(f"Status '{new_status}' invalid for mode '{mode}'")
                row["status"] = new_status
                row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updated = True
                break
        if updated:
            OrderTrack._write_all(rows)
        return updated

    @staticmethod
    def advance_status(order_id: str) -> Optional[str]:
        rows = OrderTrack._read_all()
        for row in rows:
            if row["order_id"] == order_id:
                mode = OrderTrack._normalize_mode(row["mode"])
                flow = OrderTrack.FLOW.get(mode, [])
                current_status = OrderTrack._normalize_status(row.get("status", ""))
                if current_status == "cancelled" or current_status not in flow:
                    return None
                idx = flow.index(current_status)
                if idx >= len(flow) - 1:
                    return None
                new_status = flow[idx + 1]
                row["status"] = new_status
                row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                OrderTrack._write_all(rows)
                return new_status
        return None

    @staticmethod
    def add_order(order: Dict[str, str]) -> None:
        OrderTrack._ensure_file()

        order["mode"] = OrderTrack._normalize_mode(order["mode"])
        if order["mode"] not in OrderTrack.FLOW:
            raise ValueError("Invalid mode")

        required = ["order_id", "customer_name", "user_email", "items", "total_price", "order_type"]
        for r in required:
            if r not in order:
                raise ValueError(f"Missing field: {r}")

        if isinstance(order["items"], list):
            order["items"] = json.dumps(order["items"], ensure_ascii=False)

        order["status"] = "pending"
        order["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "order_id", "customer_name", "user_email", "items",
                "total_price", "mode", "order_type", "timestamp", "status"
            ])
            writer.writerow(order)
