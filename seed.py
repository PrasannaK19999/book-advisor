import os
import time

import httpx
from dotenv import load_dotenv

from app.database import SessionLocal, Base, engine
from app.models.book import Book

load_dotenv()

API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"

# category label  ->  what we actually search Google Books for
CATEGORY_SEARCHES = {
    "IT": "software engineering",
    "Finance": "investing",
    "Design": "ux design",
}

BOOKS_PER_CATEGORY = 5


def fetch_books(search_term: str, max_results: int) -> list[dict]:
    """Call Google Books and return a list of clean book dicts."""
    params = {
        "q": search_term,
        "maxResults": max_results,
        "key": API_KEY,
        "langRestrict": "en",
    }
    response = httpx.get(BOOKS_URL, params=params, timeout=20.0)
    response.raise_for_status()
    items = response.json().get("items", [])

    books = []
    for item in items:
        info = item.get("volumeInfo", {})
        description = info.get("description")
        if not description:          # skip books without a description
            continue
        books.append({
            "name": info.get("title", "Unknown Title"),
            "price": 29.99,          # placeholder price
            "description": description,
        })
    return books


def seed():
    # make sure the table exists
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        total = 0
        for category, search_term in CATEGORY_SEARCHES.items():
            print(f"Fetching '{category}' books (search: '{search_term}')...")
            books = fetch_books(search_term, BOOKS_PER_CATEGORY)

            for b in books:
                book = Book(
                    name=b["name"],
                    category=category,
                    price=b["price"],
                    description=b["description"],
                )
                db.add(book)
                total += 1
                print(f"  + {b['name']}")

            db.commit()
            time.sleep(1)  # be polite to the API between categories

        print(f"\nDone. Seeded {total} books.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()