from app.domain.entities.users import UserEntity


def convert_user_entity_to_document(user: UserEntity) -> dict:
    return {
        "telegram_id": user.telegram_id,
        "username": user.username,
        "name": user.name.as_generic_type() if user.name else None,
        "gender": user.gender.as_generic_type() if user.gender else None,
        "age": user.age.as_generic_type() if user.age else None,
        "city": user.city.as_generic_type() if user.city else None,
        "looking_for": user.looking_for.as_generic_type() if user.looking_for else None,
        "about": user.about.as_generic_type() if user.about else None,
        "is_active": user.is_active,
    }
