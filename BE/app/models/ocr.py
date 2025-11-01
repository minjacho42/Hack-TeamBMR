from typing import Dict

from pydantic import BaseModel


class OcrUploadResponse(BaseModel):
    uploadId: str
    status: str


class OcrObjectAccessRequest(BaseModel):
    uploadId: str
    ttlSec: int


class OcrObjectAccessResponse(BaseModel):
    url: str
    expiresAt: str


class OcrResultResponse(BaseModel):
    uploadId: str
    status: str
    text: str
    fields: Dict[str, str]
    confidence: float
