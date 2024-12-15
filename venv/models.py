from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    description: str
    publicationyear: int
    price: int

    '''class Config:
        schema_extra = {
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author": "Douglas Adams",
                "description": "A humorous science fiction novel.",
                "published_year": 1979
            }
        }'''