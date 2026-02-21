from sqlalchemy import Column, String, Text, Boolean, func, Integer, DateTime, ForeignKey
from core.core.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship




class TaskModel(Base):
    __tablename__="tasks"


    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), name="fk_tasks_user_id_users")
    title = Column(String(150), nullable=False)
    description = Column(Text(500), nullable=True)
    is_completed = Column(Boolean, default=False)


    created_date = Column(DateTime, server_default=func.now())
    update_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    user = relationship("UserModel", back_populates="task", uselist=False)


