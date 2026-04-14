from sqlalchemy import Column, String, Text, Boolean, func, Integer, DateTime, ForeignKey
from core.core.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
import secrets


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# شماس میگه که خوب از الکوریتم بیسیپت استفاده کنه و اگر منقضی شد دیکه خودت میدونی که باید چکار کنی و چی بجاش بزاری در همین حد و تمام 


class UserModel(Base):
    __tablename__= "users"


    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False)
    password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)


    created_date = Column(DateTime, server_default=func.now())
    update_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    

    task = relationship("TaskModel", back_populates="user")     #   در کد پایتون بهت خود آبجکت user رو میده
    
    

#     دانشجو و درس:

# ForeignKey = شماره دانشجو
# relationship = خود دانشجو

##    و اینم بدون که فارن کی و ریلیشن شیب باید با هم باشن همین و تمام
##     این ریلیشن شیب خوب میاد و خود اون ابجکت یعنی خود یوزر رو میده ولی فارن کی فقط میاد اون عدده که برای یوزر ای دی باشه رو نشونمون میده همین و تمام 


    def hash_password(self, plain_password : str)->str:
        """Hashes the given password using bcrypt"""
        return pwd_context.hash(plain_password)
    

    def verify_password(self, plain_password : str)->bool:
        """verifies the given password againts the sorted hash."""
        return pwd_context.verify(plain_password, self.password)                   # این وری فایر که هست خوب ببین حفظی هست بدون دستور این بررسی رو داره که ببین 
                                                                  # این که هش کرده با این که ما وارد کردیم مثل هم هستن درستع یا نه همین 


    
    def set_password(self, plain_text)->None:
        self.password = self.hash_password(plain_text)


   

    def create_api_key():
        return secrets.token_hex(32)  # یه کلید تصادفی قوی




# user = UserModel(
#     username="ali",
# )

# user.password = user.hash_password("123456")

# db.add(user)
# db.commit()


class TokenModel(Base):
    __tablename__="tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), name="fk_users_token")
    token = Column(String, nullable=True, unique=True)

    created_date = Column(DateTime, server_default=func.now())

    user = relationship("UserModel", uselist=False)
    