import enum
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampedModel


class PolicyChangeType(str, enum.Enum):
    ADDED = "added"
    MODIFIED = "modified"
    REMOVED = "removed"


class PolicyVersion(TimestampedModel):
    __tablename__ = "policy_versions"
    __table_args__ = (UniqueConstraint("card_id", "version", name="uq_policy_card_version"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("credit_cards.id", ondelete="CASCADE"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    effective_date: Mapped[date] = mapped_column(Date)
    source_url: Mapped[str] = mapped_column(String(1000))
    document_hash: Mapped[str] = mapped_column(String(128), index=True)

    card: Mapped["CreditCard"] = relationship(back_populates="policy_versions")
    changes: Mapped[list["PolicyChange"]] = relationship(back_populates="policy_version")


class PolicyChange(TimestampedModel):
    __tablename__ = "policy_changes"

    id: Mapped[int] = mapped_column(primary_key=True)
    policy_version_id: Mapped[int] = mapped_column(ForeignKey("policy_versions.id", ondelete="CASCADE"), index=True)
    change_type: Mapped[PolicyChangeType] = mapped_column(Enum(PolicyChangeType))
    field_name: Mapped[str | None] = mapped_column(String(255))
    old_value: Mapped[str | None] = mapped_column(Text)
    new_value: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text)

    policy_version: Mapped[PolicyVersion] = relationship(back_populates="changes")
