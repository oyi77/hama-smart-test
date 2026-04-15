from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    is_done = Column(Boolean, default=False)
    category = Column(String, default="General")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
