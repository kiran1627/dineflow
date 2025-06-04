from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import hashlib
import csv
import os
from itsdangerous import TimestampSigner

router = APIRouter()

SECRET_KEY = "your_super_secret_key"
signer = TimestampSigner(SECRET_KEY)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "database")
USER_DB = os.path.join(DB_DIR, "users.csv")
ADMIN_DB = os.path.join(DB_DIR, "admins.csv")

os.makedirs(DB_DIR, exist_ok=True)

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def user_exists(email: str, db_file: str) -> bool:
    try:
        with open(db_file, "r") as f:
            reader = csv.DictReader(f)
            return any(row["email"] == email for row in reader)
    except FileNotFoundError:
        return False

def get_user(email: str, db_file: str):
    try:
        with open(db_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["email"] == email:
                    return {"email": row["email"], "password": row["password"]}
        return None
    except FileNotFoundError:
        return None

@router.post("/user/register")
def register_user(req: RegisterRequest):
    if user_exists(req.email, USER_DB):
        raise HTTPException(status_code=400, detail="User already exists")

    file_exists = os.path.exists(USER_DB)
    with open(USER_DB, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["email", "password"])
        writer.writerow([req.email, hash_password(req.password)])

    return {"message": "User registered successfully"}

@router.post("/admin/register")
def register_admin(req: RegisterRequest):
    if user_exists(req.email, ADMIN_DB):
        raise HTTPException(status_code=400, detail="Admin already exists")

    file_exists = os.path.exists(ADMIN_DB)
    with open(ADMIN_DB, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["email", "password"])
        writer.writerow([req.email, hash_password(req.password)])

    return {"message": "Admin registered successfully"}

@router.post("/user/login")
def login_user(req: LoginRequest):
    user = get_user(req.email, USER_DB)
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = signer.sign(f"{req.email}:user".encode()).decode()
    return {"access_token": token, "token_type": "bearer", "role": "user"}

@router.post("/admin/login")
def login_admin(req: LoginRequest):
    user = get_user(req.email, ADMIN_DB)
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = signer.sign(f"{req.email}:admin".encode()).decode()
    return {"access_token": token, "token_type": "bearer", "role": "admin"}
