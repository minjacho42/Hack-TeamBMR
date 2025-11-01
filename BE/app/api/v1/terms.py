from fastapi import APIRouter, Query

from app.models import Term, TermListResponse

router = APIRouter()


@router.get("/terms", response_model=TermListResponse)
async def search_terms(
    keyword: str = Query(..., description="Term keyword to search"),
    locale: str = Query(..., description="Locale code, e.g. ko-KR"),
) -> TermListResponse:
    """Return a canned glossary response."""
    return TermListResponse(
        items=[
            Term(
                term="근저당",
                definition="채무자가 채무를 변제하지 않을 경우...",
                examples=["근저당권 설정 계약서"],
            )
        ]
    )
