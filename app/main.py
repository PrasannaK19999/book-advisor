from fastapi import FastAPI, Depends, HTTPException

from app.database import Base, engine
from app.models.book import Book

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Advisor API")

@app.get("/books")
def read_books():
    return {"message": "Book Advisor is running"}