from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from app.core.config import MAX_LENGTH, MIN_LENGTH


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None, min_length=MIN_LENGTH, max_length=MAX_LENGTH
    )
    description: Optional[str] = Field(None, min_length=MIN_LENGTH)
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    @validator('full_amount')
    def amount_cant_be_negative(cls, value: int):
        if value <= 0:
            raise ValueError('Сумма должна быть больше нуля')
        return value


class CharityProjectCreate(CharityProjectUpdate):
    name: str = Field(..., min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: str = Field(..., min_length=MIN_LENGTH)
    full_amount: int = Field(..., gt=0)


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
