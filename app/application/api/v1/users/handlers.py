from fastapi.routing import APIRouter


router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.get("")
async def test():
    return {"status": True}
