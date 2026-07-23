import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    response = await client.post(
        "/auth/register/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient):
    await client.post(
        "/auth/register/",
        json={
            "username": "duplicate_user",
            "email": "first@example.com",
            "password": "pass1234",
        },
    )
    response = await client.post(
        "/auth/register/",
        json={
            "username": "duplicate_user",
            "email": "second@example.com",
            "password": "pass1234",
        },
    )
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    await client.post(
        "/auth/register/",
        json={
            "username": "user_one",
            "email": "same@example.com",
            "password": "pass1234",
        },
    )
    response = await client.post(
        "/auth/register/",
        json={
            "username": "user_two",
            "email": "same@example.com",
            "password": "pass1234",
        },
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient):
    response = await client.post(
        "/auth/register/",
        json={"username": "baduser", "email": "not-an-email", "password": "pass1234"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    await client.post(
        "/auth/register/",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "mypassword",
        },
    )
    response = await client.post(
        "/auth/login/",
        data={
            "username": "loginuser",
            "password": "mypassword",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        "/auth/register/",
        json={
            "username": "wrongpassuser",
            "email": "wrongpass@example.com",
            "password": "correctpass",
        },
    )
    response = await client.post(
        "/auth/login/",
        data={
            "username": "wrongpassuser",
            "password": "wrongpass",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post(
        "/auth/login/",
        data={
            "username": "nobody",
            "password": "nopassword",
        },
    )
    assert response.status_code == 401
