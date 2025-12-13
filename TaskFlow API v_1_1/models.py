from typing import Optional
from enum import Enum
from pydantic import BaseModel

'''Pydantic'''

# класс для статусов заданий
class TaskStatus(str, Enum):
    TODO = "запланировано"
    IN_PROGRESS = "в процессе"
    DONE = "выполнено"
    CANCELLED = "прервано"

'''Это то, что вводит пользователь (Наименование задачи и описание)'''
class CreateTask(BaseModel): # что принимаем от пользователя
    title: str
    description: Optional[str] = None # строка или ничего (необязательно)

'''Это то что мы добавляем автоматически (Id задачи и её статус)'''
class ResponseTask(CreateTask): # что возвращаем пользователю
    id: int
    status: TaskStatus = TaskStatus.TODO