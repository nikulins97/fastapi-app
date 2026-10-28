from datetime import datetime
from typing import Annotated
from fastapi import Depends
from schemas import AnalysisRead, AnalysisCreate, AnalysisUpdate

# ---------- In-memory storage ----------

analyses: dict[int, AnalysisRead] = {}
next_id = 1


# ---------- Dependency ----------

def get_storage() -> dict[int, AnalysisRead]:
    return analyses

def get_by_id(analysis_id: int) -> AnalysisRead | None:
    return analyses.get(analysis_id)

def create_analysis(
    payload: AnalysisCreate,
    status,
    *,
    result: str | None,
    created_at: datetime,
) -> AnalysisRead:
    global next_id

    analysis = AnalysisRead(
        id=next_id,
        name=payload.name,
        image_url=payload.image_url,
        status="pending",
        result=result,
        created_at=created_at,
    )

    analyses[analysis.id] = analysis
    next_id += 1

    return analysis

def delete_analysis(analysis_id: int) -> bool:
    return analyses.pop(analysis_id, None) is not None

def update_analysis(
    analysis_id: int,
    payload: AnalysisUpdate,
) -> AnalysisRead | None:
    analysis = analyses.get(analysis_id)

    if analysis is None:
        return None

    updated_data = payload.model_dump(exclude_unset=True)

    updated_analysis = analysis.model_copy(
        update=updated_data,
    )

    analyses[analysis_id] = updated_analysis

    return updated_analysis


Storage = Annotated[
    dict[int, AnalysisRead],
    Depends(get_storage),
]