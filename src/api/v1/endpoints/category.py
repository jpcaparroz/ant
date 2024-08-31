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
from models.category_model import CategoryModel
from schemas.category_schema import CreateCategorySchema
from schemas.category_schema import GetCategorySchema
from schemas.category_schema import UpdateCategorySchema
from schemas.generic_schema import HttpDetail
from api.v1.data.crud import category_crud as crud
from api.v1.data.crud import user_crud
from api.v1.data.template.category_template import CreateCategoryBody
from api.v1.data.template.category_template import UpdateCategoryBody


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=GetCategorySchema)
async def create_category(category: CreateCategorySchema = CreateCategoryBody,
                          db: AsyncSession = Depends(get_session)):
    new_category: CategoryModel = CategoryModel(**category.model_dump())

    user_search = await user_crud.get_user_query(category.user_id, db)
    if not user_search:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'User not found')

    try:
        response = await crud.create_category_query(new_category, db)
        return response

    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Category with this name already registered')


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[GetCategorySchema])
async def get_categories(db: AsyncSession = Depends(get_session)):
    return await crud.get_categories_query(db)


@router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=GetCategorySchema)
async def get_category(category_id: UUID, db: AsyncSession = Depends(get_session)):
    response = await crud.get_category_query(category_id, db)
    if not response:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Category not found')
    
    return response


@router.patch("/{category_id}", status_code=status.HTTP_202_ACCEPTED, response_model=GetCategorySchema)
async def update_category(category_id: UUID, category: UpdateCategorySchema = UpdateCategoryBody, 
                      db: AsyncSession = Depends(get_session)):
    try:
        response = await crud.update_category_query(category_id, category, db)
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Category name conflict')

    if not response:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Category not found')

    return response


@router.delete("/{category_id}", status_code=status.HTTP_200_OK, response_model=HttpDetail)
async def delete_category(category_id: UUID, db: AsyncSession = Depends(get_session)):
    check_category = await crud.get_category_query(category_id, db)
    if not check_category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Category not found')
    
    await crud.delete_category_query(category_id, db)
    
    return HttpDetail(detail= 'Category deleted successfully')

