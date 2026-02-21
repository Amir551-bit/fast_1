from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from core.users.models import UserModel
from core.core.database import get_db
from sqlalchemy.orm import Session


security = HTTPBasic()      # مرورگر رو وادار کن پنجرهٔ اسم و رمز باز کنه،


def get_current_username(
        credentials : HTTPBasicCredentials = Depends(security),    # قبل از اینکه این تابع اجرا بشه این رو انجام بده بعد  دیپندز
        db : Session = Depends(get_db)
):
    
    user_obj = db.query(UserModel).filter_by(username=credentials.username).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorent username or password",
            headers={"www-Authenticate" : "Basic"},
        )
    
    if not user_obj.verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorent username or password",
            headers={"www-Authenticate" : "Basic"},
        )
    
    return user_obj


#  HTTPBasicCredentials 
# این یک قالب از فست ای پی ای هستش که میکه داده ای میخوام دریافت کنم که  فقط دو تا فیلد میخوام اونم اینکه نام کاربری و پسورد هستش همین 
# این یه فرم هستش که خوب همون نام کاربری و پسورد توش هست همین فهمیدی این منظور همون فرم هستش همین 




