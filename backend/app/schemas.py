from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(RegisterRequest):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CardSearchQuery(BaseModel):
    query: str | None = None
    bank: str | None = None
    ltf: bool | None = None
    network: str | None = None
    max_annual_fee: int | None = Field(default=None, ge=0)


class RecommendationRequest(BaseModel):
    salary: int = Field(gt=0)
    occupation: str
    monthly_spends: dict[str, int] = Field(default_factory=dict)
    interested_categories: list[str] = Field(default_factory=list)
    preferred_banks: list[str] = Field(default_factory=list)
    needs_ltf: bool = False
