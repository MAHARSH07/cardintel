from decimal import Decimal

from pydantic import BaseModel, EmailStr

from app.models.user import EmploymentType, UserRole


class UserProfile(BaseModel):
    email: EmailStr
    full_name: str | None = None
    occupation: str | None = None
    monthly_income: Decimal | None = None
    state: str | None = None
    city: str | None = None
    is_student: bool = False
    employment_type: EmploymentType | None = None
    role: UserRole = UserRole.USER
