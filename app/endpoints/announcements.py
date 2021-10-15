# Standard library imports
from dataclasses import asdict
from typing import Optional

# Third-party application imports
from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse

# Local application imports
from schemas import Announcement
from db.dao import db_connector

TABLE_NAME = "announcements"
RESPONSE_CODES = {
    409: "item with such title already exists",

}
router = APIRouter()


@router.get("/")
def redirect():
    return RedirectResponse("/announcements")


@router.get("/announcements", response_model=list[Announcement])
def get_announcements(limit: Optional[int] = Query(10, ge=1, le=100),
                      skip: Optional[int] = Query(0, ge=0)):
    items = db_connector.get_many(TABLE_NAME, limit, skip)
    # DB gives us actual model, but not a business logic model. In our case this is an overhead when I translated
    # DB models to Pydantic models, but if our logic doesn't correspond to db model than it will require
    # additional layer somewhere with custom computed properties for example, so this step will be mandatory.
    items = [Announcement(**asdict(item)) for item in items]
    return items


@router.post("/announcements", response_model=Announcement, status_code=201)
def create_announcement(announcement: Announcement):
    item = db_connector.create_one(TABLE_NAME, announcement)
    return item
