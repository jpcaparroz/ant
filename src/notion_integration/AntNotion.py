from asyncio import gather
from typing import Literal
from typing import List

from notion_client import AsyncClient

from src.utils import get_env


API_KEY: str = get_env('NOTION_API_TOKEN')
ANT_ID: str = get_env('NOTION_DATABASE_ANT_ID')
ANT_INPUT_ID: str = get_env('NOTION_DATABASE_ANT_INPUT_ID')


class AntNotion():
    """AntNotion notion class representation
    """

    def __init__(self) -> None:
        self.client = AsyncClient(auth=API_KEY)


    async def get_database_page_ids(self, database: Literal['ant', 'ant_input']) -> List[str]:
        """Get all IDs of a database in Notion.

        Args:
            database (Literal['ant', 'ant_input']): Database literal name.

        Returns:
            List[str]: A list with all page IDs inside the database.
        """
        database_mapping = {
            'ant': ANT_ID,
            'ant_input': ANT_INPUT_ID
        }
        database_id = database_mapping.get(database)

        if not database_id:
            raise ValueError(f"Unsupported database: {database}. Supported values are 'ant' and 'ant_input'.")

        query = await self.client.databases.query(database_id)
        return [page.get('id') for page in query.get('results')]


    async def delete_pages(self, database: Literal['ant', 'ant_input']) -> None:
        async def parallel_process(page_id):
            try:
                await self.client.pages.update(page_id, archived=True)
            except Exception as e:
                raise e
        
        page_ids: list = await self.get_database_page_ids(database)
        if not page_ids:
            raise Exception('Pages not found')
        
        tasks = [parallel_process(page_id) for page_id in page_ids]
        await gather(*tasks)


    # async def post_pages(self, spenties) -> None:
    #     async def parallel_process(spent):
    #         try:
    #             ant = Ant(
    #                     spent.date,
    #                     spent.name,
    #                     spent.description,
    #                     spent.category_name,
    #                     spent.payment_name,
    #                     spent.installment_quantity,
    #                     spent.installment_value,
    #                     spent.value
    #                 )
    #             await self.client.pages.create(parent=ant.get_parent(), 
    #                                            properties=ant.notion_api_json())
    #         except Exception as e:
    #             raise e

    #     tasks = [parallel_process(spent) for spent in spenties]
    #     await gather(*tasks)


    async def update_ant_from_input(self) -> None:
        async def parallel_process(spent: Ant):
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
