# Standard library imports

# Third-party application imports
from fastapi import APIRouter

# Local application imports
from endpoints import announcements

router = APIRouter()
router.include_router(announcements.router, tags=["Announcements"])