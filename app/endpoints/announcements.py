# Standard library imports
from dataclasses import asdict

# Third-party application imports
from fastapi import APIRouter, HTTPException

# Local application imports
from schemas import Announcement
from db.dao import db_connector

router = APIRouter()
TABLE_NAME = "announcements"


@router.get("/announcements", response_model=list[Announcement])
async def get_announcements(limit: int = 10, page: int = 0):
    items = db_connector.get_many(TABLE_NAME, limit, page)
    # DB gives us actual model, but not a business logic model. In our case this is an overhead when I translated
    # DB models to Pydantic models, but if our logic doesn't correspond to db model than it will require
    # additional layer somewhere with custom computed properties for example, so this step will be mandatory.
    items = [Announcement(**asdict(item)) for item in items]
    return items


@router.post("/announcements", response_model=Announcement)
async def create_announcement(announcement: Announcement):
    item, code = db_connector.create_one(TABLE_NAME, announcement)
    if code != 200:
        raise HTTPException(400)
    return item
