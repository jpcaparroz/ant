from uuid import UUID

from typing import List

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.payment_model import PaymentModel
from schemas.payment_schema import UpdatePaymentSchema


# Payment
async def create_payment_query(payment: PaymentModel, db: AsyncSession):
    async with db as session:
        session.add(payment)
        await session.commit()
    
    return payment


async def get_payments_query(db: AsyncSession):
    async with db as session:
        query = select(PaymentModel)
        result = await session.execute(query)
        payments: List[PaymentModel] = result.scalars().unique().all()
        
    return payments


async def get_payment_query(payment_id: UUID, db: AsyncSession):
    async with db as session:
        query = select(PaymentModel).filter(PaymentModel.payment_id == payment_id)
        result = await session.execute(query)
        payment: PaymentModel = result.scalars().unique().one_or_none()
        
    return payment


async def get_payment_id_query(payment_name: str, db: AsyncSession):
    async with db as session:
        query = select(PaymentModel).filter(PaymentModel.name == payment_name)
        result = await session.execute(query)
        payment: PaymentModel = result.scalars().unique().one_or_none()
        
    return payment.payment_id


async def update_payment_query(payment_id: UUID,
                               updated_payment: UpdatePaymentSchema, 
                               db: AsyncSession):
    async with db as session:
        data = updated_payment.model_dump(exclude_none=True, exclude_unset=True)        
        query = update(PaymentModel).where(PaymentModel.payment_id == payment_id).values(data)
        await session.execute(query)
        await session.commit()
        
        response_query = select(PaymentModel).filter(PaymentModel.payment_id == payment_id)
        response = await session.execute(response_query)
        
        return response.scalars().unique().one_or_none()


async def delete_payment_query(payment_id: UUID, db: AsyncSession):
    async with db as session:
        query = delete(PaymentModel).where(PaymentModel.payment_id == payment_id)
        await session.execute(query)
        await session.commit()