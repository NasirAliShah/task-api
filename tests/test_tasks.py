import pytest

@pytest.mark.asyncio
async def test_create_task_authenticated(client, test_token):
    response = await client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False
        },
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["completed"] is False

@pytest.mark.asyncio
async def test_create_task_unauthenticated(client):
    response = await client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False
        }
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_list_tasks(client, test_token):
    await client.post(
        "/tasks",
        json={
            "title": "Task 1",
            "description": "First task",
            "completed": False
        },
        headers={"Authorization": f"Bearer {test_token}"}
    )
    response = await client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_get_task(client, test_token):
    create_response = await client.post(
        "/tasks",
        json={
            "title": "Get Test Task",
            "description": "Task to retrieve",
            "completed": False
        },
        headers={"Authorization": f"Bearer {test_token}"}
    )
    task_id = create_response.json()["id"]
    
    response = await client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Test Task"

@pytest.mark.asyncio
async def test_update_task(client, test_token):
    create_response = await client.post(
        "/tasks",
        json={
            "title": "Update Test Task",
            "description": "Task to update",
            "completed": False
        },
        headers={"Authorization": f"Bearer {test_token}"}
    )
    task_id = create_response.json()["id"]
    
    response = await client.put(
        f"/tasks/{task_id}",
        json={"completed": True},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True

@pytest.mark.asyncio
async def test_delete_task(client, test_token):
    create_response = await client.post(
        "/tasks",
        json={
            "title": "Delete Test Task",
            "description": "Task to delete",
            "completed": False
        },
        headers={"Authorization": f"Bearer {test_token}"}
    )
    task_id = create_response.json()["id"]
    
    response = await client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 204
