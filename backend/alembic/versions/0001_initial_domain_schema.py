"""Create the initial CardIntel domain schema.

Revision ID: 0001_initial_domain
Revises:
Create Date: 2026-07-15
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_domain"
down_revision = None
branch_labels = None
depends_on = None


def timestamps() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    ]


def upgrade() -> None:
    employment_type = sa.Enum("SALARIED", "SELF_EMPLOYED", "STUDENT", "OTHER", name="employmenttype")
    source_type = sa.Enum("PRODUCT_PAGE", "TERMS_AND_CONDITIONS", "PDF", "WEBPAGE", name="sourcetype")
    card_network = sa.Enum("VISA", "MASTERCARD", "RUPAY", "AMEX", "DINERS", name="cardnetwork")
    card_status = sa.Enum("ACTIVE", "DISCONTINUED", "PAUSED", "UPCOMING", name="cardstatus")
    reward_category = sa.Enum("DINING", "FUEL", "GROCERY", "ONLINE", "UTILITY", "INSURANCE", "RENT", "TRAVEL", "GENERAL", name="rewardcategory")
    reward_type = sa.Enum("POINTS", "CASHBACK", "MILES", "DISCOUNT", name="rewardtype")
    benefit_type = sa.Enum("LOUNGE", "MOVIES", "GOLF", "FUEL_SURCHARGE_WAIVER", "CONCIERGE", "INSURANCE", name="benefittype")
    charge_type = sa.Enum("LATE_FEE", "FOREX_MARKUP", "CASH_WITHDRAWAL", "FINANCE_CHARGE", "OTHER", name="chargetype")
    policy_change_type = sa.Enum("ADDED", "MODIFIED", "REMOVED", name="policychangetype")
    sync_status = sa.Enum("PENDING", "RUNNING", "COMPLETED", "FAILED", name="syncstatus")

    op.create_table("banks", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(255), nullable=False), sa.Column("short_name", sa.String(50), nullable=False), sa.Column("official_website", sa.String(500), nullable=False), sa.Column("customer_care", sa.String(100)), *timestamps(), sa.UniqueConstraint("name"), sa.UniqueConstraint("short_name"))
    op.create_table("sources", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("bank_id", sa.Integer(), sa.ForeignKey("banks.id", ondelete="CASCADE"), nullable=False), sa.Column("url", sa.String(1000), nullable=False), sa.Column("source_type", source_type, nullable=False), sa.Column("last_checked", sa.DateTime(timezone=True)), sa.Column("etag", sa.String(255)), *timestamps(), sa.UniqueConstraint("url"))
    op.create_index("ix_sources_bank_id", "sources", ["bank_id"])
    op.create_table("credit_cards", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("bank_id", sa.Integer(), sa.ForeignKey("banks.id", ondelete="RESTRICT"), nullable=False), sa.Column("name", sa.String(255), nullable=False), sa.Column("network", card_network, nullable=False), sa.Column("variant", sa.String(100)), sa.Column("joining_fee", sa.Numeric(12, 2), nullable=False), sa.Column("annual_fee", sa.Numeric(12, 2), nullable=False), sa.Column("fee_waiver", sa.Text()), sa.Column("is_ltf", sa.Boolean(), nullable=False), sa.Column("status", card_status, nullable=False), sa.Column("launch_date", sa.Date()), *timestamps(), sa.UniqueConstraint("bank_id", "name", "variant", name="uq_card_bank_name_variant"))
    op.create_index("ix_credit_cards_bank_id", "credit_cards", ["bank_id"])
    op.create_index("ix_credit_cards_is_ltf", "credit_cards", ["is_ltf"])
    op.create_index("ix_credit_cards_status", "credit_cards", ["status"])
    op.create_table("eligibility", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("card_id", sa.Integer(), sa.ForeignKey("credit_cards.id", ondelete="CASCADE"), nullable=False), sa.Column("min_salary", sa.Numeric(12, 2)), sa.Column("employment_type", employment_type), sa.Column("age_min", sa.Integer()), sa.Column("age_max", sa.Integer()), sa.Column("itr_required", sa.Boolean(), nullable=False), sa.Column("credit_score_required", sa.Integer()), *timestamps(), sa.UniqueConstraint("card_id"))
    op.create_table("reward_structures", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("card_id", sa.Integer(), sa.ForeignKey("credit_cards.id", ondelete="CASCADE"), nullable=False), sa.Column("category", reward_category, nullable=False), sa.Column("reward_type", reward_type, nullable=False), sa.Column("reward_rate", sa.Numeric(10, 4), nullable=False), sa.Column("reward_unit", sa.String(100), nullable=False), *timestamps())
    op.create_index("ix_reward_structures_card_id", "reward_structures", ["card_id"])
    op.create_index("ix_reward_structures_category", "reward_structures", ["category"])
    op.create_table("reward_caps", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("reward_structure_id", sa.Integer(), sa.ForeignKey("reward_structures.id", ondelete="CASCADE"), nullable=False), sa.Column("monthly_cap", sa.Numeric(12, 2)), sa.Column("quarterly_cap", sa.Numeric(12, 2)), sa.Column("annual_cap", sa.Numeric(12, 2)), *timestamps(), sa.UniqueConstraint("reward_structure_id"))
    op.create_table("benefits", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("card_id", sa.Integer(), sa.ForeignKey("credit_cards.id", ondelete="CASCADE"), nullable=False), sa.Column("benefit_type", benefit_type, nullable=False), sa.Column("description", sa.Text(), nullable=False), *timestamps())
    op.create_index("ix_benefits_card_id", "benefits", ["card_id"])
    op.create_table("charges", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("card_id", sa.Integer(), sa.ForeignKey("credit_cards.id", ondelete="CASCADE"), nullable=False), sa.Column("charge_type", charge_type, nullable=False), sa.Column("amount", sa.Numeric(12, 2), nullable=False), sa.Column("remarks", sa.Text()), *timestamps())
    op.create_index("ix_charges_card_id", "charges", ["card_id"])
    op.create_table("redemptions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("card_id", sa.Integer(), sa.ForeignKey("credit_cards.id", ondelete="CASCADE"), nullable=False), sa.Column("reward_type", reward_type, nullable=False), sa.Column("conversion_ratio", sa.String(255), nullable=False), sa.Column("minimum_points", sa.Integer()), *timestamps())
    op.create_index("ix_redemptions_card_id", "redemptions", ["card_id"])
    op.create_table("policy_versions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("card_id", sa.Integer(), sa.ForeignKey("credit_cards.id", ondelete="CASCADE"), nullable=False), sa.Column("version", sa.Integer(), nullable=False), sa.Column("effective_date", sa.Date(), nullable=False), sa.Column("source_url", sa.String(1000), nullable=False), sa.Column("document_hash", sa.String(128), nullable=False), *timestamps(), sa.UniqueConstraint("card_id", "version", name="uq_policy_card_version"))
    op.create_index("ix_policy_versions_card_id", "policy_versions", ["card_id"])
    op.create_index("ix_policy_versions_document_hash", "policy_versions", ["document_hash"])
    op.create_table("policy_changes", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("policy_version_id", sa.Integer(), sa.ForeignKey("policy_versions.id", ondelete="CASCADE"), nullable=False), sa.Column("change_type", policy_change_type, nullable=False), sa.Column("field_name", sa.String(255)), sa.Column("old_value", sa.Text()), sa.Column("new_value", sa.Text()), sa.Column("summary", sa.Text(), nullable=False), *timestamps())
    op.create_index("ix_policy_changes_policy_version_id", "policy_changes", ["policy_version_id"])
    op.create_table("sync_jobs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id", ondelete="SET NULL")), sa.Column("started_at", sa.DateTime(timezone=True)), sa.Column("ended_at", sa.DateTime(timezone=True)), sa.Column("status", sync_status, nullable=False), sa.Column("cards_updated", sa.Integer(), nullable=False), sa.Column("errors", sa.JSON()), sa.Column("trigger", sa.String(30), nullable=False), *timestamps())
    op.create_index("ix_sync_jobs_source_id", "sync_jobs", ["source_id"])
    op.create_index("ix_sync_jobs_status", "sync_jobs", ["status"])


def downgrade() -> None:
    for table in ("sync_jobs", "policy_changes", "policy_versions", "redemptions", "charges", "benefits", "reward_caps", "reward_structures", "eligibility", "credit_cards", "sources", "banks"):
        op.drop_table(table)
    for enum_name in ("syncstatus", "policychangetype", "chargetype", "benefittype", "rewardtype", "rewardcategory", "cardstatus", "cardnetwork", "sourcetype", "employmenttype"):
        sa.Enum(name=enum_name).drop(op.get_bind(), checkfirst=True)
