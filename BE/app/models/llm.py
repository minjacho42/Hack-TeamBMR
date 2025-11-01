from typing import List, Optional

from pydantic import BaseModel


class LLMReportOptions(BaseModel):
    lang: str


class LLMReportTriggerPayload(BaseModel):
    sttId: str
    ocrId: str
    options: Optional[LLMReportOptions] = None


class LLMReportTriggerResponse(BaseModel):
    reportId: str
    status: str


class LLMMatchItem(BaseModel):
    id: str
    text: str


class LLMReportResult(BaseModel):
    reportId: str
    status: str
    matched: List[LLMMatchItem]
    missing: List[LLMMatchItem]
    conflict: List[LLMMatchItem]
    summary: str


class LLMReportProgress(BaseModel):
    reportId: str
    status: str
    progress: float


class LLMReportListItem(BaseModel):
    reportId: str
    status: str
    createdAt: str


class LLMReportListResponse(BaseModel):
    items: List[LLMReportListItem]
