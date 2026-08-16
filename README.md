# # Book Advisor — AI Career Guidance from Real Books # # 

An AI-powered book and course advisor backend. Users browse a catalog of real books by category, and an LLM analyzes each book's description to surface the concrete skills a reader will gain and the career paths those skills open.

Built with FastAPI, PostgreSQL, and Groq's LLM API — fully containerized with Docker.

What it does
Browse a real catalog of books, organized by category (IT, Finance, Design), seeded from the Google Books API.
Enquire about any book — a single authenticated endpoint sends the book's stored description to an LLM, which returns structured skills and careers as JSON.
Secure access — registration and login with JWT authentication and bcrypt-hashed passwords. The AI endpoint is protected; only logged-in users can use it.

Grounded analysis, by design. The LLM analyzes only the book description provided to it — it extracts skills and careers from real stored text rather than recalling or guessing from memory. This keeps outputs factual and defensible.
A future update will integrate a RAG pipeline and an agentic system to deepen this grounding — retrieving richer source material so the analysis becomes more thorough while remaining fact-based.

Tech stack
Layer	Technology
API framework	FastAPI
Database	PostgreSQL
ORM	SQLAlchemy
Validation	Pydantic
Auth	JWT (python-jose) + bcrypt (passlib)
External calls	httpx (Google Books), Groq SDK (LLM)
Containerization	Docker + docker-compose
Architecture

The project follows a clean separation of concerns:

#app/ main.py       
App entry point — wires routers together 
#database.py        
DB connection and session management
#security.py        
Password hashing, JWT creation/verification, auth dependency
# models/            SQLAlchemy models (database tables)
  book.py
  user.py
# schemas/          Pydantic schemas (API request/response shapes)
  book.py
  user.py
# routers/          Endpoints grouped by feature
  books.py
  auth.py
# services/
  llm.py           
# seed.py            
Populates the catalog from the Google Books API

Models vs. schemas are kept separate on purpose: models describe how data lives in the database, schemas describe what crosses the API boundary. For example, the DB owns each book's id, 
so it appears in responses but is never accepted in requests.

Example enquire response :

Json
{
  "book_id": 1,
  "name": "Software Engineering",
  "skills": ["Software Development", "Project Management", "Quality Assurance"],
  "careers": ["Software Engineer", "IT Project Manager", "Quality Assurance Engineer"]
}

Exploring Further  :
  * Semantic search over the catalog (embeddings + pgvector).
  * Retrieval-augmented Q&A — ask free-form questions about any book.
  * Personalized recommendations based on a user's stated career goal.
  * Enquiry history and result caching to reduce repeat LLM calls.
