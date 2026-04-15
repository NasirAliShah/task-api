import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.main import app
from app.database import get_database
from httpx import AsyncClient

@pytest.fixture
async def db():
    client = AsyncIOMotorClient(settings.mongodb_url)
    database = client[settings.database_name + "_test"]
    yield database
    await client.drop_database(settings.database_name + "_test")
    client.close()

async def override_get_database():
    client = AsyncIOMotorClient(settings.mongodb_url)
    return client[settings.database_name + "_test"]

@pytest.fixture
async def client(db):
    app.dependency_overrides[get_database] = override_get_database
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.fixture
async def cleanup_db(db):
    yield
    await db.users.delete_many({})
    await db.tasks.delete_many({})

@pytest.fixture
async def test_user(db, cleanup_db):
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "hashed_password": "$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUm"
    }
    result = await db.users.insert_one(user_data)
    user_data["_id"] = result.inserted_id
    return user_data

@pytest.fixture
async def test_token(test_user):
    from app.security import SecurityUtils
    from datetime import timedelta
    token = SecurityUtils.create_access_token(
        data={"sub": test_user["email"]},
        expires_delta=timedelta(hours=24)
    )
    return token
