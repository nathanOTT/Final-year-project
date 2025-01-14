from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import Base, engine, get_db
from database.models import PlayerStat

# Initialize the FastAPI app
app = FastAPI()

# Initialize the database and create tables
Base.metadata.create_all(bind=engine)

# CRUD Operations
def create_player_stat(db: Session, player_id: str, speed: float, distance: float):
    """
    Add a new record to the player stats table.
    """
    stat = PlayerStat(player_id=player_id, speed=speed, distance=distance)
    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat

def get_stats_by_player(db: Session, player_id: str):
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

# API Endpoints

@app.get("/")
def read_root():
    return {"message": "Welcome to the Speed & Distance Challenge Backend"}

# Add a player stat
@app.post("/stats/")
def add_stat(player_id: str, speed: float, distance: float, db: Session = Depends(get_db)):
    """
    Endpoint to add player statistics to the database.
    Args:
        player_id: ID of the player
        speed: Speed of the player in km/h
        distance: Distance covered by the player in km
        db: Database session
    Returns:
        JSON response with the added statistics
    """
    try:
        stat = create_player_stat(db, player_id, speed, distance)
        return {"message": "Stat added successfully", "stat": stat}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Retrieve player stats
@app.get("/stats/{player_id}")
def get_stats(player_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to fetch all statistics for a specific player.
    Args:
        player_id: ID of the player
        db: Database session
    Returns:
        JSON response with the player's statistics
    """
    stats = get_stats_by_player(db, player_id)
    if not stats:
        raise HTTPException(status_code=404, detail="No stats found for this player")
    return {"player_id": player_id, "stats": stats}

# Update a player stat
@app.put("/stats/{stat_id}")
def update_stat(stat_id: int, speed: float = None, distance: float = None, db: Session = Depends(get_db)):
    """
    Endpoint to update a specific player statistic.
    Args:
        stat_id: ID of the statistic record
        speed: New speed value (optional)
        distance: New distance value (optional)
        db: Database session
    Returns:
        JSON response with the updated statistics
    """
    stat = update_player_stat(db, stat_id, speed, distance)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    return {"message": "Stat updated successfully", "stat": stat}

# Delete a player stat
@app.delete("/stats/{stat_id}")
def delete_stat(stat_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a specific player statistic.
    Args:
        stat_id: ID of the statistic record
        db: Database session
    Returns:
        JSON response confirming deletion
    """
    stat = delete_player_stat(db, stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    return {"message": "Stat deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8002, reload=True)
