from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation, User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        await investment_process(db_obj, session)
        return db_obj


async def get_not_fully_invested(session: AsyncSession):
    charity_project = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested == 0
    ).order_by('create_date'))
    charity_project = charity_project.scalars().first()
    donation = await session.execute(select(Donation).where(
        Donation.fully_invested == 0
    ).order_by('create_date'))
    donation = donation.scalars().first()
    return charity_project, donation


async def investment_process(obj_in, session: AsyncSession):
    charity_project, donation = await get_not_fully_invested(session)
    if not charity_project or not donation:
        await session.commit()
        await session.refresh(obj_in)
        return obj_in
    project_balance = (
        charity_project.full_amount - charity_project.invested_amount
    )
    donation_balance = donation.full_amount - donation.invested_amount
    if project_balance > donation_balance:
        charity_project.invested_amount += donation_balance
        donation.invested_amount += donation_balance
        donation.fully_invested = True
        donation.close_date = datetime.now()
    elif project_balance < donation_balance:
        charity_project.invested_amount += project_balance
        donation.invested_amount += project_balance
        charity_project.fully_invested = True
        charity_project.close_date = datetime.now()
    else:
        charity_project.invested_amount = charity_project.full_amount
        charity_project.fully_invested = True
        charity_project.close_date = datetime.now()
        donation.invested_amount = donation.full_amount
        donation.fully_invested = True
        donation.close_date = datetime.now()
    session.add(charity_project)
    session.add(donation)
    await session.commit()
    await session.refresh(charity_project)
    await session.refresh(donation)
    return await investment_process(obj_in, session)
