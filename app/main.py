from fastapi import FastAPI
import logging

from app.database import Base, engine
from app.routers import books, auth

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Advisor API")

app.include_router(books.router)
app.include_router(auth.router)

@app.get("/")
def read_books():
    return {"message": "Book Advisor is running"}