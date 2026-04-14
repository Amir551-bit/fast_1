from fastapi import APIRouter, Path, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from core.users.schemas import *
from core.users.models import UserModel, TokenModel
from sqlalchemy.orm import Session
from core.core.database import get_db
from typing import List
import secrets
from auth.jwt_auth import generate_acces_token, generate_refresh_token, decode_refresh_token


router = APIRouter(tags=["users"], prefix="/users")



def generate_token(length=32):
    """Generate a secure rendom token as a string"""
    return secrets.token_hex(length)



@router.post("/login")
async def user_login(request:UserLoginSchema, db : Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=request.username).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user doesnt exists")
    if not user_obj.hash_password(request.password): #رمز عبور فرستاده شده الان رو با هش ذخیره شده در دیتابیس مقایسه میکنه همین 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password is invalid")
    

    access_token = generate_acces_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)



    # token_obj = TokenModel(user_id = user_obj.id, token = generate_token())
    # if not token_obj:
    #     print('the token is exists')
    # db.add(token_obj)
    # db.commit()
    # db.refresh(token_obj)

    return JSONResponse(content={"details":"logged is succesfully", "access_token":access_token, "refresh_token" : refresh_token})

    # return token_obj




@router.post("/register") 
async def user_register(request:UserRegisterSchema, db : Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=request.username.lower()).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists")
    user_obj = UserModel(username=request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    return JSONResponse(content={"detail":"user registed succesfully"})





@router.post("/refresh-token") 
async def user_refresh_token(request:UserRefreshSchema, db : Session = Depends(get_db)):

    user_id = decode_refresh_token(request.refresh_token)
    acces_token = generate_acces_token(user_id)
    return JSONResponse(content={"acces_token":acces_token})