from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class BankCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    short_name: str = Field(min_length=1, max_length=50)
    official_website: HttpUrl
    customer_care: str | None = Field(default=None, max_length=100)

    @field_validator("name", "short_name", "customer_care", mode="before")
    @classmethod
    def trim_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = " ".join(value.split())
        if not cleaned:
            raise ValueError("Value cannot be empty")
        return cleaned


class BankUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    short_name: str | None = Field(default=None, min_length=1, max_length=50)
    official_website: HttpUrl | None = None
    customer_care: str | None = Field(default=None, max_length=100)

    @field_validator("name", "short_name", "customer_care", mode="before")
    @classmethod
    def trim_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = " ".join(value.split())
        if not cleaned:
            raise ValueError("Value cannot be empty")
        return cleaned


class BankResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    short_name: str
    official_website: HttpUrl
    customer_care: str | None
    created_at: datetime
    updated_at: datetime


class PaginatedBankResponse(BaseModel):
    items: list[BankResponse]
    total: int
    page: int
    page_size: int


class BankSummary(BaseModel):
    name: str
