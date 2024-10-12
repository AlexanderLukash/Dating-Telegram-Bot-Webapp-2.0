from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from punq import Container

from app.application.api.schemas import ErrorSchema
from app.application.api.v1.likes.schemas import (
    CreateLikeRequestSchema,
    CreateLikeResponseSchema,
    DeleteLikeRequestSchema,
    DeleteLikeResponseSchema,
    GetUsersFromResponseSchema,
)
from app.application.api.v1.users.schemas import UserDetailSchema
from app.domain.exceptions.base import ApplicationException
from app.logic.init import init_container
from app.logic.services.base import BaseLikesService


router = APIRouter(
    prefix="/likes",
    tags=["Like"],
)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    description="Get all users list.",
    responses={
        status.HTTP_200_OK: {"model": CreateLikeResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def add_like_to_user(
    schema: CreateLikeRequestSchema,
    container: Container = Depends(init_container),
) -> CreateLikeResponseSchema:
    service: BaseLikesService = container.resolve(BaseLikesService)

    try:
        like = await service.create_like(
            from_user_id=schema.from_user,
            to_user_id=schema.to_user,
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return CreateLikeResponseSchema.from_entity(like)


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    description="Delete like from user to user.",
    responses={
        status.HTTP_200_OK: {"model": DeleteLikeResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def delete_like(
    schema: DeleteLikeRequestSchema,
    container: Container = Depends(init_container),
) -> DeleteLikeResponseSchema:
    service: BaseLikesService = container.resolve(BaseLikesService)

    try:
        await service.delete_like(
            from_user_id=schema.from_user,
            to_user_id=schema.to_user,
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return DeleteLikeResponseSchema.delete_response()


@router.get(
    "/{from_user_id}",
    status_code=status.HTTP_200_OK,
    description="Get all users that the user liked.",
    responses={
        status.HTTP_200_OK: {"model": GetUsersFromResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_users_from(
    from_user_id: int,
    container: Container = Depends(init_container),
) -> GetUsersFromResponseSchema:
    service: BaseLikesService = container.resolve(BaseLikesService)

    try:
        users = await service.get_like_from_user(from_user_id=from_user_id)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return GetUsersFromResponseSchema(
        items=[UserDetailSchema.from_entity(user) for user in users],
    )
