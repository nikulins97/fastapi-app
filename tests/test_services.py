from datetime import datetime, timezone

import pytest

import repository
import services
from database import SessionLocal, engine
from schemas import AnalysisCreate, AnalysisUpdate


def _payload(name="scan"):
    return AnalysisCreate(name=name, image_url="https://example.com/a.png")


@pytest.fixture
async def session():
    async with SessionLocal() as session:
        yield session
    # The pool must be closed on this loop before pytest-asyncio shuts it down.
    await engine.dispose()


@pytest.mark.asyncio
async def test_create_analysis_sets_defaults(monkeypatch, session):
    fixed_now = datetime(2026, 1, 1, tzinfo=timezone.utc)

    class FrozenDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now

    monkeypatch.setattr(services, "datetime", FrozenDatetime)

    analysis = await services.create_analysis(session, _payload())

    assert analysis.status == "pending"
    assert analysis.result is None
    assert analysis.created_at == fixed_now


@pytest.mark.asyncio
async def test_update_analysis_raises_when_not_found(monkeypatch, session):
    async def _missing(*args, **kwargs):
        return None

    monkeypatch.setattr(repository, "update_analysis", _missing)

    with pytest.raises(services.AnalysisNotFoundError):
        await services.update_analysis(session, 1, AnalysisUpdate(name="new name"))
