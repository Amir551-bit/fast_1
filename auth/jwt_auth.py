from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.users.models import UserModel, TokenModel
from core.core.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from core.core.config import settings


security = HTTPBearer(scheme_name="Token")     # مرورگر رو وادار کن پنجرهٔ اسم و رمز باز کنه،


def get_current_user(
        credentials : HTTPAuthorizationCredentials = Depends(security),    
        db : Session = Depends(get_db)
):
    
    return None



def generate_acces_token(user_id : int, expire_in : int = 60 * 5)-> str:

    now = datetime.utcnow()
    payload = {
        "type" : "access",
        "user_id" : user_id,
        "iat" : now,
        "exp" : now + timedelta(seconds=expire_in)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm ="HS256")




def generate_refresh_token(user_id : int, expire_in : int = 3600* 24)-> str:

    now = datetime.utcnow()
    payload = {
        "type" : "refresh",
        "user_id" : user_id,
        "iat" : now,
        "exp" : now + timedelta(seconds=expire_in)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm ="HS256")

