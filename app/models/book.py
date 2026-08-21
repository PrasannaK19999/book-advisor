from sqlalchemy import Column, Integer, String, Float, Text
from pgvector.sqlalchemy import Vector

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    embedding = Column(Vector(384), nullable=True)