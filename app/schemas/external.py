from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ExternalCity(BaseModel):
    id: int
    name: str


class ExternalTag(BaseModel):
    id: int
    name: str
    description: str


class ExternalTimetableMode(BaseModel):
    id: int
    name: str


class ExternalVacancyItem(BaseModel):
    id: int
    title: str
    timetable_mode: ExternalTimetableMode
    tag: ExternalTag
    city: Optional[ExternalCity]
    published_at: datetime
    is_remote_available: bool
    is_hot: bool

    @field_validator("published_at", mode="before")
    @classmethod
    def ensure_utc(cls, v):
        """Приводит дату из внешнего API к UTC."""
        if v is None:
            return v
        if isinstance(v, str):
            v = datetime.fromisoformat(v.replace("Z", "+00:00"))
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)



class ExternalVacanciesResponse(BaseModel):
    item_count: int = Field(alias="item_count")
    items: List[ExternalVacancyItem]
    items_per_page: int
    page: int
    page_count: int
