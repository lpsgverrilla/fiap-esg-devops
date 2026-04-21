"""Generic CRUD router factory shared across all 5 collections."""

from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.db.mongo import get_db
from src.schemas import serialize


def _oid(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except InvalidId as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Invalid id: {id_str}") from e


def build_router(
    *,
    prefix: str,
    tag: str,
    collection_name: str,
    schema_in: type[BaseModel],
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[tag])

    @router.get("")
    async def list_all(limit: int = 100) -> list[dict[str, Any]]:
        cursor = get_db()[collection_name].find().limit(limit)
        return [serialize(d) async for d in cursor]

    @router.get("/{doc_id}")
    async def get_one(doc_id: str) -> dict[str, Any]:
        doc = await get_db()[collection_name].find_one({"_id": _oid(doc_id)})
        if doc is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
        return serialize(doc)

    @router.post("", status_code=status.HTTP_201_CREATED)
    async def create(payload: schema_in) -> dict[str, Any]:
        data = payload.model_dump(by_alias=False)
        result = await get_db()[collection_name].insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data

    @router.put("/{doc_id}")
    async def update(doc_id: str, payload: schema_in) -> dict[str, Any]:
        data = payload.model_dump(by_alias=False)
        result = await get_db()[collection_name].update_one({"_id": _oid(doc_id)}, {"$set": data})
        if result.matched_count == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
        doc = await get_db()[collection_name].find_one({"_id": _oid(doc_id)})
        return serialize(doc)

    @router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(doc_id: str) -> None:
        result = await get_db()[collection_name].delete_one({"_id": _oid(doc_id)})
        if result.deleted_count == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")

    @router.get("/stats/count")
    async def count() -> dict[str, int]:
        n = await get_db()[collection_name].count_documents({})
        return {"count": n}

    return router
