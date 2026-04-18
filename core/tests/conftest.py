
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from core.core.database import Base, create_engine, sessionmaker, get_db
from core.main import app
import pytest
from faker import Faker
from users.models import UserModel
from tasks.models import TaskModel


fake = Faker()


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#module
@pytest.fixture(scope="module")
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()




#module
@pytest.fixture(scope="module")
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db, None)



#session
@pytest.fixture(scope="session")
def tear_up_and_down_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)



#function
@pytest.fixture(scope="function")
def anon_client():
    client = TestClient(app)
    yield client





@pytest.fixture(scope="module", autoflush=True)
def generate_mock_data(db_session):
    user = UserModel(username="testuser")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    print(f"User created with username : {user.username}, and ID : {user.id}")


    tasks_list = []
    for _ in range(10):
        tasks_list.append(
            TaskModel(
                user_id=user.id,
                title=fake.sentence(nb_words=6),
                description=fake.text(),
                is_completed=fake.boolean()
            )
        )
    
    db_session.add_all(tasks_list)
    db_session.commit()
    print(f"added 10 tasks for user {user.id}") 