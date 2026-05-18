from fastapi import Header, HTTPException, Depends
import jwt
import os
from app.database import users_collection

SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-fakeshield-key-for-project")
ALGORITHM = "HS256"

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        user = await users_collection.find_one({"email": email})
        if user is None:
            # Bypass for Offline Mode / Development
            print(f"[AUTH] User {email} not in DB. Granting Guest access.")
            return {
                "email": email, 
                "full_name": "Guest User", 
                "subscription_tier": "free",
                "is_offline": True
            }
        return user
    except Exception as e:
        print(f"[AUTH] DB Error during auth: {e}. Granting Guest access.")
        return {
            "email": "offline_user@fakeshield.local", 
            "full_name": "Offline Tester", 
            "subscription_tier": "paid", # Grant pro for testing
            "is_offline": True
        }

async def verify_paid_tier(user: dict = Depends(get_current_user)):
    if user.get("subscription_tier") != "paid":
        raise HTTPException(
            status_code=403, 
            detail="This feature requires a Pro subscription. Please upgrade to access."
        )
    return user
