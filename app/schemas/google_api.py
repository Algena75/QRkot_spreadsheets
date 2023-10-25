from datetime import timedelta

from pydantic import BaseModel


class GoogleList(BaseModel):
    name: str
    duration: timedelta
    description: str
