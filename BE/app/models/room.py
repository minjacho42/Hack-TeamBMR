from typing import List, Optional

from pydantic import BaseModel, Field


class RoomBase(BaseModel):
    address: str
    type: str
    floor: int
    deposit: int = Field(..., ge=0)
    rent: int = Field(..., ge=0)
    maintenance: int = Field(..., ge=0)


class RoomCreatePayload(RoomBase):
    pass


class Room(RoomBase):
    roomId: str
    photos: Optional[int] = None


class RoomCreateResponse(BaseModel):
    roomId: str


class RoomPhoto(BaseModel):
    photoId: str
    url: Optional[str] = None
    thumbUrl: Optional[str] = None


class RoomListResponse(BaseModel):
    items: List[Room]


class RoomDetailResponse(RoomBase):
    roomId: str
    photos: List[RoomPhoto]


class PhotoUploadResponse(BaseModel):
    photoId: str
    objectUrl: str


class PhotoPresignRequest(BaseModel):
    contentType: str


class PhotoPresignResponse(BaseModel):
    uploadUrl: str
    photoId: str


class RoomPhotoAccessRequest(BaseModel):
    ttlSec: int


class PhotoAccessResponse(BaseModel):
    url: str
    expiresAt: str


class PhotoListResponse(BaseModel):
    items: List[RoomPhoto]
