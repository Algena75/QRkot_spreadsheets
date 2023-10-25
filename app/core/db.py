from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


class AbstractModel(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
    fully_invested = Column(Boolean, default=False)

    @declared_attr
    def __table_args__(cls):
        return (
            CheckConstraint(
                cls.invested_amount >= 0, name='check_non_negative'
            ),
            CheckConstraint(cls.full_amount > 0, name='check_positive'),
            {}
        )


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
