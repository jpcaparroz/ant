from typing import List

from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from schemas.spent_schema import GetTreatedSpentSchema
from schemas.generic_schema import HttpDetail
from api.v1.data.crud import spent_crud as crud
from notion_integration.classes import AntNotion


router = APIRouter()


@router.post("/update", status_code=status.HTTP_201_CREATED, response_model=HttpDetail)
async def update_notion_from_database(db: AsyncSession = Depends(get_session)):
    spenties: List[GetTreatedSpentSchema] = await crud.get_treated_spenties_query(db)
    ant = AntNotion()
    
    try:
        await ant.post_pages(spenties)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error on post pages, error: {str(e)}')
    
    return HttpDetail(detail='Notion update sucessfully')


@router.delete("/delete_ant_pages", status_code=status.HTTP_201_CREATED, response_model=HttpDetail)
async def update_notion_from_database():
    ant = AntNotion()
    try:
        for i in range(30):
            await ant.delete_pages()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error on delete pages, error: {str(e)}')
    
    return HttpDetail(detail='Notion pages deleted sucessfully')
