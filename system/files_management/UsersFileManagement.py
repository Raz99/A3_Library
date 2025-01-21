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
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during setup: {e}")

def create_file_users():
    try:
        # Create an empty DataFrame with the specified columns
        df = pd.DataFrame(columns=FIELD_NAMES)
        # Save the empty DataFrame to CSV
        df.to_csv(USER_FILE_PATH, index=False)
    except PermissionError:
        raise PermissionError(f"Permission denied: Unable to create file '{USER_FILE_PATH}'.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while creating the user file: {e}")



def add_user(new_lib):
    try:
        # Convert single user to DataFrame and append to existing CSV
        user_data = pd.DataFrame([new_lib.to_dict()], columns=FIELD_NAMES)
        user_data.to_csv(USER_FILE_PATH, mode='a', header=False, index=False)
    except PermissionError:
        raise PermissionError(f"Permission denied: Unable to write to file '{USER_FILE_PATH}'.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while adding a user: {e}")


def update():
    try:
        # Convert list of users to a pandas DataFrame
        users_data = [user.to_dict() for user in shared.users]
        df = pd.DataFrame(users_data, columns=FIELD_NAMES)

        # Write to CSV file
        df.to_csv(USER_FILE_PATH, index=False)
    except PermissionError:
        raise PermissionError(f"Permission denied: Unable to write to file '{USER_FILE_PATH}'.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while updating the user file: {e}")