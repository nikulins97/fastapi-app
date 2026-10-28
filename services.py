from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from models import Analysis
from schemas import AnalysisCreate, AnalysisUpdate
import repository


class AnalysisNotFoundError(Exception):
    """Exception raised when an analysis is not found."""


async def create_analysis(session: AsyncSession, payload: AnalysisCreate) -> Analysis:
    return await repository.create_analysis(
        session,
        payload,
        status="pending",
        result=None,
        created_at=datetime.now(timezone.utc),
    )


async def get_analysis_by_id(session: AsyncSession, analysis_id: int) -> Analysis:
    analysis = await repository.get_by_id(session, analysis_id)

    if analysis is None:
        raise AnalysisNotFoundError("Analysis not found")

    return analysis


async def get_analysis_list(session: AsyncSession) -> list[Analysis]:
    return await repository.list_analyses(session)


async def delete_analyses(session: AsyncSession, analyses_id: int) -> bool:
    if await repository.get_by_id(session, analyses_id) is None:
        raise AnalysisNotFoundError("Analysis not found")

    return await repository.delete_analysis(session, analyses_id)


async def update_analysis(
    session: AsyncSession,
    analysis_id: int,
    payload: AnalysisUpdate,
) -> Analysis:
    updated_analysis = await repository.update_analysis(session, analysis_id, payload)

    if updated_analysis is None:
        raise AnalysisNotFoundError("Analysis not found")

    return updated_analysis
