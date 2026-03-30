from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.users.models import UserModel, TokenModel
from core.core.database import get_db
from sqlalchemy.orm import Session


security = HTTPBearer(scheme_name="Token")     # مرورگر رو وادار کن پنجرهٔ اسم و رمز باز کنه،


def get_current_user(
        credentials : HTTPAuthorizationCredentials = Depends(security),    
        db : Session = Depends(get_db)
):
    
    token_obj = db.query(TokenModel).filter_by(token=credentials.credentials).first()  # ببین منظور از کردنتیالز دومی خوب اینکه بیا توکن رو بگیر همین 
    if not token_obj:                          # مقدار توکنی که کاربر فرستاده همین 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credentials are not provided",
        )
    
    return token_obj.user


