# Standard library imports
import json

# Third-party application imports
from fastapi import APIRouter

# Local application imports
from models.announcement import Announcement

router = APIRouter()


@router.get("/announcements", response_model=Announcement)
async def get_announcements():
    return
    return Announcement(title="Title").json()


@router.post("/announcements")
async def create_announcement(announcement: Announcement):
    return announcement
