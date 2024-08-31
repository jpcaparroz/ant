from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_current_user
from core.deps import get_session
from models.spent_model import SpentModel
from schemas.spent_schema import CreateSpentSchema
from schemas.spent_schema import GetSpentSchema
from schemas.spent_schema import UpdateSpentSchema
from schemas.generic_schema import HttpDetail
from api.v1.data.crud import spent_crud as crud
from api.v1.data.crud import category_crud
from api.v1.data.crud import payment_crud
from api.v1.data.crud import user_crud
from api.v1.data.template.spent_template import CreateSpentBody
from api.v1.data.template.spent_template import UpdateSpentBody


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=GetSpentSchema)
async def create_spent(spent: CreateSpentSchema = CreateSpentBody, 
                          db: AsyncSession = Depends(get_session)):
    new_spent: SpentModel = SpentModel(**spent.model_dump())

    user_search = await user_crud.get_user_query(spent.user_id, db)
    if not user_search:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'User not found')

    category_search = await category_crud.get_category_query(spent.category_id, db)
    if not category_search:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Category not found')

    payment_search = await payment_crud.get_payment_query(spent.payment_id, db)
    if not payment_search:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Payment not found')

    response = await crud.create_spent_query(new_spent, db)
    return response


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[GetSpentSchema])
async def get_spenties(db: AsyncSession = Depends(get_session)):
    return await crud.get_spenties_query(db)


@router.get("/{spent_id}", status_code=status.HTTP_200_OK, response_model=GetSpentSchema)
async def get_spent(spent_id: UUID, db: AsyncSession = Depends(get_session)):
    response = await crud.get_spent_query(spent_id, db)
    if not response:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Spent not found')
    
    return response


@router.patch("/{spent_id}", status_code=status.HTTP_202_ACCEPTED, response_model=GetSpentSchema)
async def update_spent(spent_id: UUID, spent: UpdateSpentSchema = UpdateSpentBody, 
                      db: AsyncSession = Depends(get_session)):
    response = await crud.update_spent_query(spent_id, spent, db)
    if not response:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Spent not found')

    return response


@router.delete("/{spent_id}", status_code=status.HTTP_200_OK, response_model=HttpDetail)
async def delete_spent(spent_id: UUID, db: AsyncSession = Depends(get_session)):
    check_spent = await crud.get_spent_query(spent_id, db)
    if not check_spent:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Spent not found')
    
    await crud.delete_spent_query(spent_id, db)
    
    return HttpDetail(detail= 'Spent deleted successfully')
