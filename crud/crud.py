# crud.py

from sqlalchemy.orm import Session
from database.models import PlayerStat

def create_player_stat(db: Session, player_id: int, speed: float, distance: float) -> PlayerStat:
    """
    Add a new record to the player stats table.
    """
    stat = PlayerStat(player_id=player_id, speed=speed, distance=distance, total_points=0)  # Ensure total_points starts at 0
    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat

def get_stats_by_player(db: Session, player_id: int):
    """
    Fetch all stats for a given player by their ID.
    """
    return db.query(PlayerStat).filter(PlayerStat.player_id == player_id).all()

def update_player_stat(db: Session, stat_id: int, speed: float = None, distance: float = None):
    """
    Update an existing stat record with new speed and/or distance.
    """
    stat = db.query(PlayerStat).filter(PlayerStat.id == stat_id).first()
    if not stat:
        return None

    if speed is not None:
        stat.speed = speed
    if distance is not None:
        stat.distance = distance

    db.commit()
    db.refresh(stat)
    return stat

def delete_player_stat(db: Session, stat_id: int):
    """
    Delete a specific stat record by ID.
    """
    stat = db.query(PlayerStat).filter(PlayerStat.id == stat_id).first()
    if not stat:
        return None

    db.delete(stat)
    db.commit()
    return stat

def update_player_points(db: Session, player_id: int, speed: float, distance: float, duration: int):
    """
    Update points for a player based on speed, distance, and duration.
    - Tier 1: 5–6.9 km/h = 1 point/min
    - Tier 2: 7–8.9 km/h = 2 points/min
    - Tier 3: 9 km/h and above = 3 points/min
    - Additional points for distance and consistency
    """
    points = 0

    # Calculate points based on speed
    if speed >= 9:
        points += 3 * duration  # High Speed Tier (3 points/min)
    elif speed >= 7:
        points += 2 * duration  # Optimal Speed Tier (2 points/min)
    elif speed >= 5:
        points += 1 * duration  # Baseline Speed Tier (1 point/min)

    # Add points for distance
    points += distance  # Add points for distance

    # Retrieve player stats from the database
    player_stat = db.query(PlayerStat).filter(PlayerStat.player_id == player_id).first()

    if player_stat:
        player_stat.total_points = player_stat.total_points + points if player_stat.total_points else points
        db.commit()
        db.refresh(player_stat)
    else:
        raise ValueError(f"Player with ID {player_id} not found.")

def leaderboard(db: Session, top_n: int = 10):
    """
    Retrieve the top N players based on total points.
    """
    return db.query(PlayerStat).order_by(PlayerStat.total_points.desc()).limit(top_n).all()

def check_consistency_bonus(db: Session, player_id: int):
    """
    Check if a player qualifies for a consistency bonus.
    """
    player_stats = db.query(PlayerStat).filter(PlayerStat.player_id == player_id).all()

    # Check for consistency over the last 7 days (as an example)
    consistent = True
    for stat in player_stats[-7:]:
        if stat.total_points < 10:  # Example: minimum points threshold
            consistent = False
            break

    if consistent:
        bonus = 100  # Example bonus for consistency
        return bonus
    else:
        return 0
