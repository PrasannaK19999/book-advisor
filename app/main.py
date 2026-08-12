from fastapi import FastAPI

from app.database import Base, engine
from app.models.book import Book
from app.routers import books

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Advisor API")

app.include_router(books.router)

@app.get("/")
def read_books():
    return {"message": "Book Advisor is running"}