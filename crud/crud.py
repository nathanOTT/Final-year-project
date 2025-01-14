#Creating player stat
from sqlalchemy.orm import Session
from database.models import PlayerStat

def create_player_stat(db: Session, player_id: str, speed: float, distance: float):
    """
    Add a new record to the player stats table.
    """
    stat = PlayerStat(player_id=player_id, speed=speed, distance=distance)
    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat

#Reading player stat
def get_stats_by_player(db: Session, player_id: str):
    """
    Fetch all stats for a given player by their ID.
    """
    return db.query(PlayerStat).filter(PlayerStat.player_id == player_id).all()

#updating player stat
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

#Delting player stat
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
