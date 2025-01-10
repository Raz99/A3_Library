import csv
from system.shared import users

USER_FILE = r"data\users.csv"
FIELD_NAMES = ["username", "password"]

def create_file_users():
    with open(USER_FILE, mode="w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writeheader()

def add_user(new_lib):
    with open(USER_FILE, mode="a") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writerow(new_lib.to_dict())

def update():
    with open(USER_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writeheader()
        for user in users:
            writer.writerow(user.to_dict())





