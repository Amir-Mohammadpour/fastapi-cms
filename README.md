# Async CMS API

A simple asynchronous Content Management System API built with FastAPI, SQLAlchemy (async), JWT authentication, and Docker support.

## Features

- User registration & login (JWT)
- Create, read, update, delete blog posts
- Post ownership validation (users can only edit/delete their own posts)
- Async SQLAlchemy with SQLite (easily switch to PostgreSQL)
- Alembic for database migrations
- Docker ready
- Unit and integration tests with pytest

## Tech Stack

- FastAPI
- SQLAlchemy 2.0 (async)
- SQLite + aiosqlite
- python-jose (JWT)
- passlib (bcrypt)
- Alembic
- Docker & Docker Compose
- pytest + httpx (testing)

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Amir-Mohammadpour/fastapi-cms.git
cd fastapi-cms
```

### 2. Set up environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

```env
DATABASE_URL=sqlite+aiosqlite:///./sql_app.db
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> Generate a secure key with: `openssl rand -hex 32`

### 3. Run with Docker (recommended)

```bash
docker compose up --build
```

The API will be available at http://localhost:8000

### 4. Run locally (without Docker)

Install dependencies:

```bash
pip install -r requirements.txt
```

Run database migrations:

```bash
alembic upgrade head
```

Start the server:

```bash
uvicorn app.main:app --reload
```

## API Endpoints
    Method	 Endpoint	        Description	            Auth required
    POST    /auth/register/	  Register a new user	         No
    POST    /auth/login/	  Login & get access token	     No
    GET	    /posts/	              List all posts	         No
    GET	    /posts/{id}/	     Get a single post	         No
    POST    /posts/      	     Create a new post	         Yes
    PUT	    /posts/{id}/	  Update a post (owner only)	 Yes
    DELETE  /posts/{id}/	  Delete a post (owner only)	 Yes


## Testing

Install test dependencies:

```bash
pip install pytest pytest-asyncio httpx
```

Run all tests:

```bash
pytest tests/ -v
```

Run a specific test file:

```bash
pytest tests/test_auth.py -v
pytest tests/test_posts.py -v
pytest tests/test_security.py -v
```

### Test Coverage

| File | Type | Description |
|------|------|-------------|
| `tests/test_security.py` | Unit | Password hashing, JWT token creation and decoding |
| `tests/test_auth.py` | Integration | User registration and login flows |
| `tests/test_posts.py` | Integration | Post CRUD and ownership authorization |

## Database Migrations

Create a new migration after model changes:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
alembic upgrade head
```

## Project Structure

```
├── app/
│   ├── api/endpoints/     # auth, posts routers
│   ├── core/              # config, security
│   ├── crud/              # database operations
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── database.py        # async engine & session
│   └── main.py            # FastAPI app
├── alembic/               # migration scripts
├── tests/
│   ├── conftest.py        # shared fixtures
│   ├── test_security.py   # unit tests
│   ├── test_auth.py       # auth integration tests
│   └── test_posts.py      # posts integration tests
├── .env.example
├── .gitignore
├── requirements.txt
├── pytest.ini
├── Dockerfile
└── docker-compose.yml
```