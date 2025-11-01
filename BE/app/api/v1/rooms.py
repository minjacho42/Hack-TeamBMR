from fastapi import APIRouter, File, Path, Query, UploadFile, status

from app.models import (
    PhotoAccessResponse,
    PhotoListResponse,
    PhotoPresignRequest,
    PhotoPresignResponse,
    PhotoUploadResponse,
    Room,
    RoomCreatePayload,
    RoomCreateResponse,
    RoomDetailResponse,
    RoomPhoto,
    RoomPhotoAccessRequest,
    RoomListResponse,
)

router = APIRouter()


@router.post(
    "/rooms",
    status_code=status.HTTP_201_CREATED,
    response_model=RoomCreateResponse,
)
async def create_room(payload: RoomCreatePayload) -> RoomCreateResponse:
    """Create a room placeholder."""
    return RoomCreateResponse(roomId="rm_123")


@router.get("/rooms", response_model=RoomListResponse)
async def list_rooms(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> RoomListResponse:
    """Return a static room collection."""
    return RoomListResponse(
        items=[
            Room(
                roomId="rm_123",
                address="서울시 마포구...",
                type="원룸",
                floor=5,
                deposit=500,
                rent=45,
                maintenance=5,
                photos=3,
            )
        ]
    )


@router.get("/rooms/{room_id}", response_model=RoomDetailResponse)
async def get_room(room_id: str = Path(..., description="Unique room id")) -> RoomDetailResponse:
    """Return sample room detail."""
    photos = [
        RoomPhoto(
            photoId="ph_1",
            url="https://example.com/photos/ph_1.jpg",
            thumbUrl="https://example.com/photos/ph_1_thumb.jpg",
        )
    ]
    return RoomDetailResponse(
        roomId=room_id,
        address="서울시 마포구...",
        type="원룸",
        floor=5,
        deposit=500,
        rent=45,
        maintenance=5,
        photos=photos,
    )


@router.delete(
    "/rooms/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_room(room_id: str = Path(..., description="Unique room id")) -> None:
    """Acknowledge room deletion."""
    return None


@router.post(
    "/rooms/{room_id}/photos",
    status_code=status.HTTP_201_CREATED,
    response_model=PhotoUploadResponse,
)
async def upload_room_photo(
    room_id: str = Path(..., description="Unique room id"),
    file: UploadFile = File(...),
) -> PhotoUploadResponse:
    """Accept photo uploads and echo metadata."""
    return PhotoUploadResponse(
        photoId="ph_1",
        objectUrl=f"https://example.com/uploads/{file.filename or 'photo.jpg'}",
    )


@router.post(
    "/rooms/{room_id}/photos/presign",
    response_model=PhotoPresignResponse,
)
async def presign_room_photo(
    payload: PhotoPresignRequest,
    room_id: str = Path(..., description="Unique room id"),
) -> PhotoPresignResponse:
    """Return a dummy pre-signed URL."""
    return PhotoPresignResponse(
        uploadUrl="https://signed-upload-url",
        photoId="ph_1",
    )


@router.post(
    "/rooms/{room_id}/photos/{photo_id}/access",
    response_model=PhotoAccessResponse,
)
async def access_room_photo(
    payload: RoomPhotoAccessRequest,
    room_id: str = Path(..., description="Unique room id"),
    photo_id: str = Path(..., description="Photo identifier"),
) -> PhotoAccessResponse:
    """Return a dummy access URL."""
    return PhotoAccessResponse(
        url="https://signed-url",
        expiresAt="2025-11-01T12:00:00Z",
    )


@router.get(
    "/rooms/{room_id}/photos",
    response_model=PhotoListResponse,
)
async def list_room_photos(
    room_id: str = Path(..., description="Unique room id"),
) -> PhotoListResponse:
    """Return a static photo list."""
    return PhotoListResponse(
        items=[RoomPhoto(photoId="ph_1", thumbUrl="https://.../thumb.jpg")],
    )


@router.delete(
    "/rooms/{room_id}/photos/{photo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_room_photo(
    room_id: str = Path(..., description="Unique room id"),
    photo_id: str = Path(..., description="Photo identifier"),
) -> None:
    """Acknowledge photo deletion."""
    return None
