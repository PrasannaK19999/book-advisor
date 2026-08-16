from fastapi import FastAPI

from app.database import Base, engine
from app.routers import books, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Advisor API")

app.include_router(books.router)
app.include_router(auth.router)

@app.get("/")
def read_books():
    return {"message": "Book Advisor is running"}