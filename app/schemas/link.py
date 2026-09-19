from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, HttpUrl


class LinkCreate(BaseModel):
    original_url: AnyHttpUrl


class LinkResponse(BaseModel):
    id: int
    original_url: HttpUrl
    short_code: str
    clicks: int

    model_config = ConfigDict(from_attributes=True)


class LinkCreated(BaseModel):
    id: int
    original_url: HttpUrl
    short_code: str
    created_at: datetime
    clicks: int
    short_url: str

    model_config = ConfigDict(from_attributes=True)


class LinkStats(BaseModel):
    id: int
    short_code: str
    original_url: str
    clicks: int
    created_at: datetime
