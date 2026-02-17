from sqlalchemy import Column, String, Text, Boolean, func, Integer, DateTime
from core.core.database import Base
from datetime import datetime




class TaskModel(Base):
    __tablename__="tasks"


    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(Text(500), nullable=True)
    is_completed = Column(Boolean, default=False)


    created_date = Column(DateTime, server_default=func.now())
    update_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())