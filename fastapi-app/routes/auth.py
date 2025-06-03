from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import hashlib
import csv
import os
from itsdangerous import TimestampSigner

router = APIRouter()

# Shared secret key
SECRET_KEY = "your_super_secret_key"
signer = TimestampSigner(SECRET_KEY)

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "database")
USER_DB = os.path.join(DB_DIR, "users.csv")
ADMIN_DB = os.path.join(DB_DIR, "admins.csv")

# Create directories if not exist
os.makedirs(DB_DIR, exist_ok=True)

# Request Models
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: str  # 'user' or 'admin'

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: str

# Password hashing
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

# REGISTER USER
@router.post("/user/register")  # Route for user registration
def register_user(req: RegisterRequest):
    db_file = USER_DB

    if user_exists(req.email, db_file):
        raise HTTPException(status_code=400, detail="User already exists")

    file_exists = os.path.exists(db_file)
    with open(db_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["email", "password"])
        writer.writerow([req.email, hash_password(req.password)])

    return {"message": "User registered successfully"}

# REGISTER ADMIN
@router.post("/admin/register")  # Route for admin registration
def register_admin(req: RegisterRequest):
    db_file = ADMIN_DB

    if user_exists(req.email, db_file):
        raise HTTPException(status_code=400, detail="Admin already exists")

    file_exists = os.path.exists(db_file)
    with open(db_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["email", "password"])
        writer.writerow([req.email, hash_password(req.password)])

    return {"message": "Admin registered successfully"}

# LOGIN USER
@router.post("/user/login")  # Login for users
def login_user(req: LoginRequest):
    db_file = USER_DB

    user = get_user(req.email, db_file)
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = signer.sign(f"{req.email}:{req.role}".encode()).decode()
    return {"access_token": token, "token_type": "bearer", "role": req.role}

# LOGIN ADMIN
@router.post("/admin/login")  # Login for admins
def login_admin(req: LoginRequest):
    db_file = ADMIN_DB

    user = get_user(req.email, db_file)
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = signer.sign(f"{req.email}:{req.role}".encode()).decode()
    return {"access_token": token, "token_type": "bearer", "role": req.role}

# Check if user exists
def user_exists(email: str, db_file: str) -> bool:
    try:
        with open(db_file, "r") as f:
            reader = csv.DictReader(f)
            return any(row["email"] == email for row in reader)
    except FileNotFoundError:
        return False

# Get user data
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
