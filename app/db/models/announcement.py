# Standard library imports
from dataclasses import dataclass, field
from datetime import datetime

# Third-party application imports

# Local application imports


@dataclass
class Announcement:
    title: str
    date: str
    _date: str = field(init=False, repr=False, default=datetime.now().isoformat())
    description: str = ""

    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, v: datetime) -> None:
        if type(v) is property:
            v = Announcement._date
        if type(v) is datetime:
            self._date = v.isoformat()
        if type(v) is str:
            self._date = v

    def asdict(self) -> dict:
        return {"title": self.title, "date": self.date, "description": self.description}
