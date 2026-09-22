from datetime import datetime

from pydantic import BaseModel, Field


class ExpenseRequestDto(BaseModel):
    title: str = Field(
        ...,
        max_length=50,
        description="Title of the expense"
    )

    description: str = Field(
        ...,
        max_length=200,
        description="Description of the expense"
    )

    amount: float = Field(
        ...,
        gt=0,
        description="Expense amount"
    )

    show: bool = True

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Grocery",
                "description": "Groceries for the month",
                "amount": 100,
                "show": True
            }
        }
    }


class ExpenseResponseDto(ExpenseRequestDto):
    id: int = Field(
        ...,
        description="Expense ID"
    )

    created_at: datetime

    model_config = {
        "from_attributes": True
    }