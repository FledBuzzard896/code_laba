from fastapi import APIRouter, HTTPException
import models

router = APIRouter(
    tags=["users"],
    responses = {
        404: {"description": "Не найдено"},
    }
)

user_1 = models.User(
    id = 1,
    login = "FledBuzzard896",
    password = "qwerty12345",
    name = "Артемий Лебедев",
    gender = True,
    email = "test@mail.com",
)

users_db: list[models.User] = [user_1]
next_id = 2

@router.get("/users/{id}", response_model=models.User)
def read_user(id: int):
    """Вывод пользователя по индексу"""
    for user in users_db:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail="Такого пользователя нету, дружище")

@router.post("/users/", response_model=models.User)
def create_user(user: models.User):

    global next_id

    new_user = models.User(
        id = next_id,
        login = user.login,
        password = user.password,
        name = user.name,
        gender = user.gender,
        email = user.email,
    )

    users_db.append(new_user)
    next_id += 1
    return new_user

@router.delete("/users/{id}", response_model=models.User)
def delete_user(id: int):

    global next_id
    for i, user in enumerate(users_db):
        if user.id == id:
            deleted_user = users_db.pop(i)
            return {"message": "Пользователь удалён", "user": deleted_user}
    raise HTTPException(status_code=404, detail="Пользователь не найден!")