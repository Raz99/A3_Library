import pandas as pd
from system.shared import users

USER_FILE = r"data\users.csv"
FIELD_NAMES = ["username", "password"]


def create_file_users():
    # Create an empty DataFrame with the specified columns
    df = pd.DataFrame(columns=FIELD_NAMES)
    # Save the empty DataFrame to CSV
    df.to_csv(USER_FILE, index=False)


def add_user(new_lib):
    # Convert single user to DataFrame and append to existing CSV
    user_data = pd.DataFrame([new_lib.to_dict()], columns=FIELD_NAMES)
    user_data.to_csv(USER_FILE, mode='a', header=False, index=False)


def update():
    # Convert list of users to a pandas DataFrame
    users_data = [user.to_dict() for user in users]
    df = pd.DataFrame(users_data, columns=FIELD_NAMES)

    # Write to CSV file
    df.to_csv(USER_FILE, index=False)