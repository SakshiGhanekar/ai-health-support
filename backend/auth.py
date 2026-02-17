from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import os
import re
import logging
from dotenv import load_dotenv

from . import models, database, schemas

# -------------------------------------------------
# Logger
# -------------------------------------------------
logger = logging.getLogger(__name__)

load_dotenv()

# -------------------------------------------------
# Config
# -------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

# -------------------------------------------------
# Helpers
# -------------------------------------------------

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password[:72])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception

    return user


# -------------------------------------------------
# SIGNUP
# -------------------------------------------------

@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    if not re.match(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$", user.password):
        raise HTTPException(status_code=400, detail="Weak password")

    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username exists")

    hashed_password = get_password_hash(user.password)

    new_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        email=user.email,
        full_name=user.full_name,
        dob=user.dob
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -------------------------------------------------
# LOGIN
# -------------------------------------------------

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}


# -------------------------------------------------
# PROFILE GET
# -------------------------------------------------

@router.get("/profile")
def get_user_profile(current_user: models.User = Depends(get_current_user)):

    return {
        "username": current_user.username or "",
        "email": current_user.email or "",
        "full_name": current_user.full_name or "",
        "gender": current_user.gender or "",
        "dob": current_user.dob.strftime("%Y-%m-%d") if current_user.dob else "",
        "height": current_user.height or "",
        "weight": current_user.weight or ""
    }


# -------------------------------------------------
# PROFILE UPDATE (🔥 FIXED VERSION)
# -------------------------------------------------

@router.put("/profile")
def update_profile(
    profile: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):

    try:

        if "full_name" in profile:
            current_user.full_name = profile["full_name"]

        if "dob" in profile:
            try:
                current_user.dob = datetime.strptime(
                    str(profile["dob"]).replace("/", "-"),
                    "%Y-%m-%d"
                ).date()
            except:
                pass

        if "gender" in profile:
            current_user.gender = profile["gender"]

        if "height" in profile:
            current_user.height = profile["height"]

        if "weight" in profile:
            current_user.weight = profile["weight"]

        db.commit()
        db.refresh(current_user)

        return {"status": "success"}

    except Exception as e:
        db.rollback()
        logger.error(f"Profile update error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
