from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from datetime import datetime
from database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    cadet_name = Column(String)
    session_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('cadet_name', 'session_id', name='unique_attendance'),
    )