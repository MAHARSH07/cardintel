from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.bank_repository import BankRepository
from app.schemas.bank import BankCreate, BankResponse, BankUpdate, PaginatedBankResponse
from app.services.bank_service import BankNotFoundError, BankService, DuplicateBankError, EmptyBankUpdateError

public_router = APIRouter(prefix="/banks", tags=["banks"])
admin_router = APIRouter(prefix="/admin/banks", tags=["admin: banks"])


def get_bank_service(db: Annotated[Session, Depends(get_db)]) -> BankService:
    return BankService(BankRepository(db))


BankServiceDependency = Annotated[BankService, Depends(get_bank_service)]


@public_router.get("", response_model=PaginatedBankResponse)
def list_banks(
    service: BankServiceDependency,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> PaginatedBankResponse:
    items, total = service.list_banks(page=page, page_size=page_size)
    return PaginatedBankResponse(items=items, total=total, page=page, page_size=page_size)


@public_router.get("/{bank_id}", response_model=BankResponse)
def get_bank(bank_id: int, service: BankServiceDependency) -> BankResponse:
    try:
        return service.get_bank(bank_id)
    except BankNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Bank not found") from exc


@admin_router.post("", response_model=BankResponse, status_code=status.HTTP_201_CREATED)
def create_bank(payload: BankCreate, service: BankServiceDependency) -> BankResponse:
    try:
        return service.create_bank(payload)
    except DuplicateBankError as exc:
        raise HTTPException(status_code=409, detail="Bank name or short name already exists") from exc


@admin_router.put("/{bank_id}", response_model=BankResponse)
def update_bank(bank_id: int, payload: BankUpdate, service: BankServiceDependency) -> BankResponse:
    try:
        return service.update_bank(bank_id, payload)
    except BankNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Bank not found") from exc
    except DuplicateBankError as exc:
        raise HTTPException(status_code=409, detail="Bank name or short name already exists") from exc
    except EmptyBankUpdateError as exc:
        raise HTTPException(status_code=422, detail="At least one field is required") from exc


@admin_router.delete("/{bank_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bank(bank_id: int, service: BankServiceDependency) -> Response:
    try:
        service.delete_bank(bank_id)
    except BankNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Bank not found") from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
