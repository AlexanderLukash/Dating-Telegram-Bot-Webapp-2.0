from fastapi.routing import APIRouter

from app.application.api.v1.users.handlers import router as users_router


router = APIRouter(
    prefix="/v1",
)

router.include_router(users_router)
