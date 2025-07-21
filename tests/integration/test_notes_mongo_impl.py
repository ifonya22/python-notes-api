import time

import pytest

from app.database.repositories.base import NoteRepository


@pytest.mark.asyncio
async def test_create(note_repo: NoteRepository):
    test_data = {
        "title": "Test Note",
        "body": "This is a test note body",
        "user_id": 123,
    }

    result = await note_repo.create(test_data)

    assert "_id" in result
    assert result["title"] == test_data["title"]
    assert result["body"] == test_data["body"]
    assert result["user_id"] == test_data["user_id"]
    assert result["is_deleted"] is False
    assert "created_at" in result
    assert "updated_at" in result


@pytest.mark.asyncio
async def test_soft_delete(note_repo: NoteRepository):
    test_data = {"title": "Note to delete", "body": "Body", "user_id": 1}
    result = await note_repo.create(test_data)
    note_id = result["_id"]

    deleted = await note_repo.soft_delete(note_id, 1)
    assert deleted is True

    note = await note_repo.collection.find_one({"_id": note_id})
    assert note["is_deleted"] is True
    assert note["updated_at"] > note["created_at"]


@pytest.mark.asyncio
async def test_restore(note_repo: NoteRepository):
    result = await note_repo.collection.insert_one(
        {"title": "Note to restore", "body": "Body", "user_id": 1, "is_deleted": True}
    )
    note_id = result.inserted_id

    restored = await note_repo.restore(note_id)
    assert restored is True

    note = await note_repo.collection.find_one({"_id": note_id})
    assert note["is_deleted"] is False


@pytest.mark.asyncio
async def test_get_by_note_id(note_repo: NoteRepository):
    result = await note_repo.collection.insert_one({"title": "Test Note", "body": "Body", "user_id": 1})
    note_id = result.inserted_id

    note = await note_repo.get_by_note_id(note_id)
    assert note["_id"] == note_id
    assert note["title"] == "Test Note"

    note_with_user = await note_repo.get_by_note_id_and_user_id(note_id, 1)
    assert note_with_user["_id"] == note_id
    assert note_with_user["user_id"] == 1

    assert await note_repo.get_by_note_id_and_user_id(note_id, 999) is None


@pytest.mark.asyncio
async def test_get_all(note_repo: NoteRepository):
    await note_repo.collection.insert_many(
        [
            {"title": "Note 1", "body": "Body 1", "user_id": 1},
            {"title": "Note 2", "body": "Body 2", "user_id": 1},
            {"title": "Note 3", "body": "Body 3", "user_id": 2},
        ]
    )

    all_notes = await note_repo.get_all()
    assert len(all_notes) == 3

    user_notes = await note_repo.get_all_by_user_id(1)
    assert len(user_notes) == 2
    assert all(note["user_id"] == 1 for note in user_notes)


@pytest.mark.asyncio
async def test_update(note_repo: NoteRepository):
    test_data = {
        "title": "Old Title",
        "body": "Old Body",
        "user_id": 1,
    }
    result = await note_repo.create(test_data)
    note_id = result["_id"]

    update_data = {"title": "New Title", "body": "New Body"}
    time.sleep(0.5)
    updated_note = await note_repo.update(note_id, 1, update_data)

    assert updated_note["_id"] == note_id
    assert updated_note["title"] == "New Title"
    assert updated_note["body"] == "New Body"
