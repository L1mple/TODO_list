"""Module for storing request/response handlers.

As an agreement handler functions are called as: <method>_<route>

For example if handler has full route: GET task/{uid} function is called get_task_uid

They can ignore docstrings, but description is required.
"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI, Query, status
from fastapi.responses import JSONResponse, Response

from todo.core.task import service as task_service
from todo.core.task.models import NewTask, TaskUID
from todo.core.task.repository import TaskRepository
from todo.dependencies import Container

from .contracts import TaskJSONResponse

router = APIRouter(prefix="/task", tags=["Task"])


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize task router for app."""
    app.include_router(router)
    return app


@router.post(
    "/",
    description="Create new task from base information",
    response_description="Successfully create new task",
    status_code=201,
)
@inject
async def post_task(  # noqa
    body: NewTask,
    task_repository: TaskRepository = Depends(  # noqa
        Provide[Container.task_repository]
    ),
):
    uid = await task_service.create_one(body, task_repository)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"task/{uid}"},
    )


@router.get(
    "/",
    description="Get multiple tasks, paginated",
    response_model=list[TaskJSONResponse],
    responses={
        404: {"description": "No tasks found"},
    },
)
@inject
async def get_task(  # noqa
    page: int = Query(  # noqa
        default=0,
        ge=0,
        description="Which batch of entities to fetch",
    ),
    per_page: int = Query(  # noqa
        default=10,
        alias="perPage",
        ge=1,
        le=50,
        description="How many query tasks will be fetched",
    ),
    task_repository: TaskRepository = Depends(  # noqa
        Provide[Container.task_repository]
    ),
):
    tasks = await task_service.get_many(page, per_page, task_repository)
    if len(tasks) == 0:
        return Response(
            content=[],
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return list(map(TaskJSONResponse.from_entity, tasks))


@router.get(
    "/{uid}",
    description="Get one task by uid",
    response_model=TaskJSONResponse,
    responses={
        404: {"description": "No task with passed uid found"},
    },
)
@inject
async def get_task_uid(  # noqa
    uid: str,
    task_repository: TaskRepository = Depends(  # noqa
        Provide[Container.task_repository]
    ),
):
    task = await task_service.get_by_uid(TaskUID(uid), task_repository)
    if task is None:
        return JSONResponse(
            content=None,
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return TaskJSONResponse.from_entity(task)


@router.patch(
    "/complete/{uid}",
    description="Mark task as completed",
)
@inject
async def patch_task_complete_uid(  # noqa
    uid: str,
    task_repository: TaskRepository = Depends(  # noqa
        Provide[Container.task_repository]
    ),
):
    await task_service.complete(uid, task_repository)
