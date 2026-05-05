from fastapi import APIRouter, HTTPException, Depends, status
from pymongo.errors import ServerSelectionTimeoutError

from pydantic import BaseModel, EmailStr
from typing import Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os
from app.database import users_collection
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-fakeshield-key-for-project")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

class UserSignup(BaseModel):
    fullName: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class OAuthLogin(BaseModel):
    provider: str
    email: EmailStr
    name: str
    profile_pic: Optional[str] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_subscription_tier(email: str):
    paid_emails = ["virdisaab419@gmail.com", "virdiakash77@gmail.com"]
    return "paid" if email.lower() in paid_emails else "free"

@router.post("/signup")
async def signup(user: UserSignup):
    # Check if user exists
    try:
        existing_user = await users_collection.find_one({"email": user.email})
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Database connection timeout. Please ensure your IP is whitelisted in MongoDB Atlas."
        )
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    tier = get_subscription_tier(user.email)
    
    user_dict = {
        "fullName": user.fullName,
        "email": user.email,
        "password": hashed_password,
        "auth_provider": "local",
        "subscription_tier": tier,
        "created_at": datetime.utcnow()
    }
    
    await users_collection.insert_one(user_dict)
    
    # Generate token
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "user": {
            "name": user.fullName, 
            "email": user.email,
            "subscription_tier": tier
        }
    }

@router.post("/login")
async def login(user: UserLogin):
    try:
        db_user = await users_collection.find_one({"email": user.email})
    except Exception as e:
        # DB offline — issue an offline JWT so the user can still use the app
        print(f"[AUTH] DB offline during login: {e}. Issuing offline token.", flush=True)
        tier = get_subscription_tier(user.email)
        access_token = create_access_token(data={"sub": user.email})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "name": user.email.split("@")[0].title(),
                "email": user.email,
                "subscription_tier": "paid"  # Grant full access in offline mode
            }
        }

    if not db_user or db_user.get("auth_provider") != "local":
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    # Ensure tier is present (migration/legacy fix)
    tier = db_user.get("subscription_tier")
    if not tier:
        tier = get_subscription_tier(db_user["email"])
        try:
            await users_collection.update_one({"_id": db_user["_id"]}, {"$set": {"subscription_tier": tier}})
        except:
            pass

    access_token = create_access_token(data={"sub": db_user["email"]})
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "user": {
            "name": db_user["fullName"], 
            "email": db_user["email"],
            "subscription_tier": tier
        }
    }

@router.post("/oauth")
async def oauth_login(oauth_data: OAuthLogin):
    """
    Mock OAuth endpoint for Github/Google. 
    """
    db_user = await users_collection.find_one({"email": oauth_data.email})
    
    if not db_user:
        # Auto-signup OAuth users
        tier = get_subscription_tier(oauth_data.email)
        user_dict = {
            "fullName": oauth_data.name,
            "email": oauth_data.email,
            "auth_provider": oauth_data.provider,
            "profile_pic": oauth_data.profile_pic,
            "subscription_tier": tier,
            "created_at": datetime.utcnow()
        }
        await users_collection.insert_one(user_dict)
        db_user = user_dict
    else:
        # Update tier if missing
        if "subscription_tier" not in db_user:
            tier = get_subscription_tier(db_user["email"])
            await users_collection.update_one({"_id": db_user["_id"]}, {"$set": {"subscription_tier": tier}})
            db_user["subscription_tier"] = tier
        
    access_token = create_access_token(data={"sub": db_user["email"]})
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "user": {
            "name": db_user["fullName"], 
            "email": db_user["email"], 
            "profile_pic": db_user.get("profile_pic"),
            "subscription_tier": db_user.get("subscription_tier", "free")
        }
    }

@router.post("/upgrade")
async def upgrade_subscription(email: str):
    """Manual upgrade endpoint (to be called after QR payment confirmation)"""
    result = await users_collection.update_one(
        {"email": email},
        {"$set": {"subscription_tier": "paid"}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Subscription upgraded successfully"}

@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    return {
        "name": user.get("fullName"),
        "email": user.get("email"),
        "subscription_tier": user.get("subscription_tier", "free"),
        "profile_pic": user.get("profile_pic")
    }

@router.get("/test")
async def auth_test():
    return {"message": "Auth router is reachable!"}
