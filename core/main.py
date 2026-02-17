from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.tasks.routes import router as tasks_routes 
from core.core.database import Base, engine
from core.tasks.models import TaskModel
from core.users.routes import router as users_routes



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
    yield
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



@app.get("/salam")
def get_Hello():

    return {"Message" : "Hello world"}