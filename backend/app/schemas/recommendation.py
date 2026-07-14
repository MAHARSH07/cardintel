from pydantic import BaseModel


class RecommendationInput(BaseModel):
    salary: int
    occupation: str
