from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from database.config import Base, engine, get_db
from database.models import PlayerStat
from utils.data_loader import load_data_to_db
from utils.heatmap import generate_heatmap

# Initialize the FastAPI app
app = FastAPI()

# Initialize the database and create tables
Base.metadata.create_all(bind=engine)

# CRUD Operations
def create_player_stat(db: Session, player_id: str, speed: float, distance: float):
    stat = PlayerStat(player_id=player_id, speed=speed, distance=distance)
    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat

def get_stats_by_player(db: Session, player_id: str):
    return db.query(PlayerStat).filter(PlayerStat.player_id == player_id).all()

def update_player_stat(db: Session, stat_id: int, speed: float = None, distance: float = None):
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
    try:
        stat = create_player_stat(db, player_id, speed, distance)
        return {"message": "Stat added successfully", "stat": stat}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Retrieve player stats
@app.get("/stats/{player_id}")
def get_stats(player_id: str, db: Session = Depends(get_db)):
    stats = get_stats_by_player(db, player_id)
    if not stats:
        raise HTTPException(status_code=404, detail="No stats found for this player")
    return {"player_id": player_id, "stats": stats}

# Update a player stat
@app.put("/stats/{stat_id}")
def update_stat(stat_id: int, speed: float = None, distance: float = None, db: Session = Depends(get_db)):
    stat = update_player_stat(db, stat_id, speed, distance)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    return {"message": "Stat updated successfully", "stat": stat}

# Delete a player stat
@app.delete("/stats/{stat_id}")
def delete_stat(stat_id: int, db: Session = Depends(get_db)):
    stat = delete_player_stat(db, stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    return {"message": "Stat deleted successfully"}

# Import a dataset
@app.post("/import/")
async def import_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Endpoint to import a dataset into the database.
    Args:
        file: Uploaded CSV file
        db: Database session
    Returns:
        JSON response confirming data import
    """
    try:
        file_path = f"datasets/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        load_data_to_db(file_path, db)
        return {"message": f"Dataset {file.filename} imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Generate heatmaps
@app.get("/heatmap/{player_id}")
def get_heatmap(player_id: str, db: Session = Depends(get_db)):
    heatmaps = generate_heatmap(player_id, db)
    if not heatmaps:
        raise HTTPException(status_code=404, detail="No stats found for this player")
    return {"message": "Heatmaps generated successfully", "heatmaps": heatmaps}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8002, reload=True)
