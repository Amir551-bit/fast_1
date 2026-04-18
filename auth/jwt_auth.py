from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.users.models import UserModel, TokenModel
from core.core.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidSignatureError
from core.core.config import settings


security = HTTPBearer(scheme_name="Token")     # مرورگر رو وادار کن پنجرهٔ اسم و رمز باز کنه،


def get_current_user(
        credentials : HTTPAuthorizationCredentials = Depends(security),    
        db : Session = Depends(get_db)
):
    
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get("user_id",  None)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authcation failed, user id not found in token")
        
        if decoded.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authcation failed, token type not valid")
        
        if datetime.now() > datetime.fromtimestamp(decoded.get("exp")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authcation failed, token has expired")
        

        user_obj = db.query(UserModel).filter_by(id=user_id).first()
        return user_obj



    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authcation failed, invalid signature")
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authcation failed, decoded field")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Authcation failed, {e}")
    





def generate_acces_token(user_id : int, expire_in : int = 60 * 5)-> str:

    now = datetime.utcnow()        #  زمان الان به صورت جهانی 
    payload = {
        "type" : "access",
        "user_id" : user_id,                                   # payload چیه 
        "iat" : now,                                            # اطلاعاتی که داخل توکن ذخیره میکنیم 
        "exp" : now + timedelta(seconds=expire_in)  
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm ="HS256")          ## کل جریان user_id → payload → encode → token




def generate_refresh_token(user_id : int, expire_in : int = 3600* 24)-> str:

    now = datetime.utcnow()
    payload = {
        "type" : "refresh",
        "user_id" : user_id,
        "iat" : now,
        "exp" : now + timedelta(seconds=expire_in)          #  تایم دلتا خوب میاد اون مدت زمانی که ما بهش دادیم رو در یکجا دخیره میکنه و میره 
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm ="HS256")





def decode_refresh_token(token):
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get("user_id",  None)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authcation failed, user id not found in token")
        
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authcation failed, token type not valid")
        
        if datetime.now() > datetime.fromtimestamp(decoded.get("exp")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authcation failed, token has expired")
        

        return user_id



    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authcation failed, invalid signature")
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authcation failed, decoded field")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Authcation failed, {e}")