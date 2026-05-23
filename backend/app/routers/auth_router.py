from fastapi import APIRouter, HTTPException, Depends, status
from pymongo.errors import ServerSelectionTimeoutError

from pydantic import BaseModel, EmailStr
from typing import Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os
import httpx
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
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    profile_pic: Optional[str] = None
    code: Optional[str] = None

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
    OAuth endpoint for Github/Google. 
    In production, this verifies the code with the provider.
    """
    email = oauth_data.email
    name = oauth_data.name
    profile_pic = oauth_data.profile_pic

    # 1. Handle Real GitHub Auth
    if oauth_data.provider.lower() == "github" and oauth_data.code:
        async with httpx.AsyncClient() as client:
            # Exchange code for access token
            token_res = await client.post(
                "https://github.com/login/oauth/access_token",
                params={
                    "client_id": os.getenv("GITHUB_CLIENT_ID"),
                    "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
                    "code": oauth_data.code
                },
                headers={"Accept": "application/json"}
            )
            token_data = token_res.json()
            access_token = token_data.get("access_token")
            
            if not access_token:
                raise HTTPException(status_code=400, detail="Failed to verify GitHub code")

            # Get User Profile
            user_res = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            github_user = user_res.json()
            name = github_user.get("name") or github_user.get("login")
            profile_pic = github_user.get("avatar_url")
            
            # Get Primary Email (often private in Profile)
            email_res = await client.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            emails = email_res.json()
            email = next((e["email"] for e in emails if e["primary"]), None)
            
            if not email:
                raise HTTPException(status_code=400, detail="No public/primary email found on GitHub")

    # 2. Proceed with user lookup/creation
    if not email:
        raise HTTPException(status_code=400, detail="Email is required for OAuth login")

    db_user = await users_collection.find_one({"email": email})
    
    if not db_user:
        # Auto-signup OAuth users
        tier = get_subscription_tier(email)
        user_dict = {
            "fullName": name or email.split("@")[0],
            "email": email,
            "auth_provider": oauth_data.provider,
            "profile_pic": profile_pic,
            "subscription_tier": tier,
            "created_at": datetime.utcnow()
        }
        await users_collection.insert_one(user_dict)
        db_user = user_dict
    else:
        # Update profile info if changed
        update_data = {"auth_provider": oauth_data.provider}
        if profile_pic: update_data["profile_pic"] = profile_pic
        
        # Update tier if missing
        if "subscription_tier" not in db_user:
            update_data["subscription_tier"] = get_subscription_tier(db_user["email"])
            
        await users_collection.update_one({"_id": db_user["_id"]}, {"$set": update_data})
        db_user.update(update_data)
        
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
