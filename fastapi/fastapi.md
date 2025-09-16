# Complete FastAPI Interview Guide - 6+ Years Experience

## Table of Contents
1. [FastAPI Fundamentals](#fastapi-fundamentals)
2. [API Design & Architecture](#api-design--architecture)
3. [Authentication & Authorization](#authentication--authorization)
4. [Database Integration](#database-integration)
5. [Advanced Features](#advanced-features)
6. [Performance & Optimization](#performance--optimization)
7. [Testing](#testing)
8. [Deployment & Production](#deployment--production)
9. [Real-world Scenarios](#real-world-scenarios)

---

## FastAPI Fundamentals

### Q1: What makes FastAPI different from Flask and Django REST Framework?

**Answer:**
FastAPI offers several key advantages:
- **Automatic API documentation** with OpenAPI/Swagger
- **Type hints integration** with automatic validation
- **Async support** built-in with better performance
- **Modern Python features** (Python 3.6+ type hints)
- **Pydantic integration** for data validation
- **High performance** comparable to NodeJS and Go

**Example:**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

@app.post("/users/")
async def create_user(user: User):
    # Automatic validation, serialization, and documentation
    return {"message": f"User {user.name} created"}
```

### Q2: Explain the request lifecycle in FastAPI

**Answer:**
1. **Request received** by ASGI server (Uvicorn/Hypercorn)
2. **Middleware processing** (CORS, authentication, etc.)
3. **Route matching** and path parameter extraction
4. **Dependency injection** resolution
5. **Request validation** using Pydantic models
6. **Handler function execution**
7. **Response serialization**
8. **Middleware post-processing**
9. **Response sent** to client

### Q3: How do you handle different HTTP methods and status codes?

**Answer:**
```python
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/items/{item_id}", status_code=status.HTTP_200_OK)
async def get_item(item_id: int):
    if item_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return {"item_id": item_id}

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: dict):
    # Custom response with headers
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Item created"},
        headers={"X-Custom-Header": "value"}
    )
```

---

## API Design & Architecture

### Q4: How do you structure a large FastAPI application?

**Answer:**
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── users.py
│   │       │   └── items.py
│   │       └── api.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── tests/
├── requirements.txt
└── Dockerfile
```

**main.py:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
```

### Q5: How do you implement API versioning?

**Answer:**
```python
# Method 1: URL Path Versioning
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.get("/users/")
async def get_users_v1():
    return {"version": "1.0", "users": []}

@v2_router.get("/users/")
async def get_users_v2():
    return {"version": "2.0", "users": [], "metadata": {}}

# Method 2: Header Versioning
from fastapi import Header, HTTPException

@app.get("/users/")
async def get_users(api_version: str = Header(default="1.0")):
    if api_version == "1.0":
        return {"version": "1.0", "users": []}
    elif api_version == "2.0":
        return {"version": "2.0", "users": [], "metadata": {}}
    else:
        raise HTTPException(400, "Unsupported API version")
```

### Q6: How do you handle request/response models with Pydantic?

**Answer:**
```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class UserBase(BaseModel):
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        return v

class UserResponse(UserBase):
    id: int
    status: UserStatus
    created_at: datetime
    
    class Config:
        from_attributes = True  # For SQLAlchemy models

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    status: Optional[UserStatus] = None

# Usage in endpoints
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    # Process user creation
    return user_from_db
```

---

## Authentication & Authorization

### Q7: How do you implement JWT authentication?

**Answer:**
```python
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI()
security = HTTPBearer()

# Configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Login endpoint
@app.post("/token")
async def login(form_data: UserLogin):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Protected endpoint
@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}
```

### Q8: How do you implement role-based access control?

**Answer:**
```python
from functools import wraps
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

class User(BaseModel):
    username: str
    email: str
    roles: List[UserRole]
    is_active: bool = True

def require_roles(*required_roles: UserRole):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if not current_user.is_active:
                raise HTTPException(403, "Account is deactivated")
            
            user_roles = set(current_user.roles)
            if not any(role in user_roles for role in required_roles):
                raise HTTPException(
                    403, 
                    f"Access denied. Required roles: {required_roles}"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Usage
@app.delete("/users/{user_id}")
@require_roles(UserRole.ADMIN)
async def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    # Only admins can delete users
    return {"message": f"User {user_id} deleted"}

# Advanced permission system
class Permission(BaseModel):
    resource: str
    action: str

def check_permission(resource: str, action: str):
    async def permission_checker(current_user: User = Depends(get_current_user)):
        # Check user permissions from database
        user_permissions = get_user_permissions(current_user.id)
        required_permission = f"{resource}:{action}"
        
        if required_permission not in user_permissions:
            raise HTTPException(403, "Insufficient permissions")
        return current_user
    return Depends(permission_checker)

@app.post("/admin/settings")
async def update_settings(
    settings: dict,
    current_user: User = check_permission("admin", "write")
):
    return {"message": "Settings updated"}
```

### Q9: How do you handle OAuth2 integration?

**Answer:**
```python
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authlib.integrations.starlette_client import OAuth
import httpx

app = FastAPI()

# OAuth2 setup
oauth = OAuth()
oauth.register(
    name='google',
    client_id='your-google-client-id',
    client_secret='your-google-client-secret',
    authorization_endpoint='https://accounts.google.com/o/oauth2/auth',
    token_endpoint='https://accounts.google.com/o/oauth2/token',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'}
)

@app.get("/auth/google")
async def google_auth():
    redirect_uri = "http://localhost:8000/auth/callback"
    return await oauth.google.authorize_redirect(redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.get_userinfo(token)
    
    # Create or update user in your database
    user = await create_or_update_user(user_info)
    
    # Generate your own JWT token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Multiple OAuth providers
@app.get("/auth/{provider}")
async def oauth_login(provider: str):
    if provider not in ['google', 'github', 'facebook']:
        raise HTTPException(400, "Unsupported provider")
    
    oauth_client = getattr(oauth, provider)
    redirect_uri = f"http://localhost:8000/auth/{provider}/callback"
    return await oauth_client.authorize_redirect(redirect_uri)
```

---

## Database Integration

### Q10: How do you integrate SQLAlchemy with FastAPI?

**Answer:**
```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # Set to False in production
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="items")

# crud.py
from sqlalchemy.orm import Session
from typing import List, Optional

class UserCRUD:
    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()
    
    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()
    
    def create_user(self, db: Session, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            hashed_password=get_password_hash(user.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def update_user(self, db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
        db_user = self.get_user(db, user_id)
        if not db_user:
            return None
        
        for field, value in user.dict(exclude_unset=True).items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user

user_crud = UserCRUD()

# endpoints.py
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(400, "Email already registered")
    return user_crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_crud.get_users(db, skip=skip, limit=limit)
```

### Q11: How do you handle database migrations?

**Answer:**
```python
# Using Alembic for migrations
# alembic.ini configuration
# Then create migration files

# versions/001_create_users_table.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

def downgrade():
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

# Running migrations programmatically
from alembic import command
from alembic.config import Config

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

# In your startup event
@app.on_event("startup")
async def startup_event():
    run_migrations()
```

### Q12: How do you implement async database operations?

**Answer:**
```python
# Using SQLAlchemy 2.0 with asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session

# Async CRUD operations
class AsyncUserCRUD:
    async def get_user(self, db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_users(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def create_user(self, db: AsyncSession, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            hashed_password=get_password_hash(user.password)
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

# Using with endpoints
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

# Connection pooling and optimization
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)
```

---

## Advanced Features

### Q13: How do you implement custom middleware?

**Answer:**
```python
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url}")
        
        # Process request
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
        
        response.headers["X-Process-Time"] = str(process_time)
        return response

class RateLimitingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old requests
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if current_time - req_time < 60
            ]
        else:
            self.requests[client_ip] = []
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return Response(
                content="Rate limit exceeded",
                status_code=429,
                headers={"Retry-After": "60"}
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        return await call_next(request)

# Add middleware to app
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitingMiddleware, requests_per_minute=100)

# Database session middleware
class DatabaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        async with async_session() as session:
            request.state.db = session
            response = await call_next(request)
            return response
```

### Q14: How do you handle background tasks?

**Answer:**
```python
from fastapi import BackgroundTasks
import smtplib
from email.mime.text import MIMEText
import asyncio

# Simple background task
def send_email(email: str, message: str):
    # Email sending logic
    print(f"Sending email to {email}: {message}")
    time.sleep(2)  # Simulate email sending

@app.post("/send-notification/")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification will be sent in background"}

# Using Celery for complex background jobs
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def process_large_file(file_path: str):
    # Heavy processing logic
    time.sleep(30)
    return {"status": "completed", "file": file_path}

@app.post("/process-file/")
async def process_file(file_path: str):
    task = process_large_file.delay(file_path)
    return {"task_id": task.id, "status": "processing"}

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {"task_id": task_id, "status": task.status, "result": task.result}

# Scheduled tasks with APScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()

async def cleanup_old_data():
    # Cleanup logic
    print("Cleaning up old data...")

@app.on_event("startup")
async def startup_event():
    scheduler.add_job(
        cleanup_old_data,
        CronTrigger(hour=2, minute=0),  # Run at 2 AM daily
        id="cleanup_job"
    )
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
```

### Q15: How do you implement WebSocket connections?

**Answer:**
```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        if user_id:
            self.user_connections[user_id] = websocket
    
    def disconnect(self, websocket: WebSocket, user_id: int = None):
        self.active_connections.remove(websocket)
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def send_to_user(self, message: str, user_id: int):
        if user_id in self.user_connections:
            await self.user_connections[user_id].send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "private":
                # Send to specific user
                await manager.send_to_user(
                    f"Private from {user_id}: {message['content']}",
                    message["target_user"]
                )
            else:
                # Broadcast to all
                await manager.broadcast(
                    f"User {user_id}: {message['content']}"
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast(f"User {user_id} left the chat")

# Chat room implementation
class ChatRoom:
    def __init__(self):
        self.rooms: Dict[str, List[WebSocket]] = {}
    
    async def join_room(self, room_id: str, websocket: WebSocket):
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        self.rooms[room_id].append(websocket)
        await websocket.send_json({"type": "joined", "room": room_id})
    
    async def leave_room(self, room_id: str, websocket: WebSocket):
        if room_id in self.rooms and websocket in self.rooms[room_id]:
            self.rooms[room_id].remove(websocket)
    
    async def broadcast_to_room(self, room_id: str, message: dict):
        if room_id in self.rooms:
            for connection in self.rooms[room_id][:]:  # Copy to avoid modification during iteration
                try:
                    await connection.send_json(message)
                except:
                    self.rooms[room_id].remove(connection)

chat_rooms = ChatRoom()

@app.websocket("/chat/{room_id}")
async def chat_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    await chat_rooms.join_room(room_id, websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            await chat_rooms.broadcast_to_room(room_id, {
                "type": "message",
                "user": data.get("user", "Anonymous"),
                "content": data.get("content", "")
            })
    except WebSocketDisconnect:
        await chat_rooms.leave_room(room_id, websocket)
```

---

## Performance & Optimization

### Q16: How do you optimize FastAPI performance?

**Answer:**
```python
# 1. Connection Pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_recycle=3600,
    pool_pre_ping=True
)

# 2. Response Caching
from functools import lru_cache
import redis
import pickle
from typing import Union

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_response(expiration: int = 300):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return pickle.loads(cached)
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, pickle.dumps(result))
            return result
        return wrapper
    return decorator

@cache_response(expiration=600)
@app.get("/expensive-operation")
async def expensive_operation(param: str):
    # Simulate expensive operation
    await asyncio.sleep(2)
    return {"result": f"Processed {param}"}

# 3. Database Query Optimization
from sqlalchemy.orm import selectinload, joinedload

# Eager loading to prevent N+1 queries
@app.get("/users-with-items")
async def get_users_with_items(db: Session = Depends(get_db)):
    users = db.query(User).options(selectinload(User.items)).all()
    return users

# 4. Async Database Operations
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import gather

async def get_user_data(db: AsyncSession, user_id: int):
    # Run multiple queries concurrently
    user_task = db.execute(select(User).where(User.id == user_id))
    items_task = db.execute(select(Item).where(Item.owner_id == user_id))
    orders_task = db.execute(select(Order).where(Order.user_id == user_id))
    
    user_result, items_result, orders_result = await gather(
        user_task, items_task, orders_task
    )
    
    return {
        "user": user_result.scalar_one_or_none(),
        "items": items_result.scalars().all(),
        "orders": orders_result.scalars().all()
    }

# 5. Response Model Optimization
from pydantic import BaseModel, Field
from typing import List, Optional

class OptimizedUserResponse(BaseModel):
    id: int
    name: str
    # Only include necessary fields
    
    class Config:
        from_attributes = True
        # Enable field aliases for different naming conventions
        allow_population_by_field_name = True

# 6. Streaming Large Responses
from fastapi.responses import StreamingResponse
import csv
from io import StringIO

@app.get("/export-users")
async def export_users(db: Session = Depends(get_db)):
    def generate_csv():
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Name", "Email"])
        
        # Stream data in chunks
        offset = 0
        limit = 1000
        
        while True:
            users = db.query(User).offset(offset).limit(limit).all()
            if not users:
                break
            
            for user in users:
                writer.writerow([user.id, user.name, user.email])
                output.seek(0)
                data = output.read()
                output.seek(0)
                output.truncate(0)
                yield data
            
            offset += limit
    
    return StreamingResponse(
        generate_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"}
    )

# 7. Memory Usage Optimization
from contextlib import asynccontextmanager

@asynccontextmanager
async def optimized_db_session():
    session = AsyncSession()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

# 8. CPU-bound task optimization
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

cpu_executor = ProcessPoolExecutor(max_workers=multiprocessing.cpu_count())

def cpu_intensive_task(data: list):
    # Heavy computation
    return sum(x ** 2 for x in data)

@app.post("/heavy-computation")
async def heavy_computation(data: List[int]):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(cpu_executor, cpu_intensive_task, data)
    return {"result": result}
```

### Q17: How do you implement rate limiting and throttling?

**Answer:**
```python
from fastapi import HTTPException
import time
from collections import defaultdict, deque
import redis
from typing import Dict, Deque

# In-memory rate limiting
class InMemoryRateLimiter:
    def __init__(self):
        self.clients: Dict[str, Deque[float]] = defaultdict(deque)
    
    def is_allowed(self, client_id: str, limit: int, window: int) -> bool:
        now = time.time()
        
        # Clean old entries
        while (self.clients[client_id] and 
               now - self.clients[client_id][0] > window):
            self.clients[client_id].popleft()
        
        # Check if limit exceeded
        if len(self.clients[client_id]) >= limit:
            return False
        
        # Add current request
        self.clients[client_id].append(now)
        return True

# Redis-based rate limiting
class RedisRateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def is_allowed(self, client_id: str, limit: int, window: int) -> bool:
        pipe = self.redis.pipeline()
        now = time.time()
        
        # Remove old entries
        pipe.zremrangebyscore(client_id, 0, now - window)
        # Add current request
        pipe.zadd(client_id, {str(now): now})
        # Count current requests
        pipe.zcard(client_id)
        # Set expiration
        pipe.expire(client_id, window)
        
        results = pipe.execute()
        request_count = results[2]
        
        return request_count <= limit

rate_limiter = RedisRateLimiter(redis.Redis())

# Rate limiting middleware
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, default_limit: int = 100, window: int = 60):
        super().__init__(app)
        self.default_limit = default_limit
        self.window = window
        self.limiter = RedisRateLimiter(redis.Redis())
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        
        if not self.limiter.is_allowed(client_ip, self.default_limit, self.window):
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"},
                headers={"Retry-After": str(self.window)}
            )
        
        return await call_next(request)

# Decorator-based rate limiting
def rate_limit(limit: int, window: int):
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            client_ip = request.client.host
            
            if not rate_limiter.is_allowed(client_ip, limit, window):
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded",
                    headers={"Retry-After": str(window)}
                )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

@app.get("/limited-endpoint")
@rate_limit(limit=10, window=60)  # 10 requests per minute
async def limited_endpoint(request: Request):
    return {"message": "This endpoint is rate limited"}

# Advanced rate limiting with different tiers
class TieredRateLimiter:
    def __init__(self):
        self.limits = {
            "free": {"requests": 100, "window": 3600},
            "premium": {"requests": 1000, "window": 3600},
            "enterprise": {"requests": 10000, "window": 3600}
        }
    
    def get_user_tier(self, user_id: int) -> str:
        # Get user tier from database
        return "free"  # Default
    
    def check_limit(self, user_id: int) -> bool:
        tier = self.get_user_tier(user_id)
        limits = self.limits[tier]
        
        return rate_limiter.is_allowed(
            f"user:{user_id}",
            limits["requests"],
            limits["window"]
        )

tiered_limiter = TieredRateLimiter()

@app.get("/api-endpoint")
async def api_endpoint(current_user: User = Depends(get_current_user)):
    if not tiered_limiter.check_limit(current_user.id):
        raise HTTPException(429, "API limit exceeded for your tier")
    
    return {"data": "API response"}
```

### Q18: How do you handle file uploads efficiently?

**Answer:**
```python
from fastapi import File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import aiofiles
from pathlib import Path
import uuid
from PIL import Image
import asyncio

# Basic file upload
@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "text/plain", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, "File type not allowed")
    
    # Validate file size (10MB limit)
    max_size = 10 * 1024 * 1024
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(400, "File too large")
    
    # Save file
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(content)
    
    return {"filename": file.filename, "size": len(content)}

# Async file upload with streaming
@app.post("/upload-large-file/")
async def upload_large_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = Path(f"uploads/{file_id}_{file.filename}")
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while content := await file.read(8192):  # Read in 8KB chunks
                await f.write(content)
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(500, f"File upload failed: {str(e)}")
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "size": file_path.stat().st_size
    }

# Multiple file uploads
@app.post("/upload-multiple/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    if len(files) > 10:
        raise HTTPException(400, "Too many files (max 10)")
    
    uploaded_files = []
    
    for file in files:
        if file.size > 5 * 1024 * 1024:  # 5MB limit per file
            continue
        
        file_id = str(uuid.uuid4())
        file_path = f"uploads/{file_id}_{file.filename}"
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        uploaded_files.append({
            "file_id": file_id,
            "filename": file.filename,
            "size": len(content)
        })
    
    return {"uploaded_files": uploaded_files}

# Image processing and upload
@app.post("/upload-image/")
async def upload_image(
    file: UploadFile = File(...),
    resize: bool = Form(False),
    max_width: int = Form(800)
):
    # Validate image
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")
    
    # Process image
    content = await file.read()
    
    if resize:
        # Process in background thread to avoid blocking
        loop = asyncio.get_event_loop()
        processed_content = await loop.run_in_executor(
            None, process_image, content, max_width
        )
    else:
        processed_content = content
    
    # Save processed image
    file_id = str(uuid.uuid4())
    file_path = f"uploads/processed_{file_id}.jpg"
    
    with open(file_path, 'wb') as f:
        f.write(processed_content)
    
    return {
        "file_id": file_id,
        "original_size": len(content),
        "processed_size": len(processed_content)
    }

def process_image(content: bytes, max_width: int) -> bytes:
    """Process image in a separate thread"""
    from io import BytesIO
    
    # Open image
    image = Image.open(BytesIO(content))
    
    # Resize if needed
    if image.width > max_width:
        ratio = max_width / image.width
        new_height = int(image.height * ratio)
        image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
    
    # Save to bytes
    output = BytesIO()
    image.save(output, format='JPEG', quality=85)
    return output.getvalue()

# File download with range support
@app.get("/download/{file_id}")
async def download_file(file_id: str, request: Request):
    file_path = Path(f"uploads/{file_id}")
    
    if not file_path.exists():
        raise HTTPException(404, "File not found")
    
    # Handle range requests for large files
    range_header = request.headers.get("Range")
    if range_header:
        return handle_range_request(file_path, range_header)
    
    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type='application/octet-stream'
    )

def handle_range_request(file_path: Path, range_header: str):
    """Handle HTTP range requests for file streaming"""
    file_size = file_path.stat().st_size
    
    # Parse range header
    range_match = re.search(r'bytes=(\d+)-(\d*)', range_header)
    if not range_match:
        raise HTTPException(400, "Invalid range header")
    
    start = int(range_match.group(1))
    end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
    
    if start >= file_size or end >= file_size:
        raise HTTPException(416, "Range not satisfiable")
    
    # Read file chunk
    with open(file_path, 'rb') as f:
        f.seek(start)
        chunk = f.read(end - start + 1)
    
    return Response(
        content=chunk,
        status_code=206,
        headers={
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(len(chunk))
        }
    )

# Cleanup old files
@app.on_event("startup")
async def cleanup_old_files():
    """Scheduled cleanup of old uploaded files"""
    def cleanup():
        upload_dir = Path("uploads")
        cutoff_time = time.time() - (7 * 24 * 3600)  # 7 days
        
        for file_path in upload_dir.glob("*"):
            if file_path.stat().st_mtime < cutoff_time:
                file_path.unlink()
    
    # Run cleanup every hour
    scheduler.add_job(cleanup, "interval", hours=1)
```

---

## Testing

### Q19: How do you write comprehensive tests for FastAPI?

**Answer:**
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base
import tempfile
import os

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    # Create test database
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    # Cleanup
    Base.metadata.drop_all(bind=engine)

# Basic endpoint testing
def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "name": "Test User", "password": "testpass123"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert "password" not in response.json()  # Ensure password is not returned

def test_get_user(client: TestClient):
    # First create a user
    create_response = client.post(
        "/users/",
        json={"email": "test2@example.com", "name": "Test User 2", "password": "testpass123"}
    )
    user_id = create_response.json()["id"]
    
    # Then get the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_user_not_found(client: TestClient):
    response = client.get("/users/999999")
    assert response.status_code == 404

# Authentication testing
@pytest.fixture
def auth_headers(client: TestClient):
    # Create user and get token
    client.post(
        "/users/",
        json={"email": "auth@example.com", "name": "Auth User", "password": "testpass123"}
    )
    
    login_response = client.post(
        "/token",
        data={"username": "auth@example.com", "password": "testpass123"}
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_protected_endpoint(client: TestClient, auth_headers):
    response = client.get("/protected", headers=auth_headers)
    assert response.status_code == 200

def test_protected_endpoint_without_auth(client: TestClient):
    response = client.get("/protected")
    assert response.status_code == 401

# Database testing with fixtures
@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def sample_user(db_session):
    user = User(email="sample@example.com", hashed_password="hashedpass")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def test_user_crud_operations(db_session, sample_user):
    # Test user exists
    assert sample_user.id is not None
    
    # Test update
    sample_user.name = "Updated Name"
    db_session.commit()
    
    updated_user = db_session.query(User).filter(User.id == sample_user.id).first()
    assert updated_user.name == "Updated Name"
    
    # Test delete
    db_session.delete(sample_user)
    db_session.commit()
    
    deleted_user = db_session.query(User).filter(User.id == sample_user.id).first()
    assert deleted_user is None

# Mock external services
@pytest.fixture
def mock_email_service(monkeypatch):
    def mock_send_email(*args, **kwargs):
        return {"status": "sent", "message_id": "mock123"}
    
    monkeypatch.setattr("app.services.email.send_email", mock_send_email)

def test_send_notification(client: TestClient, mock_email_service):
    response = client.post("/send-notification/", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert "notification will be sent" in response.json()["message"].lower()

# File upload testing
def test_file_upload(client: TestClient):
    # Create a test file
    test_file_content = b"test file content"
    
    response = client.post(
        "/upload-file/",
        files={"file": ("test.txt", test_file_content, "text/plain")}
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"

def test_file_upload_invalid_type(client: TestClient):
    response = client.post(
        "/upload-file/",
        files={"file": ("test.exe", b"executable content", "application/x-msdownload")}
    )
    assert response.status_code == 400

# WebSocket testing
@pytest.mark.asyncio
async def test_websocket():
    with TestClient(app).websocket_connect("/ws/123") as websocket:
        websocket.send_text("Hello WebSocket")
        data = websocket.receive_text()
        assert "Hello" in data

# Performance testing
def test_endpoint_performance(client: TestClient):
    import time
    
    start_time = time.time()
    response = client.get("/users/")
    end_time = time.time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 1.0  # Should respond within 1 second

# Parametrized testing
@pytest.mark.parametrize("email,expected_status", [
    ("valid@example.com", 201),
    ("invalid-email", 422),
    ("", 422),
    ("a" * 100 + "@example.com", 422),  # Too long
])
def test_user_creation_validation(client: TestClient, email, expected_status):
    response = client.post(
        "/users/",
        json={"email": email, "name": "Test User", "password": "testpass123"}
    )
    assert response.status_code == expected_status

# Integration testing
@pytest.fixture(scope="session")
def docker_compose():
    """Start docker-compose services for integration tests"""
    import subprocess
    
    subprocess.run(["docker-compose", "-f", "docker-compose.test.yml", "up", "-d"])
    yield
    subprocess.run(["docker-compose", "-f", "docker-compose.test.yml", "down"])

def test_database_integration(docker_compose, client: TestClient):
    """Test with real database"""
    response = client.post(
        "/users/",
        json={"email": "integration@example.com", "name": "Integration Test", "password": "testpass123"}
    )
    assert response.status_code == 201

# Load testing setup
def test_concurrent_requests():
    """Test handling of concurrent requests"""
    import concurrent.futures
    import threading
    
    def make_request():
        with TestClient(app) as client:
            return client.get("/users/")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(50)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    # All requests should succeed
    assert all(result.status_code == 200 for result in results)
```

### Q20: How do you test authentication and authorization?

**Answer:**
```python
import pytest
from jose import jwt
from datetime import datetime, timedelta
from app.core.security import create_access_token, verify_token

# JWT token testing
class TestJWTAuthentication:
    def test_create_valid_token(self):
        user_data = {"sub": "testuser", "role": "user"}
        token = create_access_token(user_data)
        
        # Decode and verify token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "testuser"
        assert decoded["role"] == "user"
        assert "exp" in decoded
    
    def test_token_expiration(self):
        user_data = {"sub": "testuser"}
        # Create token that expires in 1 second
        token = create_access_token(user_data, expires_delta=timedelta(seconds=1))
        
        # Token should be valid immediately
        assert verify_token(token) is not None
        
        # Wait for expiration
        import time
        time.sleep(2)
        
        # Token should be expired
        assert verify_token(token) is None
    
    def test_invalid_token(self):
        invalid_token = "invalid.token.here"
        assert verify_token(invalid_token) is None

# Role-based access testing
class TestRoleBasedAccess:
    @pytest.fixture
    def admin_token(self, client):
        # Create admin user
        client.post("/users/", json={
            "email": "admin@example.com",
            "password": "adminpass123",
            "role": "admin"
        })
        
        response = client.post("/token", data={
            "username": "admin@example.com",
            "password": "adminpass123"
        })
        return response.json()["access_token"]
    
    @pytest.fixture
    def user_token(self, client):
        # Create regular user
        client.post("/users/", json={
            "email": "user@example.com",
            "password": "userpass123",
            "role": "user"
        })
        
        response = client.post("/token", data={
            "username": "user@example.com",
            "password": "userpass123"
        })
        return response.json()["access_token"]
    
    def test_admin_access(self, client, admin_token):
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.delete("/admin/users/1", headers=headers)
        assert response.status_code in [200, 404]  # Should have access
    
    def test_user_denied_admin_access(self, client, user_token):
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.delete("/admin/users/1", headers=headers)
        assert response.status_code == 403
    
    def test_no_token_access_denied(self, client):
        response = client.delete("/admin/users/1")
        assert response.status_code == 401

# OAuth testing
class TestOAuthIntegration:
    @pytest.fixture
    def mock_oauth_response(self, monkeypatch):
        def mock_get_userinfo(token):
            return {
                "email": "oauth@example.com",
                "name": "OAuth User",
                "sub": "oauth123"
            }
        
        monkeypatch.setattr("app.auth.oauth.google.get_userinfo", mock_get_userinfo)
    
    def test_oauth_callback(self, client, mock_oauth_response):
        # Mock OAuth callback
        response = client.get("/auth/callback?code=mock_code&state=mock_state")
        assert response.status_code == 200
        assert "access_token" in response.json()

# Session testing
class TestSessionManagement:
    def test_session_invalidation(self, client):
        # Login
        login_response = client.post("/token", data={
            "username": "test@example.com",
            "password": "testpass123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Access protected resource
        response = client.get("/protected", headers=headers)
        assert response.status_code == 200
        
        # Logout (invalidate session)
        client.post("/logout", headers=headers)
        
        # Try to access protected resource again
        response = client.get("/protected", headers=headers)
        assert response.status_code == 401

# Permission testing
class TestPermissions:
    def test_resource_owner_access(self, client, auth_headers):
        # Create resource
        response = client.post("/items/", 
            json={"title": "My Item", "description": "Test item"},
            headers=auth_headers
        )
        item_id = response.json()["id"]
        
        # Owner should be able to access
        response = client.get(f"/items/{item_id}", headers=auth_headers)
        assert response.status_code == 200
        
        # Owner should be able to update
        response = client.put(f"/items/{item_id}",
            json={"title": "Updated Item"},
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_non_owner_access_denied(self, client, auth_headers):
        # Create item with different user
        other_headers = self.create_user_and_get_headers(client, "other@example.com")
        response = client.post("/items/",
            json={"title": "Other's Item"},
            headers=other_headers
        )
        item_id = response.json()["id"]
        
        # Current user should not be able to access
        response = client.get(f"/items/{item_id}", headers=auth_headers)
        assert response.status_code == 403
    
    def create_user_and_get_headers(self, client, email):
        client.post("/users/", json={
            "email": email,
            "password": "testpass123"
        })
        
        login_response = client.post("/token", data={
            "username": email,
            "password": "testpass123"
        })
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
```

---

## Deployment & Production

### Q21: How do you deploy FastAPI applications in production?

**Answer:**
```python
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker-compose.yml for production
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    restart: unless-stopped
    
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=myapp
      -