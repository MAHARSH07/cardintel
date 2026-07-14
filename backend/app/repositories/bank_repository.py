from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.bank import Bank


class BankRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, **values: object) -> Bank:
        bank = Bank(**values)
        self.db.add(bank)
        self.db.commit()
        self.db.refresh(bank)
        return bank

    def get_by_id(self, bank_id: int) -> Bank | None:
        return self.db.get(Bank, bank_id)

    def get_by_name(self, name: str) -> Bank | None:
        statement = select(Bank).where(func.lower(Bank.name) == name.lower())
        return self.db.scalar(statement)

    def get_by_short_name(self, short_name: str) -> Bank | None:
        statement = select(Bank).where(func.lower(Bank.short_name) == short_name.lower())
        return self.db.scalar(statement)

    def list(self, *, page: int, page_size: int) -> tuple[list[Bank], int]:
        total = self.db.scalar(select(func.count()).select_from(Bank)) or 0
        statement = select(Bank).order_by(Bank.name).offset((page - 1) * page_size).limit(page_size)
        return list(self.db.scalars(statement)), total

    def update(self, bank: Bank, **values: object) -> Bank:
        for field, value in values.items():
            setattr(bank, field, value)
        self.db.commit()
        self.db.refresh(bank)
        return bank

    def delete(self, bank: Bank) -> None:
        self.db.delete(bank)
        self.db.commit()
