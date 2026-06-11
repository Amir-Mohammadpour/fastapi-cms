# Async CMS API

A simple asynchronous Content Management System API built with FastAPI, SQLAlchemy (async), JWT authentication, and Docker support.

## Features

- User registration & login (JWT)
- Create, read, update, delete blog posts
- Post ownership validation (users can only edit/delete their own posts)
- Async SQLAlchemy with SQLite (easily switch to PostgreSQL)
- Alembic for database migrations
- Docker ready

## Tech Stack

- FastAPI
- SQLAlchemy 2.0 (async)
- SQLite + aiosqlite
- python-jose (JWT)
- passlib (bcrypt)
- Alembic
- Docker & Docker Compose

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/async-cms-api.git
cd async-cms-api


2. Set up environment variables
Create a .env file in the project root:
    DATABASE_URL=sqlite+aiosqlite:///./sql_app.db
    SECRET_KEY=your-super-secret-key-change-this
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30


3. Run with Docker (recommended)
    docker compose up --build
The API will be available at http://localhost:8000


4. Run locally (without Docker)
Install dependencies:
    pip install -r requirements.txt
Run database migrations:
    alembic upgrade head
Start the server:
    uvicorn app.main:app --reload


API Endpoints
    Method	 Endpoint	        Description	            Auth required
    POST    /auth/register/	  Register a new user	         No
    POST    /auth/login/	  Login & get access token	     No
    GET	    /posts/	              List all posts	         No
    GET	    /posts/{id}/	     Get a single post	         No
    POST    /posts/      	     Create a new post	         Yes
    PUT	    /posts/{id}/	  Update a post (owner only)	 Yes
    DELETE  /posts/{id}/	  Delete a post (owner only)	 Yes


Database Migrations
Create a new migration after model changes:
    alembic revision --autogenerate -m "description"
Apply migrations:
    alembic upgrade head


Project Structure
    ├── app/
    │   ├── api/endpoints/     # auth, posts routers
    │   ├── core/              # config, security
    │   ├── crud/              # database operations
    │   ├── models/            # SQLAlchemy models
    │   ├── schemas/           # Pydantic schemas
    │   ├── database.py        # async engine & session
    │   └── main.py            # FastAPI app
    ├── alembic/               # migration scripts
    ├── .env
    ├── .gitignore
    ├── requirements.txt
    ├── Dockerfile
    ├── docker-compose.yml
