from typing import Optional

from fastapi import APIRouter, Query

from app.models import ChecklistListResponse, DEFAULT_CHECKLIST_TEMPLATE

router = APIRouter()


@router.get("/checklists", response_model=ChecklistListResponse)
async def list_checklists() -> ChecklistListResponse:
    return ChecklistListResponse(items=[DEFAULT_CHECKLIST_TEMPLATE])
