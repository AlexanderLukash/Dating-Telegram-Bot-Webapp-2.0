from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

import pytest
from faker import Faker
from httpx import Response


@pytest.mark.asyncio
async def test_get_all_users_success(app: FastAPI, client: TestClient):
    url = app.url_path_for("get_all_users_handler")
    response: Response = client.get(url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()

    assert "count" in json_data
    assert "limit" in json_data
    assert "offset" in json_data
    assert "items" in json_data
    assert isinstance(json_data["items"], list)


@pytest.mark.asyncio
async def test_get_user_not_found(app: FastAPI, client: TestClient):
    url = app.url_path_for("get_user_handler", user_id=999)
    response: Response = client.get(url)

    assert not response.is_success
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_data = response.json()

    assert "error" in json_data["detail"]


@pytest.mark.asyncio
async def test_get_users_liked_from_success(app: FastAPI, client: TestClient):
    url = app.url_path_for("get_users_liked_from", user_id=1)
    response: Response = client.get(url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()

    assert "items" in json_data
    assert isinstance(json_data["items"], list)


@pytest.mark.asyncio
async def test_get_users_liked_by_success(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for("get_users_liked_by", user_id=1)
    response: Response = client.get(url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()

    assert "items" in json_data
    assert isinstance(json_data["items"], list)
