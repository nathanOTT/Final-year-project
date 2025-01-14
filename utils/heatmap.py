import os
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend to avoid GUI issues
import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from database.models import PlayerStat

def generate_heatmap(player_id: int, db: Session):
    """
    Generate a heatmap for a player's stats.

    Args:
        player_id (int): Player's unique identifier.
        db (Session): Database session.

    Returns:
        str: Path to the saved heatmap image.
    """
    stats = db.query(PlayerStat).filter(PlayerStat.player_id == player_id).all()
    if not stats:
        print(f"No data found for player {player_id}")
        return None

    # Extract data for the heatmap
    timestamps = [stat.timestamp for stat in stats]
    distances = [stat.distance for stat in stats]
    speeds = [stat.speed for stat in stats]

    # Create the heatmap (time-series plot)
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, speeds, label="Speed (km/h)", color="blue")
    plt.plot(timestamps, distances, label="Distance (km)", color="green")
    plt.xlabel("Date")
    plt.ylabel("Metrics")
    plt.title(f"Player {player_id} Performance")
    plt.legend()
    plt.grid()

    # Save the heatmap
    output_dir = "heatmaps"
    os.makedirs(output_dir, exist_ok=True)
    heatmap_path = f"{output_dir}/player_{player_id}_heatmap.png"
    plt.savefig(heatmap_path)
    plt.close()

    return heatmap_path
