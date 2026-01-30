from fastapi import APIRouter, HTTPException
import models
import users

router = APIRouter(
    tags=["projects"],
    responses={
        404: {"description": "Ниче не нашел, бро"},
    }
)

test_project = models.Project(
    id=1,
    title="Моя первая API",
    description="Я короче создаю, мне нравится",
    party=list(users.user_1)
)

projects_db: list[models.Project] = [test_project]
next_id = 2

@router.get("/projects/{id}", response_model=models.Project)
def read_prioject(id: int):
    """Вывод проекта по индексу"""
    for project in projects_db:
        if project.id == id:
            return project
    raise HTTPException(status_code=404, detail="Такого проекта не существуют")

@router.post("/projects/", response_model=models.Project)
def create_project(project: models.Project):

    global next_id

    new_project = models.Project(
        id = next_id,
        title = project.title,
        description = project.description,
        party = project.party,
    )

    projects_db.append(new_project)
    next_id += 1
    return new_project

@router.delete("/projects/{id}", response_model=models.Project)
def delete_project(id: int):

    global next_id
    for i, project in enumerate(projects_db):
        if project.id == id:
            deleted_project = projects_db.pop(i)
            return {"message": "Проект удалён", "user": deleted_project}
    raise HTTPException(status_code=404, detail="Проект не найден!")