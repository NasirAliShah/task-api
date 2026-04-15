# Task API built with FastAPI and MongoDB

A production-ready RESTful API for task management with JWT authentication, built with FastAPI and MongoDB.

## Features

### Core Features
- **Create Task**: Add new tasks with title, description, and completion status
- **List Tasks**: Retrieve all tasks with pagination support
- **Get Task**: Fetch a specific task by ID
- **Update Task**: Modify existing task details
- **Delete Task**: Remove tasks from the database

### Security & Authentication
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt-based password hashing with salt
- **User Registration**: Create new user accounts
- **User Login**: Authenticate and receive JWT tokens
- **Task Ownership**: Tasks are isolated per user

### Monitoring & Logging
- **Structured Logging**: File and console logging with rotation
- **Request Logging**: Track all API requests and responses
- **Error Tracking**: Comprehensive error logging

### Testing & Quality
- **Pytest Test Suite**: Comprehensive unit and integration tests
- **Async Test Support**: Full async/await testing
- **Test Fixtures**: Pre-configured test database and users

### Deployment
- **Docker Support**: Containerized application
- **Docker Compose**: Complete stack with MongoDB
- **Environment Configuration**: Flexible configuration management

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for data persistence
- **Motor**: Async MongoDB driver for Python
- **Pydantic**: Data validation using Python type annotations
- **PyJWT**: JSON Web Token implementation
- **Passlib**: Password hashing library
- **Pytest**: Testing framework
- **Docker**: Containerization

## Prerequisites

- Python 3.8+
- MongoDB 4.0+ (or use Docker Compose)
- Docker & Docker Compose (optional, for containerized deployment)

## Installation

### Option 1: Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd task-api
```

2. Create a virtual environment:
```bash
python3 -m venv venv
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
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
```

### Option 2: Docker Deployment

1. Clone the repository:
```bash
git clone <repository-url>
cd task-api
```

2. Start with Docker Compose:
```bash
docker-compose up -d
```

This will start both MongoDB and the FastAPI application.

## Running the Application

### Local Development
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

### Docker
```bash
docker-compose up
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token

### Tasks (Requires Authentication)
- `POST /tasks` - Create a new task
- `GET /tasks` - List all tasks (supports pagination with `skip` and `limit` query params)
- `GET /tasks/{task_id}` - Get a specific task by ID
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

## Example Usage

### Register a User
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "username": "johndoe",
    "created_at": "2024-04-15T10:00:00"
  }
}
```

### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API docs",
    "completed": false
  }'
```

### List All Tasks
```bash
curl -X GET "http://localhost:8000/tasks" \
  -H "Authorization: Bearer <your_access_token>"
```

### Get a Specific Task
```bash
curl -X GET "http://localhost:8000/tasks/{task_id}" \
  -H "Authorization: Bearer <your_access_token>"
```

### Update a Task
```bash
curl -X PUT "http://localhost:8000/tasks/{task_id}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "completed": true
  }'
```

### Delete a Task
```bash
curl -X DELETE "http://localhost:8000/tasks/{task_id}" \
  -H "Authorization: Bearer <your_access_token>"
```

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_auth.py
pytest tests/test_tasks.py
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage
```bash
pytest --cov=app
```

### Test Files
- `tests/test_auth.py` - Authentication and user registration tests
- `tests/test_tasks.py` - Task CRUD operation tests
- `tests/conftest.py` - Shared test fixtures and configuration

## Project Structure

```
task-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and routes
│   ├── models.py            # Task Pydantic models/schemas
│   ├── user_models.py       # User Pydantic models/schemas
│   ├── crud.py              # Task CRUD operations
│   ├── user_crud.py         # User CRUD operations
│   ├── database.py          # Database connection
│   ├── config.py            # Configuration settings
│   ├── security.py          # JWT and password utilities
│   ├── auth.py              # Authentication dependencies
│   ├── exceptions.py        # Custom exception classes
│   └── logger.py            # Logging configuration
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest configuration and fixtures
│   ├── test_auth.py         # Authentication tests
│   └── test_tasks.py        # Task CRUD tests
├── logs/                    # Application logs (auto-created)
├── .env.example             # Environment variables template
├── .gitignore
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Docker Compose stack
├── requirements.txt         # Python dependencies
├── LICENSE
└── README.md
```

## Security Features

### Password Security
- Bcrypt hashing with salt
- Passwords never stored in plain text
- Secure password verification

### JWT Authentication
- Token-based authentication
- Configurable token expiration
- Secure token validation

### Data Isolation
- Tasks are isolated per user
- Users can only access their own tasks
- Database queries filtered by user_id

### Error Handling
- Standardized exception classes
- Secure error messages (no sensitive data leakage)
- Proper HTTP status codes

## Logging & Monitoring

### Log Levels
- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures

### Log Output
- **File**: `logs/app.log` with rotation (10MB max, 5 backups)
- **Console**: Real-time log output to stdout

### Logged Events
- User registration and login attempts
- Task creation, updates, and deletions
- Authentication failures
- Database connection status

## Deployment

### Local Development
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Docker Deployment
```bash
docker-compose up -d
```

### Production Considerations
1. Change `SECRET_KEY` in `.env` to a secure random string
2. Use a production MongoDB instance
3. Set `DEBUG=False` in production
4. Use a production ASGI server (Gunicorn + Uvicorn)
5. Enable HTTPS/TLS
6. Set up proper monitoring and alerting
7. Configure database backups

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017` |
| `DATABASE_NAME` | Database name | `taskdb` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-change-in-production` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_HOURS` | Token expiration time | `24` |

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running
- Check `MONGODB_URL` in `.env`
- Verify network connectivity

### Authentication Errors
- Ensure token is included in `Authorization` header
- Check token hasn't expired
- Verify email and password are correct

### Docker Issues
- Ensure Docker and Docker Compose are installed
- Check port 8000 and 27017 are available
- View logs: `docker-compose logs -f`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
