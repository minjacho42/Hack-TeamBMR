from typing import Optional

from fastapi import APIRouter, File, Query, UploadFile, status

from app.models import (
    OcrObjectAccessRequest,
    OcrObjectAccessResponse,
    OcrResultResponse,
    OcrUploadResponse,
)

router = APIRouter(prefix="/ocr")


@router.post(
    "/uploads",
    status_code=status.HTTP_201_CREATED,
    response_model=OcrUploadResponse,
)
async def upload_ocr_document(
    file: UploadFile = File(...),
    docType: Optional[str] = Query(None, description="Document type hint, e.g. lease"),
    id: Optional[str] = Query(None, description="Optional client-provided identifier"),
) -> OcrUploadResponse:
    """Accept an OCR source document upload."""
    _ = (docType, id, file.filename)  # placeholders for future persistence logic
    return OcrUploadResponse(uploadId="up_abc", status="queued")


@router.post("/objects/access", response_model=OcrObjectAccessResponse)
async def generate_ocr_object_access(
    payload: OcrObjectAccessRequest,
) -> OcrObjectAccessResponse:
    """Return a signed URL for accessing an uploaded OCR source."""
    return OcrObjectAccessResponse(
        url="https://signed-url",
        expiresAt="2025-10-31T13:40:00Z",
    )


@router.get("/results/{upload_id}", response_model=OcrResultResponse)
async def get_ocr_result(upload_id: str) -> OcrResultResponse:
    """Return a canned OCR extraction result."""
    return OcrResultResponse(
        uploadId=upload_id,
        status="done",
        text="... 추출된 전문 ...",
        fields={"보증금": "500만원", "월세": "45만원"},
        confidence=0.93,
    )
