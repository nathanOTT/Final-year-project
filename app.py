from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import Base, engine, get_db
from database.models import PlayerStat
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
    heatmap_path = generate_heatmap(player_id, db)
    if not heatmap_path:
        raise HTTPException(status_code=404, detail="No data found for this player")
    return {"message": "Heatmap generated", "path": heatmap_path}
