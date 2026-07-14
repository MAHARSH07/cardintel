import enum
from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampedModel
from app.models.user import EmploymentType


class CardNetwork(str, enum.Enum):
    VISA = "visa"
    MASTERCARD = "mastercard"
    RUPAY = "rupay"
    AMEX = "amex"
    DINERS = "diners"


class CardStatus(str, enum.Enum):
    ACTIVE = "active"
    DISCONTINUED = "discontinued"
    PAUSED = "paused"
    UPCOMING = "upcoming"


class RewardCategory(str, enum.Enum):
    DINING = "dining"
    FUEL = "fuel"
    GROCERY = "grocery"
    ONLINE = "online"
    UTILITY = "utility"
    INSURANCE = "insurance"
    RENT = "rent"
    TRAVEL = "travel"
    GENERAL = "general"


class RewardType(str, enum.Enum):
    POINTS = "points"
    CASHBACK = "cashback"
    MILES = "miles"
    DISCOUNT = "discount"


class BenefitType(str, enum.Enum):
    LOUNGE = "lounge"
    MOVIES = "movies"
    GOLF = "golf"
    FUEL_SURCHARGE_WAIVER = "fuel_surcharge_waiver"
    CONCIERGE = "concierge"
    INSURANCE = "insurance"


class ChargeType(str, enum.Enum):
    LATE_FEE = "late_fee"
    FOREX_MARKUP = "forex_markup"
    CASH_WITHDRAWAL = "cash_withdrawal"
    FINANCE_CHARGE = "finance_charge"
    OTHER = "other"


class CreditCard(TimestampedModel):
    __tablename__ = "credit_cards"
    __table_args__ = (UniqueConstraint("bank_id", "name", "variant", name="uq_card_bank_name_variant"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id", ondelete="RESTRICT"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    network: Mapped[CardNetwork] = mapped_column(Enum(CardNetwork))
    variant: Mapped[str | None] = mapped_column(String(100))
    joining_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    annual_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    fee_waiver: Mapped[str | None] = mapped_column(Text)
    is_ltf: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    status: Mapped[CardStatus] = mapped_column(Enum(CardStatus), default=CardStatus.ACTIVE, index=True)
    launch_date: Mapped[date | None] = mapped_column(Date)

    bank: Mapped["Bank"] = relationship(back_populates="cards")
    eligibility: Mapped["Eligibility | None"] = relationship(back_populates="card", uselist=False)
    reward_structures: Mapped[list["RewardStructure"]] = relationship(back_populates="card")
    benefits: Mapped[list["Benefit"]] = relationship(back_populates="card")
    charges: Mapped[list["Charge"]] = relationship(back_populates="card")
    redemptions: Mapped[list["Redemption"]] = relationship(back_populates="card")
    policy_versions: Mapped[list["PolicyVersion"]] = relationship(back_populates="card")


class Eligibility(TimestampedModel):
    __tablename__ = "eligibility"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("credit_cards.id", ondelete="CASCADE"), unique=True)
    min_salary: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    employment_type: Mapped[EmploymentType | None] = mapped_column(Enum(EmploymentType))
    age_min: Mapped[int | None] = mapped_column(Integer)
    age_max: Mapped[int | None] = mapped_column(Integer)
    itr_required: Mapped[bool] = mapped_column(Boolean, default=False)
    credit_score_required: Mapped[int | None] = mapped_column(Integer)

    card: Mapped[CreditCard] = relationship(back_populates="eligibility")


class RewardStructure(TimestampedModel):
    __tablename__ = "reward_structures"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("credit_cards.id", ondelete="CASCADE"), index=True)
    category: Mapped[RewardCategory] = mapped_column(Enum(RewardCategory), index=True)
    reward_type: Mapped[RewardType] = mapped_column(Enum(RewardType))
    reward_rate: Mapped[Decimal] = mapped_column(Numeric(10, 4))
    reward_unit: Mapped[str] = mapped_column(String(100))

    card: Mapped[CreditCard] = relationship(back_populates="reward_structures")
    cap: Mapped["RewardCap | None"] = relationship(back_populates="reward_structure", uselist=False)


class RewardCap(TimestampedModel):
    __tablename__ = "reward_caps"

    id: Mapped[int] = mapped_column(primary_key=True)
    reward_structure_id: Mapped[int] = mapped_column(ForeignKey("reward_structures.id", ondelete="CASCADE"), unique=True)
    monthly_cap: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    quarterly_cap: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    annual_cap: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))

    reward_structure: Mapped[RewardStructure] = relationship(back_populates="cap")


class Benefit(TimestampedModel):
    __tablename__ = "benefits"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("credit_cards.id", ondelete="CASCADE"), index=True)
    benefit_type: Mapped[BenefitType] = mapped_column(Enum(BenefitType))
    description: Mapped[str] = mapped_column(Text)

    card: Mapped[CreditCard] = relationship(back_populates="benefits")


class Charge(TimestampedModel):
    __tablename__ = "charges"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("credit_cards.id", ondelete="CASCADE"), index=True)
    charge_type: Mapped[ChargeType] = mapped_column(Enum(ChargeType))
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    remarks: Mapped[str | None] = mapped_column(Text)

    card: Mapped[CreditCard] = relationship(back_populates="charges")


class Redemption(TimestampedModel):
    __tablename__ = "redemptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("credit_cards.id", ondelete="CASCADE"), index=True)
    reward_type: Mapped[RewardType] = mapped_column(Enum(RewardType))
    conversion_ratio: Mapped[str] = mapped_column(String(255))
    minimum_points: Mapped[int | None] = mapped_column(Integer)

    card: Mapped[CreditCard] = relationship(back_populates="redemptions")
