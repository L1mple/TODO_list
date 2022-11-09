from bson import ObjectId
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Query

from todo.dependencies import Container
from todo.domain.models import Task
from todo.service.mongo.models import PyObjectId, TaskDb
from todo.service.mongo.repositories import MongoDbTaskRepository

router = APIRouter()


@router.get("/tasks")
@inject
async def get_tasks(
    repository: MongoDbTaskRepository = Depends(Provide[Container.task_repository]),
):
    """Get all tasks from db."""
    return await repository.list_all()


@router.post("/task")
@inject
async def create_one_task(
    task_data: Task = Body(default=..., description="Task model to add in db."),
    repository: MongoDbTaskRepository = Depends(Provide[Container.task_repository]),
):
    """Create one task in db."""
    task_db = TaskDb(
        _id=PyObjectId(ObjectId(task_data.uid)),
        description=task_data.description,
        deadline=task_data.deadline,
        exp_date=task_data.exp_date,
    )
    return await repository.create_one(document_data=task_db)


@router.get("/task/{task_id}")
@inject
async def get_one_task_by_id(
    task_id: str = Path(
        default=...,
        description="Task uid to get the Task model from db.",
        example="569ed8269353e9f4c51617aa",
    ),
    repository: MongoDbTaskRepository = Depends(Provide[Container.task_repository]),
):
    """Get one task by id from db."""
    return await repository.get_one_by_id(uid=PyObjectId(task_id))


@router.post("/tasks")
@inject
async def create_many_tasks(
    tasks_data: list[Task] = Body(default=..., description="Task model to add in db."),
    repository: MongoDbTaskRepository = Depends(Provide[Container.task_repository]),
):
    """Create all tasks from request body."""
    tasks_to_create = []
    for task in tasks_data:
        task_to_add = TaskDb(
            _id=PyObjectId(ObjectId(task.uid)),
            description=task.description,
            deadline=task.deadline,
            exp_date=task.exp_date,
        )
        tasks_to_create.append(task_to_add.dict(by_alias=True))
    return await repository.create_many(documents=tasks_to_create)


@router.get("/task")
@inject
async def get_many_tasks(
    page: int = Query(default=1, description="From what number starts pagination"),
    per_page: int = Query(default=10, description="To what number starts pagination"),
    repository: MongoDbTaskRepository = Depends(Provide[Container.task_repository]),
):
    """Pagination get."""
    return await repository.get_many(page=page, per_page=per_page)


@router.delete("/task/{task_id}")
@inject
async def delete_task_by_id(
    task_id: str = Path(
        default=..., description="Task uid to delete the Task model from db."
    ),
    repository: MongoDbTaskRepository = Depends(Provide[Container.task_repository]),
):
    """Delete Task by id from db."""
    return await repository.delete_one_by_id(uid=PyObjectId(task_id))


@router.put("/task")
@inject
async def replace_task_in_db(
    task_data: TaskDb = Body(default=..., description="Replacee existing Task in db."),
    repository: MongoDbTaskRepository = Depends(Provide[Container.task_repository]),
):
    """Replace Task in db."""
    task_to_replace = TaskDb(
        _id=PyObjectId(ObjectId(task_data.uid)),
        description=task_data.description,
        deadline=task_data.deadline,
        exp_date=task_data.exp_date,
    )
    return await repository.replace_one(document=task_to_replace)
