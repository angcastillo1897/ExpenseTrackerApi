# from datetime import datetime, timedelta
# from jose import jwt

# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# REFRESH_TOKEN_EXPIRE_DAYS = 7

# def create_access_token(data: dict):
#    to_encode = data.copy()
#    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#    to_encode.update({"exp": expire})
#    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def create_refresh_token(data: dict):
#    to_encode = data.copy()
#    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
#    to_encode.update({"exp": expire})
#    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ...existing code...
# from .utils import create_access_token, create_refresh_token

# async def register_user(db: AsyncSession, user: schemas.UserCreate):
#    db_user = await repository.get_user_by_email(db, email=user.email)
#    if db_user:
#        raise BadRequestException("Email already registered")
#    hashed_password = bcrypt_context.hash(user.password)
#    db_user = await repository.create_user(db, user, hashed_password)
#    user_read = schemas.UserRead.model_validate(db_user)
#    access_token = create_access_token({"sub": str(db_user.id)})
#    refresh_token = create_refresh_token({"sub": str(db_user.id)})
#    return schemas.RegisterResponse(
#        user=user_read,
#        access_token=access_token,
#        refresh_token=refresh_token,
#    )


# @router.post("/", response_model=schemas.RegisterResponse, status_code=status.HTTP_201_CREATED)
# async def register_user(user: schemas.UserCreate, db: AsyncSessionDepends):
#    return await service.register_user(db, user)
