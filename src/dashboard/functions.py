from datetime import timedelta, datetime
from asyncio import gather, Semaphore

from src.notion_integration import Notion, DatabaseType
from src.notion_integration.classes import AntExpenses

NOW = datetime.now()


async def get_actual_month_total_value(database_id: DatabaseType) -> float:
    total_value: float = 0.0
    start_of_month = NOW.replace(day=1)
    start_of_next_month = (start_of_month + timedelta(days=32)).replace(day=1)

    query = {
        "and": [
            {
                "property": "Date",
                "date": {
                    "on_or_after": start_of_month.isoformat()
                }
            },
            {
                "property": "Date",
                "date": {
                    "before": start_of_next_month.isoformat()
                }
            }
        ]
    }

    notion = Notion()
    all_pages: list = await notion.get_notion_database_page_ids(database_id, query)
    
    async def parallel_process(page_id: str, semaphore: Semaphore) -> float:
        async with semaphore:
            try:
                page = await notion.async_client.pages.retrieve(page_id)
                return AntExpenses.from_dict(page).value
            except Exception as e:
                print(f"Error archiving page {page_id}: {str(e)}")

    if all_pages:
        semaphore = Semaphore(5)

        tasks = [parallel_process(page_id, semaphore) for page_id in all_pages]
        total_value = sum(await gather(*tasks))
    else:
        total_value = 0.0

    return total_value
