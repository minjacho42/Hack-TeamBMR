from typing import Union

from fastapi import APIRouter, Path, Query, status
from fastapi.responses import JSONResponse

from app.models import (
    LLMMatchItem,
    LLMReportListItem,
    LLMReportListResponse,
    LLMReportOptions,
    LLMReportProgress,
    LLMReportResult,
    LLMReportTriggerPayload,
    LLMReportTriggerResponse,
)

router = APIRouter()


@router.post(
    "/llm/reports",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=LLMReportTriggerResponse,
)
async def trigger_llm_report(payload: LLMReportTriggerPayload) -> LLMReportTriggerResponse:
    """Accept report generation requests."""
    return LLMReportTriggerResponse(reportId="rp_1", status="queued")


@router.get(
    "/llm/reports/{report_id}",
    response_model=Union[LLMReportResult, LLMReportProgress],
    responses={status.HTTP_202_ACCEPTED: {"model": LLMReportProgress}},
)
async def get_llm_report(
    report_id: str = Path(..., description="Report identifier"),
) -> Union[LLMReportResult, JSONResponse]:
    """Return a dummy report outcome."""
    if report_id.endswith("_processing"):
        progress = LLMReportProgress(
            reportId=report_id,
            status="processing",
            progress=0.6,
        )
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=progress.model_dump())

    base_item = LLMMatchItem(id="c1", text="위임장 원본 확인")
    return LLMReportResult(
        reportId=report_id,
        status="done",
        matched=[base_item],
        missing=[],
        conflict=[],
        summary="계약서 항목이 모두 충족되었습니다.",
    )


@router.get("/llm/reports", response_model=LLMReportListResponse)
async def list_llm_reports(
    sessionId: str = Query(..., description="Session identifier to filter reports"),
) -> LLMReportListResponse:
    """Return dummy report metadata."""
    return LLMReportListResponse(
        items=[
            LLMReportListItem(
                reportId="rp_1",
                status="done",
                createdAt="2025-01-01T00:00:00Z",
            )
        ]
    )
