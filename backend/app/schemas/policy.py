from datetime import date

from pydantic import BaseModel


class PolicyVersionSummary(BaseModel):
    policy_date: date
    source_url: str
