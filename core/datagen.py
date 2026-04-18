from core.database import Sessionmaker
from sqlalchemy.orm import Session
from users.models import UserModel
from tasks.models import TaskModel
from faker import Faker

fake = Faker()



def seed_users(db):
    user = UserModel(username=fake.user_name())
    user.set_password("12345678")
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"User created with username : {user.username}, and ID : {user.id}")
    return user



def seed_tasks(db, user, count=10):
    task_list = []
    for _ in range(count):
        task_list.append(
            TaskModel(
                user_id=user.id,
                title=fake.sentence(nb_words=5),
                description=fake.text(),
                is_completed=fake.boolean()
            )
        )

    db.add_all(task_list)
    db.commit()
    print(f"added 10 tasks for user {user.id}")


def main():
    
    db = Sessionmaker()
    try:
        user = seed_users(db)
        seed_tasks(db, user)
    finally:
        db.close()





if __name__ == "__main__":
    main()




#     ۱. مثال "میزِ کارِ نجار"
# تصور کن دیتابیس تو مثل یک انبار بزرگ پر از وسیله است. تو نمی‌تونی مستقیماً بری وسط انبار و همون‌جا شروع کنی به بریدن چوب یا ساختن صندلی؛ چون انبار شلوغه و قوانین خاص خودش رو داره.

# انبار (Database): محل ذخیره همیشگی داده‌ها.

# میز کار (The db object / Session): این همون db است. تو یک فضای موقت از انبار می‌گیری (یک میز کار) تا وسایلی که می‌خوای روشون کار کنی رو اونجا بذاری.