from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import services
from database import engine, get_session
from schemas import AnalysisCreate, AnalysisRead, AnalysisUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="Medical AI Analysis API",
    description="API for managing AI analysis tasks",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(services.AnalysisNotFoundError)
async def analysis_not_found_error_handler(request: Request, exc: services.AnalysisNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": "Analysis not found"},
    )


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
    session: AsyncSession = Depends(get_session),
):
    return await services.create_analysis(session, payload)


@app.get(
    "/analyses",
    response_model=list[AnalysisRead],
)
async def list_analyses(session: AsyncSession = Depends(get_session)):
    return await services.get_analysis_list(session)


@app.get(
    "/analyses/{analysis_id}",
    response_model=AnalysisRead,
)
async def get_analysis(
    analysis_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await services.get_analysis_by_id(session, analysis_id)


@app.patch(
    "/analyses/{analysis_id}",
    response_model=AnalysisRead,
)
async def update_analysis(
    analysis_id: int,
    payload: AnalysisUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await services.update_analysis(session, analysis_id, payload)


@app.delete(
    "/analyses/{analysis_id}",
    status_code=200,
)
async def delete_analysis(
    analysis_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await services.delete_analyses(session, analysis_id)
