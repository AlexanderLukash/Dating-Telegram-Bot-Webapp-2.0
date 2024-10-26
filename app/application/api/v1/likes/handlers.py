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
    GetLikeRequestSchema,
    GetLikeResponseSchema,
)
from app.bot.utils.notificator import send_liked_message
from app.domain.exceptions.base import ApplicationException
from app.logic.init import init_container
from app.logic.services.base import BaseLikesService


router = APIRouter(
    prefix="/likes",
    tags=["Like"],
)


@router.get(
    "/{from_user}/{to_user}",
    status_code=status.HTTP_200_OK,
    description="Get like.",
    responses={
        status.HTTP_200_OK: {"model": GetLikeRequestSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_like(
    from_user: int,
    to_user: int,
    container: Container = Depends(init_container),
) -> GetLikeResponseSchema:
    service: BaseLikesService = container.resolve(BaseLikesService)

    try:
        like = await service.check_like_is_exists(
            from_user_id=from_user,
            to_user_id=to_user,
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return GetLikeResponseSchema(status=like)


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
        await send_liked_message(
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
