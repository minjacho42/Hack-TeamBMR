from typing import List, Optional

from pydantic import BaseModel


class ChecklistItem(BaseModel):
    id: str
    text: str
    checked: Optional[bool] = None
    note: Optional[str] = None


class ChecklistCategory(BaseModel):
    id: str
    label: str
    items: List[ChecklistItem]


class Checklist(BaseModel):
    checklistId: str
    title: str
    categories: List[ChecklistCategory]


class ChecklistListResponse(BaseModel):
    items: List[Checklist]


class ChecklistCheck(BaseModel):
    id: str
    checked: bool
    note: Optional[str] = None


class ChecklistChecksPayload(BaseModel):
    roomId: str
    items: List[ChecklistCheck]


class ChecklistCheckResponse(BaseModel):
    saved: bool
    count: int
