from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas.expense import ExpenseRequestDto,ExpenseResponseDto
from app.models.expense import Expense
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.api_response import ApiResponse
from sqlalchemy import or_
from typing import Optional
from app.core.secure import get_current_user
from app.models.user import User
from sqlalchemy.orm import joinedload


expense_router=APIRouter(
    prefix="/expense",
    tags=["expense"]
)

# create expense

@expense_router.post("/" ,response_model=ApiResponse , status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense_request_dto:ExpenseRequestDto,
    db:Session=Depends(get_db),
    user:User = Depends(get_current_user)
    ):
    new_expense=Expense(
        title=expense_request_dto.title,
        description=expense_request_dto.description,
        amount=expense_request_dto.amount,
        user_id=user.id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return ApiResponse(status="success",message="Expense created successfully",data={
        "expense":ExpenseResponseDto.model_validate(new_expense)
    })

# get all expenses

@expense_router.get("/", response_model=ApiResponse)
async def get_all_expenses(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 5,
    search: Optional[str] = None
):
    query = db.query(Expense).options(joinedload(Expense.user))

    # Search
    if search:
        search_term = f"%{search}%"

        query = query.filter(
            or_(
                Expense.title.ilike(search_term),
                Expense.description.ilike(search_term)
            )
        )

    # Total records after search
    total = query.count()

    # Pagination
    expenses = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return ApiResponse(
        status="success",
        message="Expenses fetched successfully",
        data={
            "expenses": [
                ExpenseResponseDto.model_validate(expense)
                for expense in expenses
            ]
        },
        total=total
    )

# get expense by id

@expense_router.get("/{id}",response_model=ApiResponse)
async def get_expense_by_id(id:int,db:Session=Depends(get_db)):
    expense=db.query(Expense).filter(Expense.id==id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Expense not found")
    return ApiResponse(status="success",message="Expense fetched successfully",data={
        "expense":ExpenseResponseDto.model_validate(expense)
    })

# Update expense By Id

@expense_router.put("/{id}",response_model=ApiResponse)
async def update_expense_by_id(id:int,expense_request_dto:ExpenseRequestDto,db:Session=Depends(get_db)):
    expense=db.query(Expense).filter(Expense.id==id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Expense not found")
    
    expense.title=expense_request_dto.title
    expense.description=expense_request_dto.description
    expense.amount=expense_request_dto.amount

    db.commit()
    db.refresh(expense)

    return ApiResponse(status="success",message="Expense updated successfully",data={
        "expense":ExpenseResponseDto.model_validate(expense)
    })

# Delete expense By Id

@expense_router.delete("/{id}",response_model=ApiResponse)
async def delete_expense_by_id(id:int,db:Session=Depends(get_db)):
    expense=db.query(Expense).filter(Expense.id==id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Expense not found")
    db.delete(expense)
    db.commit()
    return ApiResponse(status="success",message="Expense deleted successfully",data={
        "expense":ExpenseResponseDto.model_validate(expense)
    })