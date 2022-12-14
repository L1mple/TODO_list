"""Module for storing request/response handlers.

As an agreement handler functions are called as: <method>_<route>
For example if handler has full route: GET task/{uid} function is called get_task_uid
They can ignore docstrings, but description is required.
"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, FastAPI, Path, Query, status
from fastapi.responses import JSONResponse, Response

from todo.core.task.models import Task, TaskUID, UpdateTask
from todo.core.task.services import AbstractTaskService
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
    body: Task = Body(default=..., description="Task Model from domain"),
    task_service: AbstractTaskService = Depends(Provide[Container.task_service]),
):
    uid = await task_service.create_one(body)
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
async def get_tasks(  # noqa
    page: int = Query(  # noqa
        default=1,
        ge=1,
        description="Which batch of entities to fetch",
    ),
    per_page: int = Query(  # noqa
        default=10,
        alias="perPage",
        ge=1,
        le=50,
        description="How many query tasks will be fetched",
    ),
    task_service: AbstractTaskService = Depends(Provide[Container.task_service]),
):
    tasks = await task_service.get_many(page, per_page)
    if len(tasks) == 0:
        return JSONResponse(
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
    uid: str = Path(
        default=..., regex="^[0-9a-f]{24}$", example="507f191e810c19729de860ea"
    ),
    task_service: AbstractTaskService = Depends(Provide[Container.task_service]),
):
    task = await task_service.get_by_uid(TaskUID(uid))
    if task is None:
        return JSONResponse(
            content=None,
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return TaskJSONResponse.from_entity(task)


@router.patch(
    "/complete/{uid}",
    description="Mark task as completed",
    responses={
        404: {"description": "No task with passed uid found"},
        203: {"description": "Successfully updated task info"},
    },
)
@inject
async def patch_task_complete_uid(  # noqa
    uid: str = Path(
        default=..., regex="^[0-9a-f]{24}$", example="507f191e810c19729de860ea"
    ),
    task_service: AbstractTaskService = Depends(Provide[Container.task_service]),
):
    updated_uid = await task_service.complete(uid)

    if updated_uid is None:
        return Response(
            content=None,
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
        headers={"Location": f"task/{updated_uid}"},
    )


@router.patch(
    "/",
    description="Edit Task info if needed.",
    response_description="Successfully updated task info",
    status_code=203,
    responses={
        404: {"description": "No task with passed uid found"},
        203: {"description": "Successfully updated task info"},
    },
)
@inject
async def patch_task(  # noqa
    body: UpdateTask = Body(
        default=..., description="Fields to update in task, required uid field"
    ),
    task_service: AbstractTaskService = Depends(Provide[Container.task_service]),
):
    updated_uid = await task_service.update_one(body)

    if updated_uid is None:
        return Response(
            content=None,
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
        headers={"Location": f"task/{updated_uid}"},
    )


@router.delete(
    "/{uid}",
    description="Delete Task by id.",
    response_description="Successfully updated task info",
    responses={
        204: {"description": "Successfully deleted"},
        404: {"description": "No task with passed uid found"},
    },
)
@inject
async def delete_task(
    uid: str = Path(
        default=..., regex="^[0-9a-f]{24}$", example="507f191e810c19729de860ea"
    ),
    task_service: AbstractTaskService = Depends(
        Provide[Container.task_service],
    ),
):
    result = await task_service.delete_by_uid(TaskUID(uid))
    if result is None:
        return Response(
            content=None,
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
