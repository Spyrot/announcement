# Standard library imports
import os
from typing import Optional

# Third-party application imports
import boto3
import botocore.exceptions

# Local application imports
from db.models.announcement import Announcement
from schemas import Announcement as AnnouncementSchema

DB_ENDPOINT_URL = "DB_ENDPOINT_URL"
DB_RESOURCE_NAME = "DB_RESOURCE_NAME"
DB_REGION = "DB_REGION"

CURSOR_NEXT_TOKEN = "LastEvaluatedKey"
CURSOR_STARTING_TOKEN = "StartingToken"


class AnnouncementDao:

    def __init__(self, connection=None) -> None:
        if connection is None:
            db_resource_name = os.environ.get(DB_RESOURCE_NAME, "dynamodb")
            db_endpoint_url = os.environ.get(DB_ENDPOINT_URL, "http://localhost:8000")
            db_region = os.environ.get(DB_REGION, None)
            if db_region is not None:
                connection = boto3.resource(db_resource_name, region_name=db_region)
            else:
                connection = boto3.resource(db_resource_name, endpoint_url=db_endpoint_url)
        self.connection = connection

    def __get_from_cursor(self, table_name: str, limit: int,
                          token: Optional[dict[str, str]] = None) -> tuple[list[dict], Optional[dict[str, str]]]:
        if token:
            response = self.connection.Table(table_name).scan(Limit=limit, ExclusiveStartKey=token)
        else:
            response = self.connection.Table(table_name).scan(Limit=limit)
        next_token = response.get(CURSOR_NEXT_TOKEN, None)
        return response["Items"], next_token

    def get_many(self, table_name: str, limit: int = 10, skip: int = 0) -> list[Announcement]:
        items, token = self.__get_from_cursor(table_name, limit)
        while token and len(items) < limit+skip:
            data, token = self.__get_from_cursor(table_name, limit, token)
            items.extend(data)
        items = items[skip:skip+limit]
        return [Announcement(**item) for item in items]

    def create_one(self, table_name: str, item: AnnouncementSchema) -> Announcement:
        item = Announcement(**item.dict())
        self.connection.Table(table_name).put_item(Item=item.asdict(), ConditionExpression="attribute_not_exists(title)")
        return item


db_connector = AnnouncementDao()
