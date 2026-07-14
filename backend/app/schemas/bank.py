from pydantic import BaseModel


class BankSummary(BaseModel):
    name: str
