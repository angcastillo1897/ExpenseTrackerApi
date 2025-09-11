# to run the project

### pre requisites :

- docker
- python 3.12.0
- uv

### Commands to run project at the beginning :

- uv sync
- uv run uvicorn app.main:app --reload

### architecture

Layered (N-Tier) Architecture

Flow of Data
Client → Presentation Layer
API receives the request (POST /users).
Presentation → Service Layer
Endpoint calls UserService.create_user.
Service → Repository Layer
Service checks if email exists, then calls UserRepository.create.
Repository → Database Layer
Repository persists the new user with SQLAlchemy.
Database → Repository → Service → Presentation → Client
Data bubbles back up, transformed as needed.

Controllers = handle requests.
Services = define business rules.
Repositories = talk to DB.
Models = represent data.
