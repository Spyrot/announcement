# Standard library imports
from datetime import datetime
from typing import Optional

# Third-party application imports
from pydantic import BaseModel

# Local application imports


class Announcement(BaseModel):
    title: str
    date: Optional[datetime] = datetime.now()
    description: Optional[str] = ""
