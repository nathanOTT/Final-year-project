import pandas as pd
from sqlalchemy.orm import Session
from database.models import PlayerStat

def load_data_to_db(file_path: str, db: Session):
    """
    Load data from a CSV file into the database.

    Args:
        file_path: Path to the CSV file (e.g., "/Users/nathanielani/Documents/Final year project/Final-year-project/dataset.csv")
        db: Database session
    """
    try:
        # Load the dataset
        data = pd.read_csv(file_path)

        # Ensure the dataset has the required columns
        required_columns = {"player_id", "speed", "distance", "timestamp"}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"Dataset must contain the following columns: {required_columns}")

        # Convert timestamp to datetime format
        data["timestamp"] = pd.to_datetime(data["timestamp"])

        # Insert records into the database
        for _, row in data.iterrows():
            stat = PlayerStat(
                player_id=row["player_id"],
                speed=row["speed"],
                distance=row["distance"],
                timestamp=row["timestamp"]
            )
            db.add(stat)

        db.commit()
        print(f"Data from {file_path} successfully loaded into the database.")
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
