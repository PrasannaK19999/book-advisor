from pydantic import BaseModel, Field

class BookRequest(BaseModel):     # incoming — what the API accepts
    name: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    description: str | None = Field(default=None, max_length=2000)


class BookResponse(BaseModel):    # outgoing — what the API returns
    id: int
    name: str
    category: str
    price: float
    description: str | None = None

    model_config = {"from_attributes": True}

class EnquiryResponse(BaseModel):
    book_id: int
    name: str
    skills: list[str]
    careers: list[str]

class RecommendResponse(BaseModel):
    query: str
    recommendation: str
    books: list[BookResponse]

    model_config = {"from_attributes": True}