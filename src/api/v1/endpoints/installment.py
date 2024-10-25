from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_current_user
from core.deps import get_session
from models.installment_model import InstallmentModel
from schemas.installment_schema import BaseInstallmentSchema
from schemas.installment_schema import UpdateInstallmentSchema
from schemas.installment_schema import GetInstallmentSchema
from schemas.generic_schema import HttpDetail
from api.v1.data.crud import installment_crud as crud
from api.v1.data.crud import spent_crud
from api.v1.data.template.installment_template import CreateInstallmentBody
from api.v1.data.template.installment_template import UpdateInstallmentBody


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=GetInstallmentSchema)
async def create_installment(installment: BaseInstallmentSchema = CreateInstallmentBody, 
                             db: AsyncSession = Depends(get_session)):
    new_installment: InstallmentModel = InstallmentModel(**installment.model_dump())

    spent_search = await spent_crud.get_spent_query(new_installment.spent_id, db)
    if not spent_search:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Spent not found')

    response = await crud.create_installment_query(new_installment, db)
    return response


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[GetInstallmentSchema])
async def get_installments(db: AsyncSession = Depends(get_session)):
    return await crud.get_installments_query(db)


@router.get("/{installment_id}", status_code=status.HTTP_200_OK, response_model=GetInstallmentSchema)
async def get_installment(installment_id: UUID, db: AsyncSession = Depends(get_session)):
    response = await crud.get_installment_query(installment_id, db)
    if not response:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Installment not found')
    
    return response


@router.patch("/{installment_id}", status_code=status.HTTP_202_ACCEPTED, response_model=GetInstallmentSchema)
async def update_installment(installment_id: UUID, installment: UpdateInstallmentSchema = UpdateInstallmentBody, 
                             db: AsyncSession = Depends(get_session)):
    response = await crud.update_installment_query(installment_id, installment, db)
    if not response:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Installment not found')

    return response


@router.delete("/{installment_id}", status_code=status.HTTP_200_OK, response_model=HttpDetail)
async def delete_installment(installment_id: UUID, db: AsyncSession = Depends(get_session)):
    check_installment = await crud.get_installment_query(installment_id, db)
    if not check_installment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Installment not found')
    
    await crud.delete_installment_query(installment_id, db)
    
    return HttpDetail(detail= 'Installment deleted successfully')
