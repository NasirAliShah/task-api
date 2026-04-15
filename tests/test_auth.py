import pytest

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "pass1234"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "newuser@example.com"
    assert data["user"]["username"] == "newuser"
    assert "id" in data["user"]

@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    await client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "pass1234"
        }
    )
    response = await client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "user2",
            "password": "pass1234"
        }
    )
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_login_success(client):
    await client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "pass1234"
        }
    )
    response = await client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "pass1234"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "login@example.com"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    response = await client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401
