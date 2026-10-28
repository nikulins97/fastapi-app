from datetime import datetime, timezone

import pytest

import repository
import services
from schemas import AnalysisCreate, AnalysisUpdate


def _payload(name="scan"):
    return AnalysisCreate(name=name, image_url="https://example.com/a.png")


def test_create_analysis_sets_defaults(monkeypatch):
    fixed_now = datetime(2026, 1, 1, tzinfo=timezone.utc)

    class FrozenDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now

    monkeypatch.setattr(services, "datetime", FrozenDatetime)

    analysis = services.create_analysis(_payload())

    assert analysis.status == "pending"
    assert analysis.result is None
    assert analysis.created_at == fixed_now


def test_update_analysis_raises_when_not_found(monkeypatch):
    monkeypatch.setattr(repository, "update_analysis", lambda *args, **kwargs: None)

    with pytest.raises(services.AnalysisNotFoundError):
        services.update_analysis(1, AnalysisUpdate(name="new name"))


