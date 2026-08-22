# AI-Powered Book Advisor # 

This is a book recommendation API for people figuring out what to learn for their careers. Describe what you're aiming for, and it finds relevant books from the catalog using semantic search. Pick any book and it'll also break down the skills you'll pick up and the kind of jobs it can lead to.

## Features
- Semantic search over the catalog (embeddings + pgvector)
- Career-goal recommendations, grounded in real books
- Skill & career analysis for any book
- Honest out-of-domain handling — returns nothing when no book fits
- JWT-secured, Dockerized

## How It Works
Book descriptions are embedded into vectors (all-MiniLM-L6-v2) and stored in Postgres via pgvector. A query is embedded the same way, and cosine similarity finds the closest books. A tuned distance threshold filters out weak matches, so irrelevant queries return nothing instead of noise. The retrieved books are passed to an LLM (Groq) that writes a recommendation grounded strictly in that real data — no invented titles.

The skill/career analysis works the same way: the LLM only reads a book's stored description and extracts skills and career paths from it, rather than guessing from memory.

## Tech Stack
Python · FastAPI · PostgreSQL + pgvector · SQLAlchemy · Groq (LLM) · sentence-transformers · Docker · JWT

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/recommend` | Semantic book recommendations for a career goal |
| `GET`  | `/books` | List books (optional category filter) |
| `POST` | `/books/{id}/enquire` | AI skill & career analysis for a book (auth required) |
| `POST` | `/auth/register`, `/auth/login` | User auth (JWT) |

## Running Locally

Requires Docker and a `.env` file with `GROQ_API_KEY`, `GOOGLE_BOOKS_API_KEY`, and `JWT_SECRET_KEY`.

```bash
# Start the app + database
docker compose up -d --build

# Seed the catalog from Google Books
python seed.py

# Generate embeddings for the catalog
python embed_books.py
```
API docs available at `http://localhost:8000/docs`.
