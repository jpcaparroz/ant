from uuid import UUID

from typing import List

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.category_model import CategoryModel
from schemas.category_schema import UpdateCategorySchema


# Category
async def create_category_query(category: CategoryModel, db: AsyncSession):
    async with db as session:
        session.add(category)
        await session.commit()
    
    return category


async def get_categories_query(db: AsyncSession):
    async with db as session:
        query = select(CategoryModel)
        result = await session.execute(query)
        categories: List[CategoryModel] = result.scalars().unique().all()
        
    return categories


async def get_category_id_query(category_name: str, db: AsyncSession):
    async with db as session:
        query = select(CategoryModel).filter(CategoryModel.name == category_name)
        result = await session.execute(query)
        category: CategoryModel = result.scalars().unique().one_or_none()
        
    return category.category_id


async def get_category_query(category_id: UUID, db: AsyncSession):
    async with db as session:
        query = select(CategoryModel).filter(CategoryModel.category_id == category_id)
        result = await session.execute(query)
        category: CategoryModel = result.scalars().unique().one_or_none()
        
    return category


async def update_category_query(category_id: UUID,
                                updated_category: UpdateCategorySchema, 
                                db: AsyncSession):
    async with db as session:
        data = updated_category.model_dump(exclude_none=True, exclude_unset=True)        
        query = update(CategoryModel).where(CategoryModel.category_id == category_id).values(data)
        await session.execute(query)
        await session.commit()
        
        response_query = select(CategoryModel).filter(CategoryModel.category_id == category_id)
        response = await session.execute(response_query)
        
        return response.scalars().unique().one_or_none()


async def delete_category_query(category_id: UUID, db: AsyncSession):
    async with db as session:
        query = delete(CategoryModel).where(CategoryModel.category_id == category_id)
        await session.execute(query)
        await session.commit()