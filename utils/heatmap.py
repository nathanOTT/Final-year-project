import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from database.models import PlayerStat
import os

def generate_heatmap(player_id: str, db: Session, output_dir: str = "heatmaps"):
    """
    Generate heatmaps for a player's stats and save them as images.
    
    Args:
        player_id: ID of the player to generate the heatmap for.
        db: Database session.
        output_dir: Directory to save the heatmap images.
        
    Returns:
        Dictionary containing paths to the saved heatmaps.
    """
    # Query the player's stats from the database
    stats = db.query(PlayerStat).filter(PlayerStat.player_id == player_id).all()

    if not stats:
        return None  # No data found for the given player ID

    # Convert stats to a DataFrame
    data = pd.DataFrame([{
        "timestamp": stat.timestamp,
        "speed": stat.speed,
        "distance": stat.distance
    } for stat in stats])

    # Convert timestamp to datetime and set as index
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data.set_index("timestamp", inplace=True)

    # Create pivot tables for heatmap data
    speed_pivot = data.pivot_table(values="speed", index=data.index.date, columns=data.index.hour, aggfunc="mean")
    distance_pivot = data.pivot_table(values="distance", index=data.index.date, columns=data.index.hour, aggfunc="sum")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Paths to save heatmaps
    heatmap_paths = {}

    # Generate Speed Heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(speed_pivot, annot=True, fmt=".1f", cmap="YlGnBu", cbar=True)
    plt.title(f"Speed Heatmap for Player {player_id}")
    plt.xlabel("Hour of Day")
    plt.ylabel("Date")
    speed_path = os.path.join(output_dir, f"speed_heatmap_{player_id}.png")
    plt.savefig(speed_path)
    plt.close()
    heatmap_paths["speed"] = speed_path

    # Generate Distance Heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(distance_pivot, annot=True, fmt=".1f", cmap="YlGnBu", cbar=True)
    plt.title(f"Distance Heatmap for Player {player_id}")
    plt.xlabel("Hour of Day")
    plt.ylabel("Date")
    distance_path = os.path.join(output_dir, f"distance_heatmap_{player_id}.png")
    plt.savefig(distance_path)
    plt.close()
    heatmap_paths["distance"] = distance_path

    return heatmap_paths
