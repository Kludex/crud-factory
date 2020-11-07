import pytest
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm.session import Session

from tests.utils import UserUpdate, crud_user

VALID_DATA = {"name": "Potato", "age": 7}
UPDATE_DATA = {"name": "Banana", "age": 8}
INVALID_COLUMN = {"name": "Banana", "length": 1}


@pytest.mark.parametrize(
    "kwargs",
    [
        ({"name": "Potato"}),
        ({"age": 7}),
        ({}),
    ],
)
def test_update(session: Session, kwargs: dict):
    crud_user.create(session, VALID_DATA)
    with pytest.raises(NoResultFound):
        assert crud_user.get(session, **UPDATE_DATA) is not None
    crud_user.update(session, UPDATE_DATA, **kwargs)
    found = crud_user.get(session, **UPDATE_DATA)
    assert {"name": found.name, "age": found.age} == UPDATE_DATA


@pytest.mark.parametrize(
    "kwargs",
    [
        ({"name": "Potato"}),
        ({"age": 7}),
        ({}),
    ],
)
def test_update_with_pydantic(session: Session, kwargs: dict):
    crud_user.create(session, VALID_DATA)
    with pytest.raises(NoResultFound):
        assert crud_user.get(session, **UPDATE_DATA) is not None
    crud_user.update(session, UserUpdate(**UPDATE_DATA), **kwargs)
    found = crud_user.get(session, **UPDATE_DATA)
    assert {"name": found.name, "age": found.age} == UPDATE_DATA


@pytest.mark.parametrize(
    "kwargs",
    [
        ({"name": "Potato"}),
        ({"age": 7}),
        ({}),
    ],
)
def test_update_wrong_column(session: Session, kwargs: dict):
    obj_in = crud_user.create(session, VALID_DATA)
    obj_update = crud_user.update(session, INVALID_COLUMN, **kwargs)
    assert obj_in == obj_update


@pytest.mark.parametrize("kwargs", [{"name": "otatoP"}, {"age": 8}])
def test_update_not_found(session: Session, kwargs: dict):
    crud_user.create(session, VALID_DATA)
    with pytest.raises(NoResultFound):
        crud_user.update(session, UPDATE_DATA, **kwargs)


@pytest.mark.parametrize("kwargs", [{"name": "Potato"}, {"age": 7}, {}])
def test_update_multiple_rows(session: Session, kwargs: dict):
    crud_user.create(session, VALID_DATA)
    crud_user.create(session, VALID_DATA)
    with pytest.raises(MultipleResultsFound):
        crud_user.update(session, UPDATE_DATA, **kwargs)
