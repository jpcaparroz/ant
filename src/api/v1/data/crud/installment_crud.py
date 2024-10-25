from uuid import UUID

from typing import List

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.installment_model import InstallmentModel
from schemas.installment_schema import UpdateInstallmentSchema


async def create_installment_query(installment: InstallmentModel, db: AsyncSession):
    async with db as session:
        session.add(installment)
        await session.commit()
    
    return installment


async def get_installments_query(db: AsyncSession):
    async with db as session:
        query = select(InstallmentModel)
        result = await session.execute(query)
        installments: List[InstallmentModel] = result.scalars().unique().all()
        
    return installments


async def get_installment_query(installment_id: UUID, db: AsyncSession):
    async with db as session:
        query = select(InstallmentModel).filter(InstallmentModel.installment_id == installment_id)
        result = await session.execute(query)
        installment: InstallmentModel = result.scalars().unique().one_or_none()
        
    return installment


async def update_installment_query(installment_id: UUID,
                                   updated_installment: UpdateInstallmentSchema, 
                                   db: AsyncSession):
    async with db as session:
        data = updated_installment.model_dump(exclude_none=True, exclude_unset=True)        
        query = update(InstallmentModel).where(InstallmentModel.installment_id == installment_id).values(data)
        await session.execute(query)
        await session.commit()
        
        response_query = select(InstallmentModel).filter(InstallmentModel.installment_id == installment_id)
        response = await session.execute(response_query)
        
        return response.scalars().unique().one_or_none()


async def delete_installment_query(installment_id: UUID, db: AsyncSession):
    async with db as session:
        query = delete(InstallmentModel).where(InstallmentModel.installment_id == installment_id)
        await session.execute(query)
        await session.commit()
