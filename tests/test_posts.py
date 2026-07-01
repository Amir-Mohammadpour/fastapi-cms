import pytest
from httpx import AsyncClient


async def create_user_and_get_token(
    client: AsyncClient, username: str, email: str
) -> str:
    await client.post(
        "/auth/register/",
        json={
            "username": username,
            "email": email,
            "password": "testpass123",
        },
    )
    response = await client.post(
        "/auth/login/",
        data={
            "username": username,
            "password": "testpass123",
        },
    )
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_post_success(client: AsyncClient):
    token = await create_user_and_get_token(client, "postuser", "post@example.com")
    response = await client.post(
        "/posts/",
        json={"title": "پست اول", "content": "محتوای پست اول"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_posts_empty(client: AsyncClient):
    response = await client.get("/posts/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_nonexistent(client: AsyncClient):
    response = await client.get("/posts/9999/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_post_without_token(client: AsyncClient):
    response = await client.post(
        "/posts/", json={"title": "پست بدون login", "content": "محتوا"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_post_success(client: AsyncClient):
    token = await create_user_and_get_token(client, "updateuser", "update@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    create_response = await client.post(
        "/posts/",
        json={"title": "عنوان قدیمی", "content": "محتوای قدیمی"},
        headers=headers,
    )
    post_id = create_response.json()["id"]
    response = await client.put(
        f"/posts/{post_id}/",
        json={"title": "عنوان جدید"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "عنوان جدید"
    assert response.json()["content"] == "محتوای قدیمی"


@pytest.mark.asyncio
async def test_update_post_by_other_user(client: AsyncClient):
    token1 = await create_user_and_get_token(client, "owner_user", "owner@example.com")
    create_response = await client.post(
        "/posts/",
        json={"title": "پست من", "content": "محتوا"},
        headers={"Authorization": f"Bearer {token1}"},
    )
    post_id = create_response.json()["id"]

    token2 = await create_user_and_get_token(
        client, "hacker_user", "hacker@example.com"
    )

    response = await client.put(
        f"/posts/{post_id}/",
        json={"title": "هک شد!"},
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_post_success(client: AsyncClient):
    token = await create_user_and_get_token(client, "deleteuser", "delete@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create_response = await client.post(
        "/posts/", json={"title": "پست برای حذف", "content": "محتوا"}, headers=headers
    )
    post_id = create_response.json()["id"]

    response = await client.delete(f"/posts/{post_id}/", headers=headers)
    assert response.status_code == 204

    get_response = await client.get(f"/posts/{post_id}/")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_post_by_other_user(client: AsyncClient):
    token1 = await create_user_and_get_token(
        client, "real_owner", "realowner@example.com"
    )
    create_response = await client.post(
        "/posts/",
        json={"title": "پست اصلی", "content": "محتوا"},
        headers={"Authorization": f"Bearer {token1}"},
    )
    post_id = create_response.json()["id"]

    token2 = await create_user_and_get_token(client, "intruder", "intruder@example.com")
    response = await client.delete(
        f"/posts/{post_id}/", headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 403

    get_response = await client.get(f"/posts/{post_id}/")
    assert get_response.status_code == 200
