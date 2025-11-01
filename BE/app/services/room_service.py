from __future__ import annotations

from typing import List, Optional
from uuid import uuid4

from app.database.mongodb import get_rooms_collection, get_session
from app.models import RoomBase, RoomDetailResponse, RoomPhoto
from app.repositories import RoomRepository
from app.services.storage_service import StorageService, get_storage_service


class RoomService:
    """Business logic for room operations."""

    def __init__(self, repository: RoomRepository, storage: StorageService) -> None:
        self._repository = repository
        self._storage = storage

    async def create_room(self, payload: RoomBase) -> RoomDetailResponse:
        room = self._materialize_room(payload)
        async with get_session() as session:
            await self._repository.insert_room(room, session=session)
        return await self._to_response(room)

    async def list_rooms(self, page: int, size: int) -> List[RoomDetailResponse]:
        skip = (page - 1) * size
        rooms = await self._repository.list_rooms(skip=skip, limit=size)
        responses: List[RoomDetailResponse] = []
        for room in rooms:
            responses.append(await self._to_response(room))
        return responses

    async def get_room(self, room_id: str) -> Optional[RoomDetailResponse]:
        room = await self._repository.get_room(room_id)
        if not room:
            return None
        return await self._to_response(room)

    async def delete_room(self, room_id: str) -> bool:
        async with get_session() as session:
            return await self._repository.delete_room(room_id, session=session)

    async def attach_photo(
        self,
        room_id: str,
        filename: str,
        content: bytes,
        content_type: Optional[str],
    ) -> Optional[RoomPhoto]:
        room = await self._repository.get_room(room_id)
        if not room:
            return None

        photo_id = f"ph_{uuid4().hex[:12]}"
        object_key = f"rooms/{room_id}/{photo_id}/{filename}"

        await self._storage.upload_bytes(
            object_key,
            content,
            content_type=content_type or "application/octet-stream",
        )

        async with get_session() as session:
            updated = await self._repository.update_photo(
                room_id,
                photo_id,
                object_key,
                session=session,
            )

        if not updated:
            # Roll back uploaded object when DB update fails.
            await self._storage.delete_object(object_key)
            return None

        url = await self._storage.generate_presigned_url(object_key)
        return RoomPhoto(photo_id=photo_id, object_url=url)

    def _materialize_room(self, payload: RoomBase) -> RoomBase:
        room_id = payload.room_id or f"rm_{uuid4().hex[:10]}"
        data = payload.model_dump(exclude={"room_id"}, deep=True)
        return RoomBase(**data, room_id=room_id)

    async def _to_response(
        self,
        room: RoomBase,
    ) -> RoomDetailResponse:
        photo = await self._build_photo(room)

        return RoomDetailResponse(
            room_id=room.room_id or "",
            address=room.address,
            type=room.type,
            floor=room.floor,
            deposit=room.deposit,
            rent_monthly=room.rent_monthly,
            fee_included=room.fee_included,
            fee_mgmt=room.fee_mgmt,
            report_id=room.report_id,
            checklist=room.checklist,
            photo=photo,
        )

    async def _build_photo(self, room: RoomBase) -> Optional[RoomPhoto]:
        if room.photo_id and room.photo_key:
            url = await self._storage.generate_presigned_url(room.photo_key)
            return RoomPhoto(
                photo_id=room.photo_id,
                object_url=url,
            )
        return None


def get_room_service() -> RoomService:
    repository = RoomRepository(get_rooms_collection())
    storage = get_storage_service()
    return RoomService(repository, storage)
