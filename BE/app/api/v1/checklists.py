from typing import Optional

from fastapi import APIRouter, Path, Query, status

from app.models import (
    Checklist,
    ChecklistCategory,
    ChecklistCheckResponse,
    ChecklistChecksPayload,
    ChecklistItem,
    ChecklistListResponse,
)

router = APIRouter()


@router.get("/checklists", response_model=ChecklistListResponse)
async def list_checklists(
    locale: str = Query(..., description="Locale code, e.g. ko-KR"),
    category: Optional[str] = Query(None, description="Checklist category filter"),
) -> ChecklistListResponse:
    """Return a canned checklist template response."""
    dummy_category = ChecklistCategory(
        id="id_verif",
        label="신분/위임",
        items=[ChecklistItem(id="c1", text="위임장 원본 확인")],
    )

    return ChecklistListResponse(
        items=[
            Checklist(
                checklistId="cl_lease_v1",
                title="임대차 체크리스트",
                categories=[dummy_category],
            )
        ]
    )


@router.post(
    "/checklists/{checklist_id}/checks",
    status_code=status.HTTP_201_CREATED,
    response_model=ChecklistCheckResponse,
)
async def save_checklist_checks(
    payload: ChecklistChecksPayload,
    checklist_id: str = Path(..., description="Checklist identifier"),
) -> ChecklistCheckResponse:
    """Acknowledge checklist state persistence."""
    return ChecklistCheckResponse(saved=True, count=len(payload.items))
