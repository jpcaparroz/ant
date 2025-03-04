from asyncio import gather, sleep, Semaphore
from typing import Literal
from enum import Enum

from notion_client import AsyncClient, Client

from src.utils import get_env
from src.notion_integration.classes import (
    AntExpensesInput,
    AntExpenses,
    AntIncomesInput,
    AntIncomes,
)


API_KEY: str = get_env("NOTION_API_TOKEN")
INCOMES_ID: str = get_env("NOTION_DATABASE_ANT_INCOMES_ID")
INCOMES_INPUT_ID: str = get_env("NOTION_DATABASE_ANT_INCOMES_INPUT_ID")
EXPENSES_ID: str = get_env("NOTION_DATABASE_ANT_EXPENSES_ID")
EXPENSES_INPUT_ID: str = get_env("NOTION_DATABASE_ANT_EXPENSES_INPUT_ID")
PERIODICAL_INCOMES_ID: str = get_env("NOTION_DATABASE_ANT_PERIODICAL_INCOMES_ID")
PERIODICAL_EXPENSES_ID: str = get_env("NOTION_DATABASE_ANT_PERIODICAL_EXPENSES_ID")
CATEGORY_ID: str = get_env("NOTION_DATABASE_ANT_CATEGORY_ID")
PAYMENT_ID: str = get_env("NOTION_DATABASE_ANT_PAYMENT_ID")


class DatabaseType(Enum):
    INCOMES_INPUT = "incomes_input"
    INCOMES = "incomes"
    EXPENSES_INPUT = "expenses_input"
    EXPENSES = "expenses"
    PERIODICAL_INCOMES = "periodical_incomes"
    PERIODICAL_EXPENSES = "periodical_expenses"


class Notion:
    """Notion notion class representation"""

    def __init__(self) -> None:
        self.client = Client(auth=API_KEY)
        self.async_client = AsyncClient(auth=API_KEY)

    async def get_notion_database_page_ids(
        self,
        database: DatabaseType,
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
            "payment": PAYMENT_ID,
        }
        database_id = database_mapping.get(database)

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

    async def delete_pages(self, database: DatabaseType) -> None:
        async def parallel_process(page_id: str, semaphore: Semaphore):
            async with semaphore:
                try:
                    await self.async_client.pages.update(page_id, archived=True)
                except Exception as e:
                    print(f"Error archiving page {page_id}: {e}")

        page_ids: list = await self.get_notion_database_page_ids(database)
        if not page_ids:
            raise Exception("Pages not found")

        semaphore = Semaphore(5)

        tasks = [parallel_process(page_id, semaphore) for page_id in page_ids]
        await gather(*tasks)

    async def update_expenses(self) -> None:
        """Update expenses from input"""

        async def parallel_process(page_id: str, semaphore: Semaphore):
            async with semaphore:
                try:
                    page_data = await self.async_client.pages.retrieve(page_id)
                    expenses_input = AntExpensesInput.from_dict(page_data)

                    ant = AntExpenses(
                        date=expenses_input.date,
                        name=expenses_input.name,
                        description=expenses_input.description,
                        category=expenses_input.category,
                        payment=expenses_input.payment,
                        installment=expenses_input.installment,
                        value=expenses_input.value,
                    )

                    await self.async_client.pages.create(
                        parent=await ant.get_parent(),
                        properties=await ant.get_notion_json(),
                        icon=await ant.get_icon(),
                    )

                except Exception as e:
                    print(f"Error processing page {page_id}: {e}")

        page_ids = await self.get_notion_database_page_ids("expenses_input")

        semaphore = Semaphore(5)

        tasks = [parallel_process(page_id, semaphore) for page_id in page_ids]
        await gather(*tasks)

        await self.delete_pages("expenses_input")

    async def update_incomes(self) -> None:
        """Update incomes from input"""

        async def parallel_process(page_id: str, semaphore: Semaphore):
            async with semaphore:
                try:
                    page_data = await self.async_client.pages.retrieve(page_id)
                    incomes_input = AntIncomesInput.from_dict(page_data)

                    ant = AntIncomes(
                        date=incomes_input.date,
                        name=incomes_input.name,
                        description=incomes_input.description,
                        category=incomes_input.category,
                        payment=incomes_input.payment,
                        value=incomes_input.value
                    )

                    await self.async_client.pages.create(
                        parent=await ant.get_parent(),
                        properties=await ant.get_notion_json(),
                        icon=await ant.get_icon(),
                    )

                except Exception as e:
                    print(f"Error processing page {page_id}: {e}")

        page_ids = await self.get_notion_database_page_ids("incomes_input")

        semaphore = Semaphore(5)

        tasks = [parallel_process(page_id, semaphore) for page_id in page_ids]
        await gather(*tasks)

        await self.delete_pages("incomes_input")

    async def update_incomes_temp(self, incomes: list) -> None:
        """Update incomes from input temporary"""

        async def parallel_process(income: AntIncomes, semaphore: Semaphore):
            async with semaphore:
                try:
                    await self.async_client.pages.create(
                        parent=await income.get_parent(),
                        properties=await income.get_notion_json(),
                        icon=await income.get_icon(),
                    )
                except Exception as e:
                    print(f"Error processing page {income.name}: {str(e)}")

        semaphore = Semaphore(5)

        tasks = [parallel_process(income, semaphore) for income in incomes]
        await gather(*tasks)
