# Standard library imports
from datetime import datetime
from typing import Optional

# Third-party application imports
from pydantic import BaseModel, validator, Field

# Local application imports


class Announcement(BaseModel):
    title: str
    date: Optional[datetime] = Field(default_factory=datetime.now)
    description: Optional[str] = ""

    @validator("title")
    def not_empty_title(cls, v) -> str:
        if v == "":
            raise ValueError("title should not be empty")
        return v

    @validator("description")
    def not_too_long_description(cls, v) -> str:
        if len(v) > 256:
            raise ValueError("description length must be lower than 256")
        return v
