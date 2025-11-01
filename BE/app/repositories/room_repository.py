from __future__ import annotations

from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorCollection

from app.models import RoomBase, RoomChecklist


class RoomRepository:
    """Persistence layer for room records."""

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self._collection = collection

    async def insert_room(
        self,
        room: RoomBase,
        *,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> None:
        document = room.model_dump(exclude_none=True)
        document["_id"] = document["room_id"]
        await self._collection.insert_one(document, session=session)

    async def get_room(self, room_id: str) -> Optional[RoomBase]:
        document = await self._collection.find_one({"_id": room_id})
        return self._deserialize(document)

    async def list_rooms(self, skip: int, limit: int) -> List[RoomBase]:
        cursor = (
            self._collection.find()
            .skip(skip)
            .limit(limit)
            .sort("room_id", 1)
        )
        documents = await cursor.to_list(length=limit)
        return [room for doc in documents if (room := self._deserialize(doc))]

    async def delete_room(
        self,
        room_id: str,
        *,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> bool:
        result = await self._collection.delete_one({"_id": room_id}, session=session)
        return result.deleted_count == 1

    async def update_photo(
        self,
        room_id: str,
        photo_id: str,
        object_key: str,
        *,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> bool:
        result = await self._collection.update_one(
            {"_id": room_id},
            {
                "$set": {
                    "photo_id": photo_id,
                    "photo_key": object_key,
                }
            },
            session=session,
        )
        return result.modified_count == 1

    def _deserialize(self, document: Optional[dict]) -> Optional[RoomBase]:
        if not document:
            return None

        data = dict(document)
        data.setdefault("room_id", data.pop("_id", None))
        data.setdefault("photo_id", data.get("photo_id"))
        if "photo_key" not in data:
            data["photo_key"] = None

        # Ensure nested checklist structure always materialises as expected by RoomBase.
        if "checklist" not in data or not data["checklist"]:
            data["checklist"] = RoomChecklist()

        return RoomBase.model_validate(data)
