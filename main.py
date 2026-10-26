from datetime import datetime, timezone
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Query, Response
from schemas import *
from repository import Storage, next_id


app = FastAPI(
    title="Medical AI Analysis API",
    description="API for managing AI analysis tasks",
    version="1.0.0",
)


# ---------- Endpoints ----------

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post(
    "/analyses",
    response_model=AnalysisRead,
    status_code=201,
)
async def create_analysis(
    payload: AnalysisCreate,
    storage: Storage,
):
    global next_id

    analysis = AnalysisRead(
        id=next_id,
        name=payload.name,
        image_url=payload.image_url,
        status="pending",
        result=None,
        created_at=datetime.now(timezone.utc),
    )

    storage[analysis.id] = analysis
    next_id += 1

    return analysis


@app.get(
    "/analyses",
    response_model=list[AnalysisRead],
)
async def list_analyses(
    storage: Storage,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    items = sorted(
        storage.values(),
        key=lambda item: item.id,
    )

    return items[offset:offset + limit]


@app.get(
    "/analyses/{analysis_id}",
    response_model=AnalysisRead,
)
async def get_analysis(
    analysis_id: int,
    storage: Storage,
):
    analysis = storage.get(analysis_id)

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )

    return analysis


@app.patch(
    "/analyses/{analysis_id}",
    response_model=AnalysisRead,
)
async def update_analysis(
    analysis_id: int,
    payload: AnalysisUpdate,
    storage: Storage,
):
    analysis = storage.get(analysis_id)

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )

    updates = payload.model_dump(exclude_unset=True)

    updated_analysis = analysis.model_copy(
        update=updates,
    )

    storage[analysis_id] = updated_analysis

    return updated_analysis


@app.delete(
    "/analyses/{analysis_id}",
    status_code=204,
)
async def delete_analysis(
    analysis_id: int,
    storage: Storage,
):
    if analysis_id not in storage:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )

    del storage[analysis_id]

    return Response(status_code=204)