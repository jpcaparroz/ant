from uuid import UUID

from typing import List

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.spent_model import SpentModel
from schemas.spent_schema import UpdateSpentSchema


# Spent
async def create_spent_query(spent: SpentModel, db: AsyncSession):
    async with db as session:
        session.add(spent)
        await session.commit()
    
    return spent


async def get_spenties_query(db: AsyncSession):
    async with db as session:
        query = select(SpentModel)
        result = await session.execute(query)
        spenties: List[SpentModel] = result.scalars().unique().all()
        
    return spenties


async def get_spent_query(spent_id: UUID, db: AsyncSession):
    async with db as session:
        query = select(SpentModel).filter(SpentModel.spent_id == spent_id)
        result = await session.execute(query)
        spent: SpentModel = result.scalars().unique().one_or_none()
        
    return spent


async def update_spent_query(spent_id: UUID,
                             updated_spent: UpdateSpentSchema, 
                             db: AsyncSession):
    async with db as session:
        data = updated_spent.model_dump(exclude_none=True, exclude_unset=True)        
        query = update(SpentModel).where(SpentModel.spent_id == spent_id).values(data)
        await session.execute(query)
        await session.commit()
        
        response_query = select(SpentModel).filter(SpentModel.spent_id == spent_id)
        response = await session.execute(response_query)
        
        return response.scalars().unique().one_or_none()


async def delete_spent_query(spent_id: UUID, db: AsyncSession):
    async with db as session:
        query = delete(SpentModel).where(SpentModel.spent_id == spent_id)
        await session.execute(query)
        await session.commit()
