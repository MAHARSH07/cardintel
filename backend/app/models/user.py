import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedModel


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    USER = "user"


class EmploymentType(str, enum.Enum):
    SALARIED = "salaried"
    SELF_EMPLOYED = "self_employed"
    STUDENT = "student"
    OTHER = "other"


class User(TimestampedModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
    full_name: Mapped[str | None] = mapped_column(String(255))
    occupation: Mapped[str | None] = mapped_column(String(120))
    monthly_income: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    state: Mapped[str | None] = mapped_column(String(120))
    city: Mapped[str | None] = mapped_column(String(120))
    is_student: Mapped[bool] = mapped_column(Boolean, default=False)
    employment_type: Mapped[EmploymentType | None] = mapped_column(Enum(EmploymentType))
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
