from uuid import UUID

from typing import List

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_model import UserModel
from schemas.user_schema import UpdateUserSchema


# User
async def create_user_query(user: UserModel, db: AsyncSession):
    async with db as session:
        session.add(user)
        await session.commit()
    
    return user


async def get_users_query(db: AsyncSession):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserModel] = result.scalars().unique().all()
        
    return users


async def get_user_query(user_id: UUID, db: AsyncSession):
    async with db as session:
        query = select(UserModel).filter(UserModel.user_id == user_id)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()
        
    return user


async def update_user_query(user_id: UUID, 
                            updated_user: UpdateUserSchema, 
                            db: AsyncSession):
    async with db as session:
        data = updated_user.model_dump(exclude_none=True, exclude_unset=True)        
        query = update(UserModel).where(UserModel.user_id == user_id).values(data)
        await session.execute(query)
        await session.commit()
        
        response_query = select(UserModel).filter(UserModel.user_id == user_id)
        response = await session.execute(response_query)
        
        return response.scalars().unique().one_or_none()


async def delete_user_query(user_id: UUID, db: AsyncSession):
    async with db as session:
        query = delete(UserModel).where(UserModel.user_id == user_id)
        await session.execute(query)
        await session.commit()