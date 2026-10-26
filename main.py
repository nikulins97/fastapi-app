from fastapi import FastAPI, HTTPException

import services
from schemas import *


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
async def create_analysis(payload: AnalysisCreate):
    return services.create_analysis(payload)


@app.get(
    "/analyses",
    response_model=list[AnalysisRead],
)
async def list_analyses():
    items = services.get_analysis_list()

    return items


@app.get(
    "/analyses/{analysis_id}",
    response_model=AnalysisRead,
)
async def get_analysis(
    analysis_id: int,
):
    analysis = services.get_analysis_by_id(analysis_id)

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
):

    updated_analysis = services.update_analysis(analysis_id, payload)

    return updated_analysis


@app.delete(
    "/analyses/{analysis_id}",
    status_code=200,
)
async def delete_analysis(analysis_id: int):
    res = services.delete_analyses(analysis_id)

    return res