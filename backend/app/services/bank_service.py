from app.models.bank import Bank
from app.repositories.bank_repository import BankRepository
from app.schemas.bank import BankCreate, BankUpdate


class DuplicateBankError(Exception):
    """Raised when a bank name or short name is already in use."""


class BankNotFoundError(Exception):
    """Raised when a requested bank does not exist."""


class EmptyBankUpdateError(Exception):
    """Raised when an update supplies no fields."""


class BankService:
    def __init__(self, repository: BankRepository) -> None:
        self.repository = repository

    def create_bank(self, payload: BankCreate) -> Bank:
        values = self._create_values(payload)
        self._ensure_unique(values["name"], values["short_name"])
        return self.repository.create(**values)

    def get_bank(self, bank_id: int) -> Bank:
        bank = self.repository.get_by_id(bank_id)
        if bank is None:
            raise BankNotFoundError
        return bank

    def list_banks(self, *, page: int, page_size: int) -> tuple[list[Bank], int]:
        return self.repository.list(page=page, page_size=page_size)

    def update_bank(self, bank_id: int, payload: BankUpdate) -> Bank:
        bank = self.get_bank(bank_id)
        values = self._update_values(payload)
        if not values:
            raise EmptyBankUpdateError
        self._ensure_update_is_unique(bank, values)
        return self.repository.update(bank, **values)

    def delete_bank(self, bank_id: int) -> None:
        self.repository.delete(self.get_bank(bank_id))

    def _ensure_unique(self, name: str, short_name: str) -> None:
        if self.repository.get_by_name(name) or self.repository.get_by_short_name(short_name):
            raise DuplicateBankError

    def _ensure_update_is_unique(self, bank: Bank, values: dict[str, object]) -> None:
        name = values.get("name")
        if isinstance(name, str):
            existing = self.repository.get_by_name(name)
            if existing and existing.id != bank.id:
                raise DuplicateBankError
        short_name = values.get("short_name")
        if isinstance(short_name, str):
            existing = self.repository.get_by_short_name(short_name)
            if existing and existing.id != bank.id:
                raise DuplicateBankError

    @staticmethod
    def _create_values(payload: BankCreate) -> dict[str, object]:
        return {
            "name": payload.name,
            "short_name": payload.short_name.upper(),
            "official_website": str(payload.official_website),
            "customer_care": payload.customer_care,
        }

    @staticmethod
    def _update_values(payload: BankUpdate) -> dict[str, object]:
        values = payload.model_dump(exclude_unset=True)
        if "short_name" in values and values["short_name"] is not None:
            values["short_name"] = str(values["short_name"]).upper()
        if "official_website" in values and values["official_website"] is not None:
            values["official_website"] = str(values["official_website"])
        return values
