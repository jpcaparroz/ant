from datetime import datetime
from typing import Optional, Dict
import json

from utils import get_env, get_nested_value


DATABASE_ID: str = get_env('NOTION_DATABASE_ANT_EXPENSES_ID')
DATE_FORMAT: str = '%Y-%m-%d'


class AntExpenses():
    """Expenses class representation
    """

    def __init__(self,
                 date: datetime,
                 name: str,
                 description: str,
                 category: str,
                 payment: str,
                 installment: int,
                 value: float,
                 installment_value: float = 0.0,
                 notion_id: Optional[int] = None) -> None:
        
        self.database_id = DATABASE_ID
        self.date = date if isinstance(date, datetime) else datetime.strptime(date, DATE_FORMAT)
        self.name = name
        self.description = description if description else ''
        self.category = category
        self.payment = payment
        self.installment = installment
        self.installment_value = installment_value
        self.value = value
        self.notion_id = notion_id


    def to_dict(self) -> dict:
        body_as_dict: dict = {
            'DatabaseId': self.database_id,
            'ID': self.notion_id,
            'Name': self.name,
            'Date': self.date,
            'Description': self.description,
            'Category': self.category,
            'Payment': self.payment,
            'Installment': self.installment,
            'Installment Value': self.installment_value,
            'Value': self.value
        }
        
        return body_as_dict


    async def get_parent(self) -> dict:
        """Get notion parent expect json

        Returns:
            dict: Notion body properties to post a page
        """
        parent: dict = {
            "type": "database_id", 
            "database_id": self.database_id
        }
    
        return parent


    @classmethod
    def from_json(cls, ant_as_json: str) -> 'AntExpenses':
        """ Alternative constructor

        :param ant_as_json: ant as JSON string
        :return: Ant, an instance of this class
        """
        ant_as_dict = json.loads(ant_as_json)
        return cls.from_dict(ant_as_dict)


    @classmethod
    def from_dict(cls, ant_as_dict: Dict) -> 'AntExpenses':
        """ Alternative constructor

        :param ant_as_dict: ant as dict
        :return: Ant, an instance of this class
        """
        properties: dict = ant_as_dict['properties']
        treated_date = datetime.strptime(get_nested_value(properties, 'Date', 'date', 'start'), DATE_FORMAT)
        
        return cls(
            notion_id=get_nested_value(properties, 'id', 'unique_id', 'number'),
            date=treated_date,
            name=get_nested_value(properties, 'Name', 'title', 0, 'text', 'content'),
            description=get_nested_value(properties, 'Description', 'rich_text', 0, 'text', 'content'),
            category=get_nested_value(properties, 'Category', 'relation', 0, 'id'),
            payment=get_nested_value(properties, 'Payment', 'relation', 0, 'id'),
            installment=get_nested_value(properties, 'Installment', 'number'),
            value=get_nested_value(properties, 'Value', 'number'))
    

    async def get_icon(self) -> dict:
        """Get notion icon dict

        Returns:
            dict: Notion json icon
        """
        body_json: dict = {
            "type": "external",
            "external": {
                "url": "https://www.notion.so/icons/share_gray.svg"
            }
        }

        return body_json

    async def get_notion_json(self) -> dict:
        """Get notion expect json

        Returns:
            dict: Notion json to post a page
        """
        body_json: dict = {
                        "Date": {
                            "type": "date",
                            "date": {
                                "start": self.date.strftime(DATE_FORMAT),
                                "end": None,
                                "time_zone": None 
                            }
                        },
                        "Name": {
                            "type": "title",
                            "title": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": self.name,
                                        "link": None
                                    },
                                    "annotations": {
                                        "bold": False,
                                        "italic": False,
                                        "strikethrough": False,
                                        "underline": False,
                                        "code": False,
                                        "color": "default",
                                    },
                                    "plain_text": self.name,
                                    "href": None,
                                }
                            ],
                        },
                        "Description": {
                            "type": "rich_text",
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": self.description,
                                        "link": None
                                    },
                                    "annotations": {
                                        "bold": False,
                                        "italic": False,
                                        "strikethrough": False,
                                        "underline": False,
                                        "code": False,
                                        "color": "default"
                                    },
                                    "plain_text": self.description,
                                    "href": None
                                }
                            ]
                        },
                        "Category": {
                            "type": "relation",
                            "relation": [
                                {
                                    "id": self.category,
                                }
                            ]
                        },
                        "Payment": {
                            "type": "relation",
                            "relation": [
                                {
                                    "id": self.payment,
                                }
                            ]
                        },
                        "Installment": {
                            "type": "number",
                            "number": self.installment
                        },
                        "Value": {
                            "type": "number",
                            "number": self.value
                        }
                    }

        return body_json
