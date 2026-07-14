from pydantic import BaseModel


class CardSummary(BaseModel):
    name: str
    bank_name: str
