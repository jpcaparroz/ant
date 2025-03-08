import sys
sys.path.append("src")

from notion_integration import Notion

async def clear() -> None:
    # notion = Notion()
    
    # query = {
    #     "and": [
    #         {"property": "Checkbox", "checkbox": {"equals": False}},
    #         {"property": "Clean", "checkbox": {"equals": True}},
    #         {"property": "Date", "date": {"before": datetime.now().strftime("%Y-%m-%d")}}
    #     ]
    # }

    # await notion.delete_pages(query)
    return

async def update_expenses() -> None:
    notion = Notion()
    await notion.update_expenses()

async def update_incomes() -> None:
    notion = Notion()
    await notion.update_incomes()


