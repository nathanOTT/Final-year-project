from sqlalchemy import Column, Integer, Float, String, DateTime
from database.config import Base
from datetime import datetime

class PlayerStat(Base):
    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, nullable=False)
    speed = Column(Float, nullable=False)
    distance = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
