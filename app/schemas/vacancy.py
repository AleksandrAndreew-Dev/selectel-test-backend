# from datetime import datetime, timezone
# from typing import Optional

# from pydantic import BaseModel, ConfigDict, field_validator

# class VacancyBase(BaseModel):
#     title: str
#     timetable_mode_name: str
#     tag_name: str
#     city_name: Optional[str] = None
#     published_at: datetime
#     is_remote_available: bool
#     is_hot: bool
#     external_id: Optional[int] = None

#     model_config = ConfigDict(
#         from_attributes=True
#     )

#     @field_validator("published_at", mode="before")
#     @classmethod
#     def ensure_utc(cls, v):
#         """
#         Гарантируем, что дата всегда имеет информацию о временной зоне.
#         Если зона не передана, считаем, что это UTC.
#         """
#         if isinstance(v, str):
#             v = datetime.fromisoformat(v.replace("Z", "+00:00"))
#         if v.tzinfo is None:
#             return v.replace(tzinfo=timezone.utc)
#         return v.astimezone(timezone.utc)




# class VacancyCreate(VacancyBase):
#     pass


# class VacancyUpdate(VacancyBase):
#     pass


# class VacancyRead(VacancyBase):
#     model_config = ConfigDict(from_attributes=True)

#     id: int
#     created_at: datetime

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class VacancyBase(BaseModel):
    title: str
    timetable_mode_name: str
    tag_name: str
    city_name: Optional[str] = None
    published_at: datetime
    is_remote_available: bool
    is_hot: bool
    external_id: Optional[int] = None

    @field_validator("published_at", mode="before")
    @classmethod
    def ensure_utc(cls, v):
        """Приводит входящую дату к UTC, добавляет таймзону, если её нет."""
        if v is None:
            return v
        if isinstance(v, str):
            # Заменяем Z на +00:00 для совместимости с fromisoformat
            v = datetime.fromisoformat(v.replace("Z", "+00:00"))
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)


class VacancyCreate(VacancyBase):
    pass


class VacancyUpdate(BaseModel):
    """Все поля необязательны для поддержки частичного обновления."""
    title: Optional[str] = None
    timetable_mode_name: Optional[str] = None
    tag_name: Optional[str] = None
    city_name: Optional[str] = None
    published_at: Optional[datetime] = None
    is_remote_available: Optional[bool] = None
    is_hot: Optional[bool] = None
    external_id: Optional[int] = None

    # Валидатор для published_at, если поле передано
    @field_validator("published_at", mode="before")
    @classmethod
    def ensure_utc(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            v = datetime.fromisoformat(v.replace("Z", "+00:00"))
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)


class VacancyRead(VacancyBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        # Явно задаём формат вывода дат (как в отчёте)
        json_encoders={
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")
        }
    )
