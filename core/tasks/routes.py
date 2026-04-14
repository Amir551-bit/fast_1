from fastapi import APIRouter, Path, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from core.tasks.schemas import *
from core.tasks.models import TaskModel
from core.users.models import UserModel
from sqlalchemy.orm import Session
from core.core.database import get_db
from auth.jwt_auth import get_current_user
from typing import List

router = APIRouter(tags=["tasks"], prefix="/todo")


@router.get("/tasks", response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(
    completed : bool = Query(None, description="filter tasks based on being completed or not"),
    limit : int = Query(10, gt=0, le=50, description="limiting the number of items to retrieve"),
    offset : int = Query(0, ge=0, description="use for paginating based on passsed items"),        # این که گذاشته نان خوب برای اینکه یعنی کاربر اصلا میتونه چیزی وارد نکنه 
    db : Session = Depends(get_db), 
    user : UserModel = Depends(get_current_user)):


    query = db.query(TaskModel).filter_by(user_id=user.id).first()                                                                # بزنه فالس فقط اونایی که فالس هست رو نشون میده و بزنه ترو اونایی که ترو هست فقط نشون میده 
    if completed is not None:

        query = query.filter_by(is_completed=completed)

    return query.limit(limit).offset(offset).all() 





@router.get("/tasks/{task_id}", response_model=TaskResponseSchema)
async def retrieve_tasks_details(task_id:int = Path(..., gt=0),
                                 db : Session = Depends(get_db),
                                 user : UserModel = Depends(get_current_user)):
    task_obj = db.query(TaskModel).filter_by(user_id=user.id, id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found") 
    return task_obj





@router.post("/tasks", response_model=TaskResponseSchema)
async def create_task(request:TaskCreateSchema,  db : Session = Depends(get_db),
                      user : UserModel = Depends(get_current_user)):
    
    data = request.model_dump()
    data.update({"user_id": user.id})                                     # ببین حالا این ریکواست خوب همون یک شی از تسک کریت شما است
    task_obj = TaskModel(**data)        # از دیکشنری باید در بیاد چون برای دیتابیس دیکشنری لازم نیس اصن
    db.add(task_obj)
    db.commit()           # چون میخواد یه شی از تسک مدل بشه باید از دیکشنری در بیاد دیکه همین 
    db.refresh(task_obj)

    return task_obj



    # task = TaskModel(
    #     title=request.title,
    #     description=request.description,
    #     is_completed=request.is_completed
    # )






@router.put("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(request:TaskUpdateSchema,
                      task_id : int = Path(..., gt=0),
                      db : Session = Depends(get_db),
                      user : UserModel = Depends(get_current_user)):
    task_obj = db.query(TaskModel).filter_by(user_id=user.id,id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found") 
    


    for field, value in request.model_dump(exclude_unset=True).items(): 
        setattr(task_obj, field, value)                                    # task_obj.field =  value       قشنگ معادل همین هست 

    db.commit()
    db.refresh(task_obj)


    return task_obj
 





@router.delete("/tasks/{task_id}", response_model=list[TaskResponseSchema])
async def delete_user(task_id : int = Path(..., gt=0),
                      db : Session = Depends(get_db),
                      user : UserModel = Depends(get_current_user)):
    task_obj = db.query(TaskModel).filter_by(user_id=user.id,id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_obj)
    db.commit()
    return JSONResponse(content="Task Removed Succesfully",status_code=200)






#چون ببین میدونی که شماس منظور فایل شماس خوب میدونی که به دیکشنری داده نمیده پس ما باید برای اینکه میخواهیم به فست ای پی ای بدیم 
# باید بیاییم اول خوب به به دیکشنری کنیم که فست ای پی ای بگیره و بعد دوباره جالا میخواهیم به دیتابیس بدیم از دیکشنری در بیاد همین 
# ببین نسبت به خط اول که برات نوشتم جون ریکواست شد یه شی از اون خوب دیکه از جالت دیکشنری در میاد فهمیدی بخاطر همینه وگرنه فست خودش
# همرو به دیکشنری تبدیل میکنه در همین حد 