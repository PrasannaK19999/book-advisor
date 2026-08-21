import json
import logging
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "openai/gpt-oss-120b"


def analyze_book(name: str, description: str) -> dict:
    """Ask the LLM to extract skills and career paths from a book's description."""
    prompt = (
        f"Based on the following book, identify what a reader will gain.\n\n"
        f"Book: {name}\n"
        f"Description: {description}\n\n"
        f"Respond ONLY with valid JSON in exactly this format, no extra text:\n"
        f'{{"skills": ["skill1", "skill2", "skill3"], '
        f'"careers": ["career1", "career2", "career3"]}}'
    )

    try:
        response = client.chat.completions.create(
            model= GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            timeout=30.0,
        )
    except Exception as exc:
        logger.error("LLM API call failed: %s", exc)
        raise RuntimeError("AI service is temporarily unavailable") from exc

    raw = response.choices[0].message.content

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("LLM returned invalid JSON: %s", raw)
        raise RuntimeError("AI returned an unexpected response") from exc

    if "skills" not in data or "careers" not in data:
        logger.error("LLM response missing expected keys: %s", data)
        raise RuntimeError("AI response was incomplete")

    return data


def recommend_from_books(query: str, books: list) -> str:
    """Ask the LLM to write a grounded recommendation from retrieved books ONLY."""
    # Build the catalog context from the retrieved books
    book_context = "\n\n".join(
        f"Title: {b.name}\nCategory: {b.category}\nDescription: {b.description or 'N/A'}"
        for b in books
    )

    prompt = (
        f"A user asked: \"{query}\"\n\n"
        f"Here are the ONLY books you may recommend from:\n\n"
        f"{book_context}\n\n"
        f"Write a helpful recommendation (2-4 sentences) explaining which of these "
        f"books best fit the user's goal and why. Recommend ONLY from the books above. "
        f"Do NOT invent or mention any book not listed. If none fit, say so honestly."
    )

    try:
        response = client.chat.completions.create(
            model= GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            timeout=30.0,
        )
    except Exception as exc:
        logger.error("LLM recommendation call failed: %s", exc)
        raise RuntimeError("AI service is temporarily unavailable") from exc

    return response.choices[0].message.content