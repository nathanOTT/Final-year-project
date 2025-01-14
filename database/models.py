from sqlalchemy import Column, Integer, Float, String, DateTime
from database.config import Base

class PlayerStat(Base):
    """
    Database model for player statistics.
    """
    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, index=True)  # Changed to Integer
    speed = Column(Float)
    distance = Column(Float)
    timestamp = Column(DateTime)
