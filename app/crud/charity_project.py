from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(select(CharityProject.id).where(
            CharityProject.name == project_name
        ))
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list:
        projects = await session.execute(select(CharityProject).where(
            CharityProject.fully_invested == 1
        ))
        projects = projects.scalars().all()
        project_list = []
        for project in projects:
            project_list.append({
                'name': project.name,
                'duration': project.close_date - project.create_date,
                'description': project.description
            })
        project_list = sorted(project_list, key=lambda x: x['duration'])
        return project_list


charity_project_crud = CRUDCharityProject(CharityProject)
