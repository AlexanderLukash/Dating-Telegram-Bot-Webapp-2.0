import pytest

from app.domain.exceptions.users import (
    AboutTextTooLongException,
    AboutTextTooShortException,
    AgeNotInRangeException,
    CityTooShortException,
    EmptyAgeException,
    EmptyCityException,
    EmptyNameException,
    NameTooLongException,
    NameTooShortException,
)
from app.domain.values.users import (
    AboutText,
    Age,
    City,
    Gender,
    Name,
)


def test_create_name_empty_exception():
    with pytest.raises(EmptyNameException):
        Name(value="")


def test_create_name_too_long_exception():
    with pytest.raises(NameTooLongException):
        Name(value="a" * 51)


def test_create_name_too_short_exception():
    with pytest.raises(NameTooShortException):
        Name(value="a")


def test_create_name_success():
    value = "John"
    name = Name(value=value)

    assert name.value == value


def test_create_gender_exception():
    with pytest.raises(ValueError):
        Gender(value="Invalid")


def test_create_gender_success():
    value = "Man"
    gender = Gender(value=value)

    assert gender.value == value


def test_create_age_range_exception():
    with pytest.raises(AgeNotInRangeException):
        Age(value=10)

    with pytest.raises(AgeNotInRangeException):
        Age(value=121)


def test_create_age_is_empty_exception():
    with pytest.raises(EmptyAgeException):
        Age(value=None)  # noqa


def test_create_age_success():
    age = 19
    assert Age(value=age).value == age


def test_create_city_is_empty_exception():
    with pytest.raises(EmptyCityException):
        City(value="")


def test_create_city_too_short_exception():
    with pytest.raises(CityTooShortException):
        City(value="a")


def test_create_city_success():
    city = "London"
    assert City(value=city).value == city


def test_create_about_too_short_exception():
    with pytest.raises(AboutTextTooShortException):
        AboutText(value="a")


def test_create_about_too_long_exception():
    text = "a" * 126
    with pytest.raises(AboutTextTooLongException):
        AboutText(value=text)


def test_create_about_success():
    text = "I am a software engineer."
    about = AboutText(value=text)

    assert about.value == text
