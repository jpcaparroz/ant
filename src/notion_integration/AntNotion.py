from collections import defaultdict
import asyncio
from asyncio import gather
from typing import Literal
from typing import List

from notion_client import AsyncClient, Client

from src.utils import get_env
from src.notion_integration.classes import Ant, AntInput, AntPayment, AntCategory


API_KEY: str = get_env('NOTION_API_TOKEN')
ANT_ID: str = get_env('NOTION_DATABASE_ANT_ID')
ANT_INPUT_ID: str = get_env('NOTION_DATABASE_ANT_INPUT_ID')
ANT_CATEGORY_ID: str = get_env('NOTION_DATABASE_ANT_CATEGORY_ID')
ANT_PAYMENT_ID: str = get_env('NOTION_DATABASE_ANT_PAYMENT_ID')


class AntNotion():
    """AntNotion notion class representation
    """

    def __init__(self) -> None:
        self.client = Client(auth=API_KEY)
        self.async_client = AsyncClient(auth=API_KEY)
        

    async def get_notion_database_page_ids(self, 
                                           database: Literal['ant', 'ant_input'], 
                                           query: dict = None):
        """Get all IDs of a database in Notion with a filter.

        Args:
            database (Literal['ant', 'ant_input']): Database literal name.
            query_filter (dict): The filter to apply in the query.

        Returns:
            List[str]: A list with page IDs inside the database.
        """
        database_mapping = {
            'ant': ANT_ID,
            'ant_input': ANT_INPUT_ID
        }
        database_id = database_mapping.get(database)

        if not database_id:
            raise ValueError(f"Unsupported database: {database}. Supported values are 'ant' and 'ant_input'.")
        
        all_responses: list = []

        try:
            query_response = await self.async_client.databases.query(database_id, filter=query) \
                             if query \
                             else \
                             await self.async_client.databases.query(database_id)        
                                                                                         
            all_responses.append(query_response)
            
            while query_response.get('has_more', False):
                next_cursor = query_response.get('next_cursor')
                if not next_cursor:
                    break
                
                query_response = await self.async_client.databases.query(database_id,
                                                                         start_cursor=next_cursor,
                                                                         filter=query) \
                                 if query \
                                 else \
                                 await self.async_client.databases.query(database_id,
                                                                         start_cursor=next_cursor)
                                
                all_responses.append(query_response)
            
        except Exception as e:
            raise e

        page_ids: list = []
        for response in all_responses:
            for page in response.get('results', []):
                page_ids.append(page.get('id'))
        
        return page_ids


    async def get_database_select_options(self, database: Literal['ant', 'ant_input'],
                                                property_name: str) -> List[str]:
        """Get all select options of a database in Notion with a filter.

        Args:
            database (Literal['ant', 'ant_input']): Database literal name.

        Returns:
            List[str]: A list with all options inside the database.
        """
        database_mapping = {
            'ant': ANT_ID,
            'ant_input': ANT_INPUT_ID
        }
        database_id = database_mapping.get(database)

        if not database_id:
            raise ValueError(f"Unsupported database: {database}. Supported values are 'ant' and 'ant_input'.")

    
        query = await self.async_client.databases.retrieve(database_id)
        treated_result = query.get('properties', {})\
                              .get(property_name, {})\
                              .get('select', {})\
                              .get('options', [])
        if not treated_result:
            raise SystemError(f"No option created for the property: {property_name}.")
        else:
            return [result.get('name') for result in treated_result]


    async def delete_pages(self, database: Literal['ant', 'ant_input']) -> None:
        async def parallel_process(page_id):
            try:
                await self.async_client.pages.update(page_id, archived=True)
            except Exception as e:
                raise e
        
        page_ids: list = await self.get_notion_database_page_ids(database)
        if not page_ids:
            raise Exception('Pages not found')
        
        tasks = [parallel_process(page_id) for page_id in page_ids]
        await gather(*tasks)


    async def update_ant(self) -> None:
        async def parallel_process(page_id: str):
            try:
                ant_input = AntInput.from_dict(await self.async_client.pages.retrieve(page_id))
                ant = Ant(
                    date=ant_input.date,
                    spent=ant_input.spent,
                    description=ant_input.description,
                    category=ant_input.category,
                    payment=ant_input.payment,
                    installment=ant_input.installment,
                    installment_value=ant_input.installment_value,
                    value=ant_input.value
                )
                await self.async_client.pages.create(
                    parent=await ant.get_parent(),
                    properties=await ant.get_notion_json()
                )
            except Exception as e:
                print(f"Error processing page {page_id}: {e}")

        page_ids = await self.get_notion_database_page_ids('ant_input')
        for i in range(0, len(page_ids), 3):  # Processa 3 por vez
            tasks = [parallel_process(page_id) for page_id in page_ids[i:i+3]]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)  # Aguarda 1 segundo entre os lotes

        # await self.delete_pages('ant_input')


    async def update_ant_payment(self) -> None:
        async def parallel_process(payment: str, page_ids: list):
            try:
                monthly_ants = defaultdict(list)
                final_value_per_month = defaultdict(float)
                count_per_month = defaultdict(int)

                for page_id in page_ids:
                    ant: Ant = Ant.from_dict(await self.async_client.pages.retrieve(page_id))
                    month_key = ant.date.strftime("%Y-%m")
                    
                    monthly_ants[month_key].append(ant)
                    final_value_per_month[month_key] += ant.value
                    count_per_month[month_key] += 1

                for month, ants in monthly_ants.items():
                    ant_payment = AntPayment(
                        period=month,
                        payment=payment,
                        spents=count_per_month[month],
                        value=round(final_value_per_month[month], 2)
                    )
                    await self.async_client.pages.create(parent= await ant_payment.get_parent(),
                                                         properties= await ant_payment.get_notion_json())
            except Exception:
                raise

        payment_page_ids: dict = {}
        payment_names: list = await self.get_database_select_options('ant', 'payment')
        for payment in payment_names:
            query: dict = {
                "property": "payment",
                "select": {"equals": payment}
            }
            page_ids = await self.get_notion_database_page_ids('ant', query)
            payment_page_ids[payment] = page_ids

        tasks: list = [parallel_process(key, value) for key, value in payment_page_ids.items()]
        await gather(*tasks)


    async def update_ant_category(self) -> None:
        async def parallel_process(category: str, page_ids: list):
            try:
                monthly_ants = defaultdict(list)
                final_value_per_month = defaultdict(float)
                count_per_month = defaultdict(int)

                for page_id in page_ids:
                    ant: Ant = Ant.from_dict(await self.async_client.pages.retrieve(page_id))
                    month_key = ant.date.strftime("%Y-%m")
                    
                    monthly_ants[month_key].append(ant)
                    final_value_per_month[month_key] += ant.value
                    count_per_month[month_key] += 1

                for month, ants in monthly_ants.items():
                    ant_category = AntCategory(
                        period=month,
                        category=category,
                        spents=count_per_month[month],
                        value=round(final_value_per_month[month], 2)
                    )
                    await self.async_client.pages.create(parent= await ant_category.get_parent(),
                                                         properties= await ant_category.get_notion_json())
            except Exception:
                raise

        category_page_ids: dict = {}
        category_names: list = await self.get_database_select_options('ant', 'category')
        for category in category_names:
            query: dict = {
                "property": "category",
                "select": {"equals": category}
            }
            page_ids = await self.get_notion_database_page_ids('ant', query)
            category_page_ids[category] = page_ids

        tasks: list = [parallel_process(key, value) for key, value in category_page_ids.items()]
        await gather(*tasks)
