import asyncio
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from database import SessionLocal, engine
from main import app

ROOT = Path(__file__).resolve().parents[1]


def _reset_storage() -> None:
    async def _delete() -> None:
        async with SessionLocal() as session:
            await session.execute(text("DELETE FROM analyses"))
            await session.commit()
        await engine.dispose()

    asyncio.run(_delete())


@pytest.fixture(scope="session", autouse=True)
def migrate_database():
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=ROOT,
        check=True,
    )


@pytest.fixture(autouse=True)
def clean_storage():
    _reset_storage()
    yield
    _reset_storage()


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def created(client):
    response = client.post("/analyses", json={"name": "test", "image_url": "https://www.google.com/"})
    return response.json()
