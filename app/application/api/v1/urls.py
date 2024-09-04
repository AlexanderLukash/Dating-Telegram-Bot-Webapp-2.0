from fastapi.routing import APIRouter

from app.application.api.v1.users.handlers import router as users_router
from app.application.api.v1.webhooks.telegram import router as telegram_webhook_router


router = APIRouter(
    prefix="/v1",
)

router.include_router(users_router)
router.include_router(telegram_webhook_router)
