from datetime import datetime
from typing import Optional
import re

from utils import get_env


DATABASE_ID: str = get_env('NOTION_DATABASE_ANT_ID')


class Ant():
    """TimeiT notion class representation
    """

    def __init__(self,
                 date: Optional[datetime],
                 spent: str,
                 description: str,
                 category: str,
                 payment: str,
                 installment: int,
                 installment_value: float,
                 value: float) -> None:
        
        self.database_id = DATABASE_ID
        self.date = date.strftime('%Y-%m-%d')
        self.spent = spent
        self.description = description
        self.category = category
        self.payment = payment
        self.installment = installment
        self.installment_value = installment_value
        self.value = value


    def to_dict(self) -> dict:
        body_as_dict: dict = {
            'DatabaseId': self.database_id,
            'Date': self.date,
            'Spent': self.spent,
            'Description': self.description,
            'Category': self.category,
            'Payment': self.payment,
            'Installment': self.installment,
            'Install_Value': self.installment_value,
            'Value': self.value
        }
        
        return body_as_dict


    def get_parent(self) -> dict:
        """Get notion parent expect json

        Returns:
            dict: Notion body properties to post a page
        """
        parent: dict = {
            "type": "database_id", 
            "database_id": self.database_id
        }
    
        return parent


    def notion_api_json(self) -> dict:
        """Get notion expect json

        Returns:
            dict: Notion json to post a page
        """
        body_json: dict = {
                        "date": {
                            "type": "date",
                            "date": {
                                "start": self.date,
                                "end": None,
                                "time_zone": None 
                            }
                        },
                        "spent": {
                            "id": "spent",
                            "type": "title",
                            "title": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": self.spent,
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
                                    "plain_text": self.spent,
                                    "href": None,
                                }
                            ],
                        },
                        "description": {
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
                        "category": {
                            "type": "select",
                            "select": {
                                "name": self.category,
                            }
                        },
                        "payment": {
                            "type": "select",
                            "select": {
                                "name": self.payment,
                            }
                        },
                        "installment": {
                            "type": "number",
                            "number": self.installment
                        },
                        "installment_value": {
                            "type": "number",
                            "number": self.installment_value
                        },
                        "value": {
                            "type": "number",
                            "number": self.value
                        }
                    }

        return body_json
