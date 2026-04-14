from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.users.models import UserModel, TokenModel
from core.core.database import get_db
from sqlalchemy.orm import Session


security = HTTPBearer(scheme_name="Token")     # مرورگر رو وادار کن پنجرهٔ اسم و رمز باز کنه،      HTTPBearer = نگهبان در ورودی که میگه "توکن داری؟ بده ببینم"


def get_current_user(
        credentials : HTTPAuthorizationCredentials = Depends(security),    
        db : Session = Depends(get_db)
):
    
    token_obj = db.query(TokenModel).filter_by(token=credentials.credentials).first()  # ببین منظور از کردنتیالز دومی خوب اینکه بیا توکن رو بگیر همین 
    if not token_obj:                          # مقدار توکنی که کاربر فرستاده همین 
        raise HTTPException(                                    #   یا همون یک فرم اماده هست 
            status_code=status.HTTP_401_UNAUTHORIZED,               #   منظور از کرن دن تیالز دومی همون توکن هست 
            detail="credentials are not provided",
        )
    
    return token_obj.user                                 ##  این یوزر معنی یعنی همین ریلیشن شیب هستش خوب فهمیدی در همین حد و تمام اون یوز که مربوط به این توکن هست رو بده همین و تمام 


#      HTTPAuthorizationCredentials = یک آبجکت که اطلاعات داخل Authorization header رو تمیز جدا کرده و بهت میده

##   همین که پایین بهت گفتم 

##  credentials.scheme        # نوع (مثلاً Bearer)
##  credentials.credentials   # HTTPAuthorizationCredentials این دوتا هستش   خود توکن         داخل 


# HTTPAuthorizationCredentials(
#     scheme="Bearer",                      اینم مثالش                           منظور از شما خوب همین نوع احراز هست که توکن هست 
#     credentials="abc123"
# )



# credentials.scheme = "Bearer"        این نوعش 
# credentials.credentials = "abc123"     اینم رمزش



##    Bearer = نوع مدرک (توکن)   که همون منظور احراز هویت توکن هستش 
##   abc123 =  این یعنی همون توکن  خود مدرک   

##    Authorization     این بخشی از هدر هستش که خوب که این در بخش هدر به منظور مجوز دسترسی هستش همین و تمام 

##