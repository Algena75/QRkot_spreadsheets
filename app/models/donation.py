from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import AbstractModel


class Donation(AbstractModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)
