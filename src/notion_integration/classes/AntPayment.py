from datetime import datetime
from typing import Optional
from typing import Dict
import json

from utils import get_env, get_nested_value


DATABASE_ID: str = get_env('NOTION_DATABASE_ANT_PAYMENT_ID')
DATE_FORMAT: str = '%Y-%m-%d'


class AntPayment():
    """AntPayment notion class representation
    """

    def __init__(self,
                 period: str,
                 payment: str,
                 spents: int,
                 value: float,
                 notion_id: Optional[int] = None) -> None:
        
        self.database_id = DATABASE_ID
        self.period = period
        self.payment = payment
        self.spents = spents
        self.value = value
        self.notion_id = notion_id


    def to_dict(self) -> dict:
        body_as_dict: dict = {
            'DatabaseId': self.database_id,
            'ID': self.notion_id,
            'Period': self.period,
            'Payment': self.payment,
            'Spents': self.spents,
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
    def from_json(cls, ant_payment_as_json: str) -> 'AntPayment':
        """ Alternative constructor

        :param ant_payment_as_json: ant as JSON string
        :return: AntPayment, an instance of this class
        """
        ant_payment_as_dict = json.loads(ant_payment_as_json)
        return cls.from_dict(ant_payment_as_dict)


    @classmethod
    def from_dict(cls, ant_payment_as_dict: Dict) -> 'AntPayment':
        """ Alternative constructor

        :param ant_payment_as_dict: ant as dict
        :return: AntPayment, an instance of this class
        """
        properties: dict = ant_payment_as_dict['properties']
        
        return cls(
            notion_id=get_nested_value(properties, 'id', 'unique_id', 'number'),
            period=get_nested_value(properties, 'period', 'title', 0, 'text', 'content'),
            payment=get_nested_value(properties, 'payment', 'select', 'name'),
            spents=get_nested_value(properties, 'spents', 'number'),
            value=get_nested_value(properties, 'value', 'number'))
    

    def get_notion_json(self) -> dict:
        """Get notion expect json

        Returns:
            dict: Notion json to post a page
        """
        body_json: dict = {
                        "period": {
                            "id": "period",
                            "type": "title",
                            "title": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": self.period,
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
                                    "plain_text": self.period,
                                    "href": None,
                                }
                            ],
                        },
                        "spents": {
                            "type": "number",
                            "number": self.spents
                        },
                        "payment": {
                            "type": "select",
                            "select": {
                                "name": self.payment,
                            }
                        },
                        "value": {
                            "type": "number",
                            "number": self.value
                        }
                    }

        return body_json
