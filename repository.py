from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Analysis
from schemas import AnalysisCreate, AnalysisUpdate


async def get_by_id(session: AsyncSession, analysis_id: int) -> Analysis | None:
    return await session.get(Analysis, analysis_id)


async def list_analyses(session: AsyncSession) -> list[Analysis]:
    result = await session.scalars(select(Analysis).order_by(Analysis.id))
    return list(result.all())


async def create_analysis(
    session: AsyncSession,
    payload: AnalysisCreate,
    status: str,
    *,
    result: str | None,
    created_at: datetime,
) -> Analysis:
    analysis = Analysis(
        name=payload.name,
        image_url=str(payload.image_url),
        status=status,
        result=result,
        created_at=created_at,
    )
    session.add(analysis)
    await session.flush()
    await session.refresh(analysis)
    return analysis


async def delete_analysis(session: AsyncSession, analysis_id: int) -> bool:
    analysis = await session.get(Analysis, analysis_id)
    if analysis is None:
        return False

    await session.delete(analysis)
    await session.flush()
    return True


async def update_analysis(
    session: AsyncSession,
    analysis_id: int,
    payload: AnalysisUpdate,
) -> Analysis | None:
    analysis = await session.get(Analysis, analysis_id)
    if analysis is None:
        return None

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(analysis, field, value)

    await session.flush()
    await session.refresh(analysis)
    return analysis
