from collections import defaultdict
from asyncio import gather, sleep
from typing import Literal,List

from notion_client import AsyncClient, Client

from src.utils import get_env
from src.notion_integration.classes import AntExpensesInput, AntExpenses


API_KEY: str = get_env("NOTION_API_TOKEN")
INCOMES_ID: str = get_env("NOTION_DATABASE_ANT_INCOMES_ID")
INCOMES_INPUT_ID: str = get_env("NOTION_DATABASE_ANT_INCOMES_INPUT_ID")
EXPENSES_ID: str = get_env("NOTION_DATABASE_ANT_EXPENSES_ID")
EXPENSES_INPUT_ID: str = get_env("NOTION_DATABASE_ANT_EXPENSES_INPUT_ID")
PERIODICAL_INCOMES_ID: str = get_env("NOTION_DATABASE_ANT_PERIODICAL_INCOMES_ID")
PERIODICAL_EXPENSES_ID: str = get_env("NOTION_DATABASE_ANT_PERIODICAL_EXPENSES_ID")
CATEGORY_ID: str = get_env("NOTION_DATABASE_ANT_CATEGORY_ID")
PAYMENT_ID: str = get_env("NOTION_DATABASE_ANT_PAYMENT_ID")


class Notion:
    """Notion notion class representation"""

    def __init__(self) -> None:
        self.client = Client(auth=API_KEY)
        self.async_client = AsyncClient(auth=API_KEY)

    async def get_notion_database_page_ids(
        self,
        database: Literal[
            "incomes_input",
            "incomes",
            "expenses_input",
            "expenses",
            "periodical_incomes",
            "periodical_expenses",
        ],
        query: dict = None,
    ):
        """Get all IDs of a database in Notion with a filter.

        Args:
            database (str): Database literal name.
            query_filter (dict): The filter to apply in the query.

        Returns:
            List[str]: A list with page IDs inside the database.
        """
        database_mapping = {
            "incomes_input": INCOMES_INPUT_ID,
            "incomes": INCOMES_ID,
            "expenses_input": EXPENSES_INPUT_ID,
            "expenses": EXPENSES_ID,
            "periodical_incomes": PERIODICAL_INCOMES_ID,
            "periodical_expenses": PERIODICAL_EXPENSES_ID,
            "category": CATEGORY_ID,
            "payment": PAYMENT_ID
        }
        database_id = database_mapping.get(database)

        if not database_id:
            raise ValueError(
                f"Unsupported database: {database}. Supported values are 'ant' and 'ant_input'."
            )

        all_responses: list = []

        try:
            query_response = (
                await self.async_client.databases.query(database_id, filter=query)
                if query
                else await self.async_client.databases.query(database_id)
            )

            all_responses.append(query_response)

            while query_response.get("has_more", False):
                next_cursor = query_response.get("next_cursor")
                if not next_cursor:
                    break

                query_response = (
                    await self.async_client.databases.query(
                        database_id, start_cursor=next_cursor, filter=query
                    )
                    if query
                    else await self.async_client.databases.query(
                        database_id, start_cursor=next_cursor
                    )
                )

                all_responses.append(query_response)

        except Exception as e:
            raise e

        page_ids: list = []
        for response in all_responses:
            for page in response.get("results", []):
                page_ids.append(page.get("id"))

        return page_ids

    async def get_database_select_options(
        self, database: Literal["ant", "ant_input"], property_name: str
    ) -> List[str]:
        """Get all select options of a database in Notion with a filter.

        Args:
            database (Literal['ant', 'ant_input']): Database literal name.

        Returns:
            List[str]: A list with all options inside the database.
        """
        database_mapping = {"ant": ANT_ID, "ant_input": ANT_INPUT_ID}
        database_id = database_mapping.get(database)

        if not database_id:
            raise ValueError(
                f"Unsupported database: {database}. Supported values are 'ant' and 'ant_input'."
            )

        query = await self.async_client.databases.retrieve(database_id)
        treated_result = (
            query.get("properties", {})
            .get(property_name, {})
            .get("select", {})
            .get("options", [])
        )
        if not treated_result:
            raise SystemError(f"No option created for the property: {property_name}.")
        else:
            return [result.get("name") for result in treated_result]

    async def delete_pages(self, database: Literal["ant", "ant_input"]) -> None:
        async def parallel_process(page_id):
            try:
                await self.async_client.pages.update(page_id, archived=True)
            except Exception as e:
                raise e

        page_ids: list = await self.get_notion_database_page_ids(database)
        if not page_ids:
            raise Exception("Pages not found")

        tasks = [parallel_process(page_id) for page_id in page_ids]
        await gather(*tasks)


    async def update_expenses(self) -> None:
        """ Update expenses from input
        """

        async def parallel_process(page_id: str):
            try:
                expenses_input = AntExpenses.from_dict(
                    await self.async_client.pages.retrieve(page_id)
                )
                ant = AntExpenses(
                    date=expenses_input.date,
                    spent=expenses_input.spent,
                    description=expenses_input.description,
                    category=expenses_input.category,
                    payment=expenses_input.payment,
                    installment=expenses_input.installment,
                    installment_value=expenses_input.installment_value,
                    value=expenses_input.value,
                )
                await self.async_client.pages.create(
                    parent=await ant.get_parent(),
                    properties=await ant.get_notion_json(),
                )
            except Exception as e:
                print(f"Error processing page {page_id}: {e}")

        page_ids = await self.get_notion_database_page_ids("expenses_input")
        for i in range(0, len(page_ids), 3):  # Processa 3 por vez
            tasks = [parallel_process(page_id) for page_id in page_ids[i : i + 3]]
            await gather(*tasks)
            await sleep(1)  # Aguarda 1 segundo entre os lotes

        # await self.delete_pages('ant_input')

    async def update_expenses_temp(self, expenses: list) -> None:
        """ Update expenses from input temporary
        """

        async def parallel_process(expense: AntExpenses):
            try:
                await self.async_client.pages.create(
                    parent=await expense.get_parent(),
                    properties=await expense.get_notion_json(),
                )
            except Exception as e:
                print(f"Error processing page {expense.name}: {str(e)}")

        for i in range(0, len(expenses), 3):  # Processa 3 por vez
            tasks = [parallel_process(expense) for expense in expenses[i : i + 3]]
            await gather(*tasks)
            await sleep(1)  # Aguarda 1 segundo entre os lotes
