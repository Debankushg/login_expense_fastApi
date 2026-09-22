from app.core.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime,Float
from sqlalchemy.orm import relationship
from datetime import datetime


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True, auto_increment=True)
    title= Column(String(50), index=True ,nullable=False)
    description = Column(String, index=True ,nullable=True)
    show = Column(Boolean, default=True)
    amount = Column(Float, index=True ,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow ,nullable=False)