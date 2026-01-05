import os
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 50

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
