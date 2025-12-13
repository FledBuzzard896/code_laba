import sys
sys.path.append("/path/to/pydantic")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from routers import tasks

app = FastAPI(title="TaskFlow API", version="1.0")
app.include_router(tasks.router) # подключаем роутер задач

# эндпоинт для проверки
@app.get("/")
def read_root():
    return {"message": "TaskFlow API v1.0 работает!"}


'''
СПРАВКА:

ФУНКЦИЯ СОЗДАНИЯ ЗАДАЧИ:
@router.post("/", response_model=models.ResponseTask)
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

ОБЪЯСНЕНИЕ ФУНКЦИИ:
1.1 @app.post (@router.post) - декоратор, который поясняет что функция обрабатывает post-запросы (создание)
1.2 "/tasks" ("/") - Это URL эндпоинта (пример запроса: http://сервер/tasks)
1.3 response_model=ResponseTask - проверка, что функция возвращает данные в формате ResponseTask

2.1 task: CreateTask - параметр функции, который FastAPI возьмет из post-запроса и проверит что соответсвует CreateTask

3.1 global next_id - говорим работать с глобальной переменной, дабы происходило изменение индекса

4-11 Создание новой задачи, добавление в БД, изменение индекса и возврат новой задачи.

ЧТО ПРОИСХОДИТ ПОСЛЕ:
1. FastAPI Берёт new_task
2. Проверяет, что он соответствует ResponseTask (из response_model)
3. Автоматически конвертирует в JSON
4. Отправляет клиенту с HTTP-статусом 200 (или 201)
'''