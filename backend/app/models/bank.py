import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampedModel


class SourceType(str, enum.Enum):
    PRODUCT_PAGE = "product_page"
    TERMS_AND_CONDITIONS = "terms_and_conditions"
    PDF = "pdf"
    WEBPAGE = "webpage"


class Bank(TimestampedModel):
    __tablename__ = "banks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    short_name: Mapped[str] = mapped_column(String(50), unique=True)
    official_website: Mapped[str] = mapped_column(String(500))
    customer_care: Mapped[str | None] = mapped_column(String(100))

    cards: Mapped[list["CreditCard"]] = relationship(back_populates="bank")
    sources: Mapped[list["Source"]] = relationship(back_populates="bank")


class Source(TimestampedModel):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id", ondelete="CASCADE"), index=True)
    url: Mapped[str] = mapped_column(String(1000), unique=True)
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType))
    last_checked: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    etag: Mapped[str | None] = mapped_column(String(255))

    bank: Mapped[Bank] = relationship(back_populates="sources")
