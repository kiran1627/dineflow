import csv
import os
from datetime import datetime

class Booking:
    @staticmethod
    def save_to_csv(
        booking_id: str,
        customer_name: str,
        email: str,
        phone: str,
        date: str,
        time: str,
        guests: int,
        timestamp: datetime,
        status: str = "pending"
    ) -> bool:
        try:
            os.makedirs("database", exist_ok=True)
            file_path = os.path.join("database", "bookings.csv")
            file_exists = os.path.isfile(file_path)

            with open(file_path, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not file_exists or os.path.getsize(file_path) == 0:
                    writer.writerow([
                        "booking_id", "customer_name", "email", "phone",
                        "date", "time", "guests", "timestamp", "status"
                    ])
                writer.writerow([
                    booking_id,
                    customer_name,
                    email,
                    phone,
                    date,
                    time,
                    guests,
                    timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    status
                ])
            return True
        except Exception as e:
            print(f"❌ Error saving booking to CSV: {e}")
            return False
