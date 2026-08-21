from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
#from sqlalchemy import func
from sentence_transformers import SentenceTransformer

from app.database import get_db
from app.models.book import Book
from app.schemas.book import RecommendResponse
from app.services.llm import recommend_from_books

router = APIRouter(prefix="/recommend", tags=["Recommend"])

model = SentenceTransformer("all-MiniLM-L6-v2")

# Books with cosine distance less than this threshold are considered relevant
DISTANCE_THRESHOLD = 0.6


@router.get("/", response_model=RecommendResponse)
def recommend(query: str, k: int = 3, db: Session = Depends(get_db)):
    query_vector = model.encode(query)

    distance = Book.embedding.cosine_distance(query_vector)
    results = (
        db.query(Book, distance.label("distance"))
        .filter(Book.embedding.isnot(None))
        .order_by(distance)
        .limit(k)
        .all()
    )

    # TEMP debug — see the distances
    #for book, dist in results:
    #    print(f"  distance={dist:.3f}  {book.name}")
   
    relevant_books = [book for book, dist in results if dist < DISTANCE_THRESHOLD]

    # If nothing is relevant, return honestly — don't force noise
    if not relevant_books:
        return RecommendResponse(
            query=query,
            recommendation="No books in the catalog match your query closely enough. Try a different topic.",
            books=[],
        )

    recommendation = recommend_from_books(query, relevant_books)

    return RecommendResponse(
        query=query,
        recommendation=recommendation,
        books=relevant_books,
    )