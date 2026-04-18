from fastapi import FastAPI, Depends, Request, Response, BackgroundTasks
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from core.tasks.routes import router as tasks_routes 
from core.core.database import Base, engine
from core.tasks.models import TaskModel
from core.users.routes import router as users_routes
from core.users.models import UserModel
from auth.token_auth import get_current_user
import time, random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger



scheduler = AsyncIOScheduler()


def my_task():
    print(f"Task executed at {time.strftime('%Y-%m-%d %H:%M:%S')}")


tags_metadata = [
    {
        "name" : "tasks",
        "description" : "operation related to task management",
        "enternalDocs" : {
            "description" : "more about tasks",
            "url" : "https://example.com/docs/tasks"
        }
    }
]




@asynccontextmanager
async def welcome(FastAPI):
    print("Application startup")
    scheduler.add_job(my_task, trigger=IntervalTrigger(seconds=10))
    scheduler.start()
    yield
    scheduler.shutdown()
    print("Application shutdown")







app = FastAPI(
    title="Todo Application",
    description="this is a section for description",
    version="0.0.1",
    terms_of_services="https://example.com/terms/",
    contact={
        "name":"Ali bigdeli",
        "url" : "https:/thealibigdeli.ir",
        "email" : "bigdeli.ali3@gmail.com"
    }
    ,lifespan=welcome, openapi_tags=tags_metadata)


Base.metadata.create_all(bind=engine)


app.include_router(tasks_routes)
app.include_router(users_routes)



# from auth.basic_auth import get_current_username
# from fastapi.security import APIKeyHeader , APIKeyQuery     # APIKeyquery   هیح فرقی با هدر نداره کوئری همین

# header_schema = APIKeyHeader(name="x-key")    # مهر شرکت روی اون بلیط ها هست 




@app.get("/public")
def public_route():
    return {"Message" : "this is a public route"}



# @app.get("/private")
# def private_route(api_key = Depends(header_schema)):          ول
#     return {"Message" : "this is a private route"}



# @app.get("/private")
# def private_route(user:UserModel = Depends(get_current_username)):       ول
#     print(user)
#     return {"Message" : "this is a private route"}



# from auth.token_auth import get_current_user

                                                                    #1
# @app.get("/private")
# def private_route(user = Depends(get_current_user)):
#     print(user)
#     return {"Message" : "this is a private route"}



from auth.jwt_auth import get_current_user


@app.get("/private")
def private_route(user = Depends(get_current_user)):
    print(user.id)
    return {"Message" : "this is a private route"}





# @app.get("/private")
# def private_route(user = Depends(get_current_user)):
#     return user





@app.post("/set-cookie")
def set_cookie(response:Response):
    response.set_cookie(key="test", value="somethings") 
    return {"message" : "Cookie has been set succesfully"}                         #  با کوکی خوب میشه  قشنک لاگین رو هم اوکی کرد همین بعدن با هوش مصنوعی بزن یاد بده 



@app.get("/get-cookie")
def get_cookie(request:Request):
    print(request.cookies.get("test")) 
    return {"message" : "Cookie has been set succesfully"}




#  modheader    برای اینکه خوب اون توکن هر بار هی وارد  نکنی اون بالا اونو میزاری
# Authorization: Bearer YOUR_TOKEN




@app.middleware("http")
async def add_process_time_header(request: Request, call_next):          
    start_time = time.perf_counter()

    response = await call_next(request)           #  انگار میگه این ریکواست رو انجام بده و برو بعدی جالا مرحله بعد 
    
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# خلاصه طلایی:
# call_next یک پل است.

# وقتی صداش می‌زنی، یعنی: «درخواست رو ببر جلو، جواب رو برام بیار».

# وقتی جواب رو آورد، تو می‌تونی قبل از اینکه جواب رو به کاربر بدی، یک نگاهی بهش بندازی یا تغییرش بدی.

# الان متوجه شدی که چرا بدون call_next کدهای اصلی تو اصلاً اجرا نمی‌شن؟


#   Black       یه چیزی مثل المبیک در ترمینال میزنی و میتونی باهاش کد هارو مرتب کنی فقط دستور رو بزنی خودش برات مرتب میکنه همین و تمام و به چیزی هم نیازی نداره 



@app.get("/")
def get_Hello():
    return {"Message" : "Hello World"}



task_counter = 1


def start_task(task_id):
    print("start task")
    print(f"doing the process : {task_id}")
    time.sleep(random.randint(3,10))
    print(f"finished task {task_id}")




@app.get("/initiate-task", status_code=200)
async def initiate_task(background_tasks: BackgroundTasks):
    global task_counter
    background_tasks.add_task(start_task, task_id=task_counter)
    task_counter += 1
    return JSONResponse(content={"detail":"task is done"})









from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
# from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache 


cache_backend = InMemoryBackend()
FastAPICache.init(cache_backend)


