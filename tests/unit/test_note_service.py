from unittest.mock import AsyncMock

import pytest
from bson import ObjectId
from fastapi import HTTPException

from app.api.v1.notes.schemas import (
    CreateNoteRequestV1,
    NoteResponseAdminV1,
    NoteResponseV1,
    UpdateNoteRequestV1,
)
from app.database.repositories.base import NoteRepository
from app.services.notes.notes import NoteService
from app.utils.fields import PyObjectId


@pytest.mark.asyncio
async def test_create_note():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id = PyObjectId("687c1f81149d65b662bab130")
    mock_repo.create = AsyncMock(
        return_value={
            "_id": note_id,
            "title": "Test Note",
            "body": "Test Body",
            "user_id": 1,
            "is_deleted": False,
        }
    )

    service = NoteService(mock_repo)

    note_data = CreateNoteRequestV1(title="Test Note", body="Test Body")
    user_id = 1

    result = await service.create_note(note_data, user_id)

    assert isinstance(result, NoteResponseV1)

    assert result.title == "Test Note"
    assert result.body == "Test Body"
    assert str(result.note_id) == note_id


@pytest.mark.asyncio
async def test_get_note_by_note_id_and_user_id_success():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id_str = "687c1f81149d65b662bab130"
    mock_repo.get_by_note_id_and_user_id = AsyncMock(
        return_value={
            "_id": note_id_str,
            "title": "Test Note",
            "body": "Test Body",
            "user_id": 1,
            "is_deleted": False,
        }
    )

    service = NoteService(mock_repo)

    note_id = PyObjectId(note_id_str)
    user_id = 1

    result = await service.get_note_by_note_id_and_user_id(note_id_str, user_id)

    assert isinstance(result, NoteResponseV1)
    assert result.title == "Test Note"
    assert result.body == "Test Body"

    assert isinstance(result.note_id, ObjectId)

    assert str(result.note_id) == note_id
    mock_repo.get_by_note_id_and_user_id.assert_awaited_once_with(note_id_str, user_id)


@pytest.mark.asyncio
async def test_get_note_by_note_id_and_user_id_not_found():
    mock_repo = AsyncMock(spec=NoteRepository)
    mock_repo.get_by_note_id_and_user_id = AsyncMock(return_value=None)
    service = NoteService(mock_repo)

    note_id = PyObjectId("note_123")
    user_id = 1

    with pytest.raises(HTTPException) as exc_info:
        await service.get_note_by_note_id_and_user_id(note_id, user_id)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Note was not founded!"


@pytest.mark.asyncio
async def test_get_note_by_note_id_and_user_id_deleted():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id_str = "687c1f81149d65b662bab130"
    mock_repo.get_by_note_id_and_user_id = AsyncMock(
        return_value={
            "_id": note_id_str,
            "title": "Test Note",
            "body": "Test Body",
            "user_id": 1,
            "is_deleted": True,
        }
    )
    service = NoteService(mock_repo)

    note_id = PyObjectId(note_id_str)
    user_id = 1

    with pytest.raises(HTTPException) as exc_info:
        await service.get_note_by_note_id_and_user_id(note_id, user_id)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == f"Note {note_id_str} was deleted!"


@pytest.mark.asyncio
async def test_get_note_by_note_id_success():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id_str = "687c1f81149d65b662bab130"
    mock_repo.get_by_note_id = AsyncMock(
        return_value={
            "_id": note_id_str,
            "title": "Test Note",
            "body": "Test Body",
            "user_id": 1,
            "is_deleted": False,
        }
    )
    service = NoteService(mock_repo)

    note_id = PyObjectId(note_id_str)

    result = await service.get_note_by_note_id(note_id)

    assert isinstance(result, NoteResponseAdminV1)
    assert result.title == "Test Note"
    assert result.body == "Test Body"
    assert result.user_id == 1
    mock_repo.get_by_note_id.assert_awaited_once_with(note_id)


@pytest.mark.asyncio
async def test_get_note_by_note_id_not_found():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id_str = "687c1f81149d65b662bab130"
    mock_repo.get_by_note_id = AsyncMock(return_value=None)
    service = NoteService(mock_repo)

    note_id = PyObjectId(note_id_str)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_note_by_note_id(note_id)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Note was not founded!"


