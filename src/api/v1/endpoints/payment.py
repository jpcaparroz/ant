from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.deps import get_current_user
from core.deps import get_session
from models.payment_model import PaymentModel
from schemas.payment_schema import CreatePaymentSchema
from schemas.payment_schema import GetPaymentSchema
from schemas.payment_schema import UpdatePaymentSchema
from schemas.generic_schema import HttpDetail
from api.v1.data.crud import payment_crud as crud
from api.v1.data.crud import user_crud
from api.v1.data.template.payment_template import CreatePaymentBody
from api.v1.data.template.payment_template import UpdatePaymentBody


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=GetPaymentSchema)
async def create_payment(payment: CreatePaymentSchema = CreatePaymentBody, 
                          db: AsyncSession = Depends(get_session)):
    new_payment: PaymentModel = PaymentModel(**payment.model_dump())

    user_search = await user_crud.get_user_query(payment.user_id, db)
    if not user_search:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'User not found')

    try:
        response = await crud.create_payment_query(new_payment, db)
        return response

    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Payment with this name already registered')


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[GetPaymentSchema])
async def get_payments(db: AsyncSession = Depends(get_session)):
    return await crud.get_payments_query(db)


@router.get("/{payment_id}", status_code=status.HTTP_200_OK, response_model=GetPaymentSchema)
async def get_payment(payment_id: UUID, db: AsyncSession = Depends(get_session)):
    response = await crud.get_payment_query(payment_id, db)
    if not response:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Payment not found')
    
    return response


@router.patch("/{payment_id}", status_code=status.HTTP_202_ACCEPTED, response_model=GetPaymentSchema)
async def update_payment(payment_id: UUID, payment: UpdatePaymentSchema = UpdatePaymentBody, 
                      db: AsyncSession = Depends(get_session)):
    try:
        response = await crud.update_payment_query(payment_id, payment, db)
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Payment name conflict')

    if not response:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Payment not found')

    return response


@router.delete("/{payment_id}", status_code=status.HTTP_200_OK, response_model=HttpDetail)
async def delete_payment(payment_id: UUID, db: AsyncSession = Depends(get_session)):
    check_payment = await crud.get_payment_query(payment_id, db)
    if not check_payment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Payment not found')
    
    await crud.delete_payment_query(payment_id, db)
    
    return HttpDetail(detail= 'Payment deleted successfully')

