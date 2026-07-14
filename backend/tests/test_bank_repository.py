from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.session import Base
from app.models.bank import Bank
from app.repositories.bank_repository import BankRepository


def test_list_returns_paginated_banks():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        repository = BankRepository(session)
        repository.create(name="HDFC Bank", short_name="HDFC", official_website="https://www.hdfcbank.com")
        repository.create(name="Axis Bank", short_name="AXIS", official_website="https://www.axisbank.com")

        items, total = repository.list(page=1, page_size=1)

    assert total == 2
    assert len(items) == 1
    assert items[0].name == "Axis Bank"


def test_get_by_name_is_case_insensitive():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        repository = BankRepository(session)
        bank = repository.create(name="HDFC Bank", short_name="HDFC", official_website="https://www.hdfcbank.com")

        result = repository.get_by_name("hdfc bank")

    assert result is not None
    assert result.id == bank.id
