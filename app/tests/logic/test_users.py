import pytest
from faker import Faker

from app.domain.entities.users import UserEntity
from app.domain.values.users import (
    AboutText,
    Name,
)
from app.infra.repositories.memory import MemoryUsersRepository
from app.logic.exceptions.users import UserAlreadyExistsException
from app.logic.services.users import UsersService


@pytest.mark.asyncio
async def test_create_user_success(faker: Faker):
    user_repository = MemoryUsersRepository()
    service = UsersService(user_repository=user_repository)
    user = UserEntity(
        telegram_id=faker.random_int(),
        name=Name(faker.first_name()),
        is_active=True,
    )

    created_user = await service.create_user(user)

    assert created_user.telegram_id in user_repository._users
    assert user_repository._users[created_user.telegram_id] == user


@pytest.mark.asyncio
async def test_create_user_already_exists(faker: Faker):
    user_repository = MemoryUsersRepository()
    service = UsersService(user_repository=user_repository)
    user = UserEntity(
        telegram_id=faker.random_int(),
        name=Name(faker.first_name()),
        is_active=True,
    )
    await user_repository.create_user(user)

    with pytest.raises(UserAlreadyExistsException):
        await service.create_user(user)


@pytest.mark.asyncio
async def test_get_user_success(faker: Faker):
    user_repository = MemoryUsersRepository()
    service = UsersService(user_repository=user_repository)
    telegram_id = faker.random_int()
    user = UserEntity(
        telegram_id=telegram_id,
        name=Name(faker.first_name()),
        is_active=True,
    )
    await user_repository.create_user(user)

    fetched_user = await service.get_user(telegram_id)

    assert fetched_user == user


@pytest.mark.asyncio
async def test_update_user_info_after_reg(faker: Faker):
    user_repository = MemoryUsersRepository()
    service = UsersService(user_repository=user_repository)
    telegram_id = faker.random_int()
    user = UserEntity(
        telegram_id=telegram_id,
        name=Name(faker.first_name()),
        is_active=True,
    )
    await user_repository.create_user(user)

    new_data = {"is_active": False}
    await service.update_user_info_after_reg(telegram_id, new_data)

    assert not user_repository._users[telegram_id].is_active


@pytest.mark.asyncio
async def test_update_user_about_info(faker: Faker):
    user_repository = MemoryUsersRepository()
    service = UsersService(user_repository=user_repository)
    telegram_id = faker.random_int()
    user = UserEntity(
        telegram_id=telegram_id,
        name=Name(faker.first_name()),
        is_active=True,
    )
    await user_repository.create_user(user)

    about_text = AboutText(faker.text())
    await service.update_user_about_info(telegram_id, about_text)

    assert user_repository._users[telegram_id].about == about_text


@pytest.mark.asyncio
async def test_check_user_exist(faker: Faker):
    user_repository = MemoryUsersRepository()
    service = UsersService(user_repository=user_repository)
    telegram_id = faker.random_int()
    user = UserEntity(
        telegram_id=telegram_id,
        name=Name(faker.first_name()),
        is_active=True,
    )
    await user_repository.create_user(user)

    assert await service.check_user_exist(telegram_id) is True
    assert await service.check_user_exist(faker.random_int()) is False


@pytest.mark.asyncio
async def test_check_user_is_active(faker: Faker):
    user_repository = MemoryUsersRepository()
    service = UsersService(user_repository=user_repository)
    telegram_id = faker.random_int()
    user = UserEntity(
        telegram_id=telegram_id,
        name=Name(faker.first_name()),
        is_active=True,
    )
    await user_repository.create_user(user)

    assert await service.check_user_is_active(telegram_id) is True

    await service.update_user_info_after_reg(telegram_id, {"is_active": False})

    assert await service.check_user_is_active(telegram_id) is False
