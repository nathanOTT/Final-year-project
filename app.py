# app.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import Base, engine, get_db
from database.models import PlayerStat  # Import PlayerStat model here
from crud.crud import update_player_points, leaderboard, check_consistency_bonus  # Correct import path for crud.py in the crud folder
from utils.data_loader import load_data_to_db
from utils.heatmap import generate_heatmap

# Initialize the FastAPI app
app = FastAPI()

# Initialize the database and create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Speed & Distance Challenge Backend"}

@app.post("/import/")
def import_data(db: Session = Depends(get_db)):
    """
    Endpoint to import the dataset into the database.
    """
    try:
        load_data_to_db(db)
        return {"message": "Dataset imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/heatmap/{player_id}")
def get_heatmap(player_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to generate a heatmap for a player's stats.
    """
    player_exists = db.query(PlayerStat).filter(PlayerStat.player_id == player_id).first()

    if not player_exists:
        raise HTTPException(status_code=404, detail=f"Player ID {player_id} not found in the dataset.")
    
    heatmap_path = generate_heatmap(player_id, db)
    
    if not heatmap_path:
        raise HTTPException(status_code=404, detail="No data found for this player")
    
    return {"message": "Heatmap generated", "path": heatmap_path}

@app.post("/update_points/{player_id}")
def update_points(player_id: int, speed: float, distance: float, duration: int, db: Session = Depends(get_db)):
    """
    Endpoint to update points for a player based on speed, distance, and duration.
    """
    try:
        update_player_points(db, player_id, speed, distance, duration)
        return {"message": f"Points updated successfully for player ID {player_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leaderboard/")
def get_leaderboard(top_n: int = 10, db: Session = Depends(get_db)):
    """
    Endpoint to get the leaderboard showing the top N players by total points.
    """
    top_players = leaderboard(db, top_n)
    return {"leaderboard": top_players}

@app.get("/check_consistency_bonus/{player_id}")
def get_consistency_bonus(player_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to check if a player qualifies for a consistency bonus.
    """
    bonus = check_consistency_bonus(db, player_id)
    return {"bonus": bonus}
