from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


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

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')
        }
    )



class ExternalVacanciesResponse(BaseModel):
    item_count: int = Field(alias="item_count")
    items: List[ExternalVacancyItem]
    items_per_page: int
    page: int
    page_count: int
