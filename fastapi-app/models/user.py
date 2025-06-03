import csv
import os

USER_CSV = os.path.join(os.path.dirname(__file__), "..", "database", "users.csv")

class User:
    def __init__(self, username, email, hashed_password):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

    def save(self):
        file_exists = os.path.isfile(USER_CSV)
        with open(USER_CSV, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['username', 'email', 'hashed_password'])
            writer.writerow([self.username, self.email, self.hashed_password])

    @staticmethod
    def get_user_by_username(username):
        try:
            with open(USER_CSV, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == username:
                        return User(row['username'], row['email'], row['hashed_password'])
        except FileNotFoundError:
            return None
        return None
