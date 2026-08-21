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
    "IT & Software": "software engineering",
    "Finance": "personal finance investing",
    "Sales": "sales techniques",
    "Game Development": "game development programming",
    "Healthcare": "medicine healthcare",
    "Marketing": "digital marketing",
    "Data & AI": "data science machine learning",
    "Law": "business law",
    "Psychology": "psychology human behavior",
    "Entrepreneurship": "startup entrepreneurship",
    "Design": "ux design",
}

BOOKS_PER_CATEGORY = 10


def fetch_books(search_term: str, max_results: int) -> list[dict]:
    """Call Google Books and return a list of clean book dicts."""
    params = {
        "q": search_term,
        "maxResults": max_results,
        "key": API_KEY,
        "langRestrict": "en",
        "printType": "books",          # filter out magazines/junk
    }
    response = httpx.get(BOOKS_URL, params=params, timeout=20.0)
    response.raise_for_status()
    items = response.json().get("items", [])

    books = []
    for item in items:
        info = item.get("volumeInfo", {})
        description = info.get("description")
        title = info.get("title")
        if not description or not title:   # skip books missing either
            continue
        books.append({
            "name": title,
            "price": 29.99,
            "description": description,
        })
    return books


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Clear existing books so re-runs give a clean catalog (no duplicate pile-up)
        db.query(Book).delete()
        db.commit()

        seen_titles = set()   # global dedup across all categories
        total = 0

        for category, search_term in CATEGORY_SEARCHES.items():
            print(f"Fetching '{category}' (search: '{search_term}')...")
            books = fetch_books(search_term, BOOKS_PER_CATEGORY)

            added_here = 0
            for b in books:
                key = b["name"].strip().lower()
                if key in seen_titles:     # skip duplicate titles
                    continue
                seen_titles.add(key)

                db.add(Book(
                    name=b["name"],
                    category=category,
                    price=b["price"],
                    description=b["description"],
                ))
                added_here += 1
                total += 1

            db.commit()
            print(f"  added {added_here} unique books")
            time.sleep(1)

        print(f"\nDone. Seeded {total} unique books across {len(CATEGORY_SEARCHES)} categories.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()