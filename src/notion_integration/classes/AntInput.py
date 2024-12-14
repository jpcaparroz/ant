from datetime import datetime
from typing import Optional
from typing import Dict
import json

from utils import get_env, get_nested_value


DATABASE_ID: str = get_env('NOTION_DATABASE_ANT_INPUT_ID')
DATE_FORMAT: str = '%Y-%m-%d'


class AntInput():
    """AntInput notion class representation
    """

    def __init__(self,
                 date: datetime,
                 spent: str,
                 description: str,
                 category: str,
                 payment: str,
                 installment: int,
                 installment_value: float,
                 value: float,
                 notion_id: Optional[int]) -> None:
        
        self.database_id = DATABASE_ID
        self.date = date.strftime(DATE_FORMAT)
        self.spent = spent
        self.description = description
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


    @classmethod
    def from_json(cls, ant_as_json: str) -> 'AntInput':
        """ Alternative constructor

        :param ant_as_json: ant as JSON string
        :return: AntInput, an instance of this class
        """
        ant_as_dict = json.loads(ant_as_json)
        return cls.from_dict(ant_as_dict)


    @classmethod
    def from_dict(cls, ant_as_dict: Dict) -> 'AntInput':
        """ Alternative constructor

        :param ant_as_dict: ant as dict
        :return: AntInput, an instance of this class
        """
        properties: dict = ant_as_dict['properties']
        treated_date = datetime.strptime(get_nested_value(properties, 'date', 'date', 'start'), DATE_FORMAT)
        
        return cls(
            notion_id=get_nested_value(properties, 'id', 'unique_id', 'number'),
            date=treated_date,
            spent=get_nested_value(properties, 'spent', 'title', 0, 'text', 'content'),
            description=get_nested_value(properties, 'description', 'rich_text', 0, 'text', 'content'),
            category=get_nested_value(properties, 'category', 'select', 'name'),
            payment=get_nested_value(properties, 'payment', 'select', 'name'),
            installment=get_nested_value(properties, 'installment', 'number'),
            installment_value=get_nested_value(properties, 'installment_value', 'formula', 'number'),
            value=get_nested_value(properties, 'value', 'number'))
    

    def get_notion_json(self) -> dict:
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
                        "value": {
                            "type": "number",
                            "number": self.value
                        }
                    }

        return body_json
