from typing import List

from pydantic import BaseModel


class Term(BaseModel):
    term: str
    definition: str
    examples: List[str]


class TermListResponse(BaseModel):
    items: List[Term]
