from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String(255))
    price = Column(Float)
    img_url = Column(String(500))
    brand = Column(String(100))
    rating = Column(Float)
    platform = Column(String(50))
    trace_id = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    trace_id = Column(String(50))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now)