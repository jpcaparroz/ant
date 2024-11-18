from asyncio import gather
from typing import List

from notion_client import AsyncClient

from schemas.spent_schema import GetTreatedSpentSchema
from notion_integration.classes import Ant
from utils import get_env


API_KEY: str = get_env('NOTION_API_TOKEN')
DATABASE_ID: str = get_env('NOTION_DATABASE_ANT_ID')


class AntNotion():
    """AntNotion notion class representation
    """

    def __init__(self) -> None:
        self.client = AsyncClient(auth=API_KEY)


    async def get_database_page_ids(self, database_id: str = DATABASE_ID) -> List[str]:
        """Get all ID's of a database in notion

        Args:
            database (str): Database ID

        Returns:
            List[str]: A list with all pages id inside database
        """
        query: dict = await self.client.databases.query(database_id)
        ids: list = [page_id.get('id') for page_id in query.get('results')]
        
        return ids


    async def delete_pages(self) -> None:
        async def parallel_process(page_id):
            try:
                await self.client.pages.update(page_id, archived=True)
            except Exception as e:
                raise e
        
        page_ids: list = await self.get_database_page_ids()
        if not page_ids:
            raise Exception('Pages not found')
        
        tasks = [parallel_process(page_id) for page_id in page_ids]
        await gather(*tasks)


    async def post_pages(self, spenties: List[GetTreatedSpentSchema]) -> None:
        async def parallel_process(spent):
            try:
                ant = Ant(
                        spent.date,
                        spent.name,
                        spent.description,
                        spent.category_name,
                        spent.payment_name,
                        spent.installment_quantity,
                        spent.installment_value,
                        spent.value
                    )
                await self.client.pages.create(parent=ant.get_parent(), 
                                            properties=ant.notion_api_json())
            except Exception as e:
                raise e

        tasks = [parallel_process(spent) for spent in spenties]
        await gather(*tasks)
