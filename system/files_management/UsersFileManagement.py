import pandas as pd
from system import shared
from system.User import User

# Path to the CSV file containing user data
USER_FILE_PATH = r"data\users.csv"

# Field names for the user data
FIELD_NAMES = ["username", "password"]

def setup():
    """
    Sets up the user system by reading the users from the CSV file and initializing the shared users list.

    Reads the CSV file, creates user instances, and populates the shared users list.
    If the CSV file is not found, it creates a new file.
    """
    try:
        df = pd.read_csv(USER_FILE_PATH)
        for _, row in df.iterrows():
            current = User(row["username"], str(row["password"]))
            shared.users.append(current)
    except FileNotFoundError:
        create_file_users()
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during setup: {e}")

def create_file_users():
    """
    Creates a new CSV file for users with the specified columns.

    Creates an empty DataFrame with the specified columns and saves it to the CSV file.
    """
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
    """
    Adds a new user to the users CSV file.

    Converts the new user instance to a pandas DataFrame and appends it to the existing CSV file.

    Args:
        new_lib (User): The new user instance to add.
    """
    try:
        # Convert single user to DataFrame and append to existing CSV
        user_data = pd.DataFrame([new_lib.to_dict()], columns=FIELD_NAMES)
        user_data.to_csv(USER_FILE_PATH, mode='a', header=False, index=False)
    except PermissionError:
        raise PermissionError(f"Permission denied: Unable to write to file '{USER_FILE_PATH}'.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while adding a user: {e}")

def update():
    """
    Updates the users CSV file with the current state of the shared users list.

    Converts the shared users list to a pandas DataFrame and writes it to the CSV file.
    """
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