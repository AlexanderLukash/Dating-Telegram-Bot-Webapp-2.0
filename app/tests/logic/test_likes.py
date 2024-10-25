import pytest
from faker import Faker

from app.infra.repositories.memory import MemoryLikesRepository
from app.logic.exceptions.likes import (
    LikeAlreadyExistsException,
    LikeIsNotExistsException,
    LikeTheSameUserException,
)
from app.logic.services.likes import LikesService


@pytest.mark.asyncio
async def test_create_like_success(faker: Faker):
    like_repository = MemoryLikesRepository()
    service = LikesService(like_repository=like_repository)

    from_user_id = faker.random_int()
    to_user_id = faker.random_int()

    like = await service.create_like(from_user_id, to_user_id)

    assert like.from_user.value == from_user_id
    assert like.to_user.value == to_user_id
    assert await like_repository.check_like_is_exists(from_user_id, to_user_id)


@pytest.mark.asyncio
async def test_create_like_already_exists(faker: Faker):
    like_repository = MemoryLikesRepository()
    service = LikesService(like_repository=like_repository)

    from_user_id = faker.random_int()
    to_user_id = faker.random_int()

    await service.create_like(from_user_id, to_user_id)

    with pytest.raises(LikeAlreadyExistsException):
        await service.create_like(from_user_id, to_user_id)


@pytest.mark.asyncio
async def test_create_like_the_same_user(faker: Faker):
    like_repository = MemoryLikesRepository()
    service = LikesService(like_repository=like_repository)

    user_id = faker.random_int()

    with pytest.raises(LikeTheSameUserException):
        await service.create_like(user_id, user_id)


@pytest.mark.asyncio
async def test_delete_like_success(faker: Faker):
    like_repository = MemoryLikesRepository()
    service = LikesService(like_repository=like_repository)

    from_user_id = faker.random_int()
    to_user_id = faker.random_int()

    await service.create_like(from_user_id, to_user_id)

    await service.delete_like(from_user_id, to_user_id)

    assert not await like_repository.check_like_is_exists(from_user_id, to_user_id)


@pytest.mark.asyncio
async def test_delete_like_not_exists(faker: Faker):
    like_repository = MemoryLikesRepository()
    service = LikesService(like_repository=like_repository)

    from_user_id = faker.random_int()
    to_user_id = faker.random_int()

    with pytest.raises(LikeIsNotExistsException):
        await service.delete_like(from_user_id, to_user_id)


@pytest.mark.asyncio
async def test_get_telegram_id_liked_from(faker: Faker):
    like_repository = MemoryLikesRepository()
    service = LikesService(like_repository=like_repository)

    from_user_id = faker.random_int()
    to_user_id = faker.random_int()

    await service.create_like(from_user_id, to_user_id)

    liked_users = await service.get_telegram_id_liked_from(from_user_id)
    assert to_user_id in liked_users


@pytest.mark.asyncio
async def test_get_users_ids_liked_by(faker: Faker):
    like_repository = MemoryLikesRepository()
    service = LikesService(like_repository=like_repository)

    from_user_id = faker.random_int()
    to_user_id = faker.random_int()

    await service.create_like(from_user_id, to_user_id)

    liked_by_users = await service.get_users_ids_liked_by(to_user_id)
    assert from_user_id in liked_by_users
