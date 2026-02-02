from fastapi import APIRouter, HTTPException
import models


router = APIRouter(
    tags=["tasks"],
    responses={
        404: {"description": "Не найдено"},
        418: {"description": "Я чайник"}
    }
)


task_1 = models.ResponseTask(
    id = 1,
    title = "Купить Молоко",
    description = "Марка: Домик в деревне, Жирность: 3,2%",
    status = models.TaskStatus.TODO,
)
task_2 = models.ResponseTask(
    id = 2,
    title = "Отучиться в колледже",
    description = "Закончить на красный диплом",
    status = models.TaskStatus.IN_PROGRESS,
)

tasks_db: list[models.ResponseTask] = [task_1, task_2]  # база данных
next_id = 3



'''FastAPI'''
# get (получение одной задачи)
@router.get("/tasks/{task_id}", response_model=models.ResponseTask)
def read_task(task_id: int):
    """Получить одну задачу."""
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


# get (получение всех задач)
@router.get("/tasks/", response_model=list[models.ResponseTask])
def read_all_tasks():
    """Получить все задачи."""
    return tasks_db


# post (создание)
@router.post("/tasks/", response_model=models.ResponseTask)
def create_task(task: models.CreateTask):
    """Создать новую задачу."""
    global next_id # берем глобальную переменную

    # создаём новую задачу
    new_task = models.ResponseTask(
        id = next_id,
        title = task.title,
        description = task.description,
        status = models.TaskStatus.TODO,
    )

    tasks_db.append(new_task)
    next_id += 1
    return new_task


# put (обновить)
@router.put("/tasks/{task_id}", response_model=models.ResponseTask)
def update_task(task_id: int, updated_task: models.ResponseTask):
    """
        Обновить задачу по индексу.

        Возможные статусы задачи:
        - **запланировано** — задача запланирована
        - **в процессе** — задача в работе
        - **выполнено** — задача выполнена
        - **прервано** — задача прервана
    """
    for i, task in enumerate(tasks_db): # enumerate даёт еще и индекс
        if task.id == task_id:

            updated = models.ResponseTask(
                id = task.id,
                title = updated_task.title,
                description = updated_task.description,
                status = updated_task.status,
            )

            tasks_db[i] = updated
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


# delete (удаление)
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удаление задачи по индексу."""
    global tasks_db
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            deleted_task = tasks_db.pop(i)
            return {"message": "Задача удалена", "task":deleted_task}
    raise HTTPException(status_code=404, detail="Задача не найдена")