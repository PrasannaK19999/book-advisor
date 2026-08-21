""" Generate embeddings for books in the database """

from sentence_transformers import SentenceTransformer
from app.database import SessionLocal
from app.models.book import Book

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_all_books():
    db = SessionLocal()
    try:
        books = db.query(Book).all()
        print(f"Found {len(books)} books to embed.")

        for book in books:
            text = f"{book.name}. Category: {book.category}. {book.description or ''}"
            vector = model.encode(text)
            book.embedding = vector

        db.commit()
        print(f"\nDone. All {len(books)} books embedded and saved.")
    finally:
        db.close()

if __name__ == "__main__":
    embed_all_books()