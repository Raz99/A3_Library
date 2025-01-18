import pandas as pd
from system import shared
from system.User import User

USER_FILE_PATH = r"data\users.csv"
FIELD_NAMES = ["username", "password"]

def setup():
    try:
        df = pd.read_csv(USER_FILE_PATH)
        for _, row in df.iterrows():
            current = User(row["username"],str(row["password"]))
            shared.users.append(current)

    except FileNotFoundError:
        create_file_users()

def create_file_users():
    # Create an empty DataFrame with the specified columns
    df = pd.DataFrame(columns=FIELD_NAMES)
    # Save the empty DataFrame to CSV
    df.to_csv(USER_FILE_PATH, index=False)


def add_user(new_lib):
    # Convert single user to DataFrame and append to existing CSV
    user_data = pd.DataFrame([new_lib.to_dict()], columns=FIELD_NAMES)
    user_data.to_csv(USER_FILE_PATH, mode='a', header=False, index=False)


def update():
    # Convert list of users to a pandas DataFrame
    users_data = [user.to_dict() for user in shared.users]
    df = pd.DataFrame(users_data, columns=FIELD_NAMES)

    # Write to CSV file
    df.to_csv(USER_FILE_PATH, index=False)