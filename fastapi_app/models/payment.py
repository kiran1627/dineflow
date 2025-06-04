import csv
import os
import uuid
from datetime import datetime

class Payment:
    def __init__(self, payment_id, order_id, amount, method, status, timestamp):
        self.payment_id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.method = method
        self.status = status
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "order_id": self.order_id,
            "amount": self.amount,
            "method": self.method,
            "status": self.status,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @staticmethod
    def create_payment(order_id, amount, method):
        try:
            payment_id = str(uuid.uuid4())
            status = "Success"
            timestamp = datetime.now()

            file_path = os.path.join("database", "payments.csv")
            file_exists = os.path.isfile(file_path)

            with open(file_path, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                if not file_exists or os.path.getsize(file_path) == 0:
                    writer.writerow([
                        "payment_id", "order_id", "amount",
                        "method", "status", "timestamp"
                    ])

                writer.writerow([
                    payment_id,
                    order_id,
                    amount,
                    method,
                    status,
                    timestamp.strftime("%Y-%m-%d %H:%M:%S")
                ])

            return Payment(payment_id, order_id, amount, method, status, timestamp)

        except Exception as e:
            print(f"❌ Error saving payment: {e}")
            return None

    @staticmethod
    def get_all_payments():
        payments = []
        try:
            file_path = os.path.join("database", "payments.csv")
            if not os.path.exists(file_path):
                return payments  # Return empty list if file doesn't exist

            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    payment = Payment(
                        payment_id=row["payment_id"],
                        order_id=row["order_id"],
                        amount=float(row["amount"]),
                        method=row["method"],
                        status=row["status"],
                        timestamp=datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                    )
                    payments.append(payment)

        except Exception as e:
            print(f"❌ Error reading payments: {e}")

        return payments