@pytest.mark.asyncio
async def test_get_note_by_note_id_deleted():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id_str = "687c1f81149d65b662bab130"
    mock_repo.get_by_note_id = AsyncMock(
        return_value={
            "_id": note_id_str,
            "title": "Test Note",
            "body": "Test Body",
            "user_id": 1,
            "is_deleted": True,
        }
    )
    service = NoteService(mock_repo)

    note_id = PyObjectId(note_id_str)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_note_by_note_id(note_id)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == f"Note {note_id} was deleted!"


@pytest.mark.asyncio
async def test_get_all_notes_by_user_id_admin():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id_str1 = "687c1f81149d65b662bab130"
    note_id_str2 = "687c1f81149d65b662bab131"
    mock_repo.get_all_by_user_id = AsyncMock(
        return_value=[
            {
                "_id": note_id_str1,
                "title": "Note 1",
                "body": "Body 1",
                "user_id": 1,
                "is_deleted": False,
            },
            {
                "_id": note_id_str2,
                "title": "Note 2",
                "body": "Body 2",
                "user_id": 1,
                "is_deleted": True,
            },
        ]
    )
    service = NoteService(mock_repo)

    user_id = 1
    results = await service.get_all_notes_by_user_id_admin(user_id)

    assert len(results) == 2
    assert results[0].title == "Note 1"
    assert results[1].title == "Note 2"
    assert results[0].is_deleted is False
    assert results[1].is_deleted is True


@pytest.mark.asyncio
async def test_delete_note_by_note_id_and_user_id_success():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id_str = "687c1f81149d65b662bab130"
    mock_repo.soft_delete = AsyncMock(return_value=True)
    service = NoteService(mock_repo)

    note_id = PyObjectId(note_id_str)
    user_id = 1

    result = await service.delete_note_by_note_id_and_user_id(note_id, user_id)

    assert result is True
    mock_repo.soft_delete.assert_awaited_once_with(note_id, user_id)


@pytest.mark.asyncio
async def test_delete_note_by_note_id_and_user_id_failure():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id_str = "687c1f81149d65b662bab130"
    mock_repo.soft_delete = AsyncMock(return_value=False)
    service = NoteService(mock_repo)

    note_id = PyObjectId(note_id_str)
    user_id = 1

    with pytest.raises(HTTPException) as exc_info:
        await service.delete_note_by_note_id_and_user_id(note_id, user_id)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == f"Note {note_id_str} was not deleted!"


@pytest.mark.asyncio
async def test_restore_note_by_note_id_success():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id_str = "687c1f81149d65b662bab130"
    mock_repo.restore = AsyncMock(return_value=True)
    service = NoteService(mock_repo)

    note_id = PyObjectId(note_id_str)

    result = await service.restore_note_by_note_id(note_id)

    assert result is True
    mock_repo.restore.assert_awaited_once_with(note_id)


@pytest.mark.asyncio
async def test_restore_note_by_note_id_failure():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id_str = "687c1f81149d65b662bab130"
    mock_repo.restore = AsyncMock(return_value=False)
    service = NoteService(mock_repo)

    note_id = PyObjectId(note_id_str)

    with pytest.raises(HTTPException) as exc_info:
        await service.restore_note_by_note_id(note_id)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == f"Note {note_id_str} was not restored!"


@pytest.mark.asyncio
async def test_update_note_by_id_success():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id_str = "687c1f81149d65b662bab130"
    mock_repo.update = AsyncMock(
        return_value={
            "_id": note_id_str,
            "title": "Updated Title",
            "body": "Updated Body",
            "user_id": 1,
            "is_deleted": False,
        }
    )
    service = NoteService(mock_repo)

    note_id = PyObjectId(note_id_str)
    user_id = 1
    update_data = UpdateNoteRequestV1(title="Updated Title", body="Updated Body")

    result = await service.update_note_by_id(note_id, user_id, update_data)

    assert isinstance(result, NoteResponseV1)
    assert result.title == "Updated Title"
    assert result.body == "Updated Body"
    mock_repo.update.assert_awaited_once_with(note_id, user_id, {"title": "Updated Title", "body": "Updated Body"})


@pytest.mark.asyncio
async def test_update_note_by_id_failure():
    mock_repo = AsyncMock(spec=NoteRepository)
    note_id_str = "687c1f81149d65b662bab130"
    mock_repo.update = AsyncMock(return_value=None)
    service = NoteService(mock_repo)

    note_id = PyObjectId(note_id_str)
    user_id = 1
    update_data = UpdateNoteRequestV1(title="Updated Title", body="Updated Body")

    with pytest.raises(HTTPException) as exc_info:
        await service.update_note_by_id(note_id, user_id, update_data)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == f"Note {note_id_str} was not restored!"
