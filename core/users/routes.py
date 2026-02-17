from fastapi import APIRouter, Path, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from core.users.schemas import *
from core.users.models import UserModel
from sqlalchemy.orm import Session
from core.core.database import get_db
from typing import List


router = APIRouter(tags=["users"], prefix="/users")

 


@router.post("/login")
async def user_login(request:UserLoginSchema, db : Session = Depends(get_db)):
    return {}




@router.post("/register")
async def user_register(request:UserRegisterSchema, db : Session = Depends(get_db)):
    return {}