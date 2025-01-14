import pandas as pd
from sqlalchemy.orm import Session
from database.models import PlayerStat

def load_data_to_db(db: Session):
    """
    Load data from the CSV file into the database.

    Args:
        db: Database session.
    """
    file_path = ("/Users/nathanielani/Documents/Final year project/Final-year-project/dailyActivity_merged.csv")

    try:
        print(f"Loading data from: {file_path}")
        # Load the dataset
        data = pd.read_csv(file_path)
        print(f"Dataset loaded. Number of rows: {len(data)}")

        # Validate the required columns
        required_columns = {"Id", "ActivityDate", "TotalSteps", "TotalDistance"}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"Dataset must contain the following columns: {required_columns}")

        # Preprocess the data
        data["ActivityDate"] = pd.to_datetime(data["ActivityDate"], errors='coerce')  # Ensure correct date format
        data["Speed"] = data["TotalDistance"] / 24  # Assuming average distance spread across 24 hours
        print(f"Preview of processed data:\n{data[['Id', 'ActivityDate', 'TotalSteps', 'TotalDistance', 'Speed']].head()}")

        # Insert records into the database
        for _, row in data.iterrows():
            stat = PlayerStat(
                player_id=row["Id"],  # Use the Id column as player_id
                speed=row["Speed"],
                distance=row["TotalDistance"],
                timestamp=row["ActivityDate"]
            )
            db.add(stat)

        db.commit()
        print(f"Data successfully inserted into the database.")
        print(f"Records in the database after commit: {db.query(PlayerStat).count()}")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
