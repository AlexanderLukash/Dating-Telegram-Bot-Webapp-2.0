from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.routing import APIRouter

from punq import Container

from app.application.api.schemas import ErrorSchema
from app.application.api.v1.users.filters import GetUsersFilters
from app.application.api.v1.users.schemas import (
    GetUsersFromResponseSchema,
    GetUsersResponseSchema,
    UserDetailSchema,
)
from app.domain.exceptions.base import ApplicationException
from app.logic.init import init_container
from app.logic.services.base import (
    BaseLikesService,
    BaseUsersService,
)


router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Get all users list.",
    responses={
        status.HTTP_200_OK: {"model": GetUsersResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_all_users_handler(
    filters: GetUsersFilters = Depends(),
    container: Container = Depends(init_container),
) -> GetUsersResponseSchema:
    service: BaseUsersService = container.resolve(BaseUsersService)

    try:
        users, count = await service.get_all_users(filters=filters.to_infra())
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return GetUsersResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[UserDetailSchema.from_entity(user) for user in users],
    )


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    description="Get information about the users.",
    responses={
        status.HTTP_200_OK: {"model": UserDetailSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_user_handler(
    user_id: int,
    container: Container = Depends(init_container),
) -> UserDetailSchema:
    service: BaseUsersService = container.resolve(BaseUsersService)

    try:
        user = await service.get_user(telegram_id=user_id)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return UserDetailSchema.from_entity(user)


@router.get(
    "/from/{user_id}",
    status_code=status.HTTP_200_OK,
    description="Get all users that the user liked.",
    responses={
        status.HTTP_200_OK: {"model": GetUsersFromResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_users_liked_from(
    user_id: int,
    container: Container = Depends(init_container),
) -> GetUsersFromResponseSchema:
    service_likes: BaseLikesService = container.resolve(BaseLikesService)
    service_users: BaseUsersService = container.resolve(BaseUsersService)

    try:
        telegram_ids = await service_likes.get_telegram_id_liked_from(
            user_id=user_id,
        )
        users = await service_users.get_users_liked_from(users_list=telegram_ids)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return GetUsersFromResponseSchema(
        items=[UserDetailSchema.from_entity(user) for user in users],
    )


@router.get(
    "/by/{user_id}",
    status_code=status.HTTP_200_OK,
    description="Get all users that liked the user.",
    responses={
        status.HTTP_200_OK: {"model": GetUsersFromResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_users_liked_by(
    user_id: int,
    container: Container = Depends(init_container),
) -> GetUsersFromResponseSchema:
    service_likes: BaseLikesService = container.resolve(BaseLikesService)
    service_users: BaseUsersService = container.resolve(BaseUsersService)

    try:
        telegram_ids = await service_likes.get_users_ids_liked_by(
            user_id=user_id,
        )
        users = await service_users.get_users_liked_by(users_list=telegram_ids)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return GetUsersFromResponseSchema(
        items=[UserDetailSchema.from_entity(user) for user in users],
    )
