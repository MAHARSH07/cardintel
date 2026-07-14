import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.session import Base
from app.repositories.bank_repository import BankRepository
from app.schemas.bank import BankCreate, BankUpdate
from app.services.bank_service import BankNotFoundError, BankService, DuplicateBankError


def make_service() -> BankService:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    return BankService(BankRepository(Session(engine)))


def test_create_normalizes_short_name_and_prevents_duplicates():
    service = make_service()
    bank = service.create_bank(BankCreate(name="HDFC Bank", short_name="hdfc", official_website="https://www.hdfcbank.com"))

    assert bank.short_name == "HDFC"
    with pytest.raises(DuplicateBankError):
        service.create_bank(BankCreate(name="hdfc bank", short_name="hdfc2", official_website="https://example.com"))


def test_update_missing_bank_raises_not_found():
    service = make_service()

    with pytest.raises(BankNotFoundError):
        service.update_bank(999, BankUpdate(name="New Name"))
