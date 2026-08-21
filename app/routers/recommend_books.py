from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer

from app.database import get_db
from app.models.book import Book
from app.schemas.book import BookResponse

router = APIRouter(prefix="/recommend", tags=["Recommend"])

model = SentenceTransformer("all-MiniLM-L6-v2")


@router.get("/", response_model=list[BookResponse])
def recommend_books(query: str, k: int = 3, db: Session = Depends(get_db)):
    # 1. Embed the user's question into a 384-vector
    query_vector = model.encode(query)

    # 2. pgvector similarity search: find the k closest book-vectors
    results = (
        db.query(Book)
        .filter(Book.embedding.isnot(None))
        .order_by(Book.embedding.cosine_distance(query_vector))
        .limit(k)
        .all()
    )

    # 3. Return the matching books
    return results