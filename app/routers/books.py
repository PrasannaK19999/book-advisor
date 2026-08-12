from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.schemas.book import BookRequest, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse)
def create_book(payload: BookRequest, db: Session = Depends(get_db)):
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.get("/", response_model=list[BookResponse])
def list_books(category: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Book)
    if category:
        query = query.filter(Book.category == category)
    return query.all()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book