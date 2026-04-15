# Task API built with FastAPI and MongoDB

A simple RESTful API for task management built with FastAPI and MongoDB.

## Features

- **Create Task**: Add new tasks with title, description, and completion status
- **List Tasks**: Retrieve all tasks with pagination support
- **Get Task**: Fetch a specific task by ID
- **Update Task**: Modify existing task details
- **Delete Task**: Remove tasks from the database

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for data persistence
- **Motor**: Async MongoDB driver for Python
- **Pydantic**: Data validation using Python type annotations

## Prerequisites

- Python 3.8+
- MongoDB (running locally or remote instance)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd task-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` file with your MongoDB connection details:
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=taskdb
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Root
- `GET /` - Welcome message

### Tasks
- `POST /tasks` - Create a new task
- `GET /tasks` - List all tasks (supports pagination with `skip` and `limit` query params)
- `GET /tasks/{task_id}` - Get a specific task by ID
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

## Example Usage

### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API docs",
    "completed": false
  }'
```

### List All Tasks
```bash
curl -X GET "http://localhost:8000/tasks"
```

### Get a Specific Task
```bash
curl -X GET "http://localhost:8000/tasks/{task_id}"
```

### Update a Task
```bash
curl -X PUT "http://localhost:8000/tasks/{task_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

### Delete a Task
```bash
curl -X DELETE "http://localhost:8000/tasks/{task_id}"
```

## Project Structure

```
task-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and routes
│   ├── models.py        # Pydantic models/schemas
│   ├── crud.py          # CRUD operations
│   ├── database.py      # Database connection
│   └── config.py        # Configuration settings
├── .env.example         # Environment variables template
├── .gitignore
├── requirements.txt     # Python dependencies
├── LICENSE
└── README.md
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
