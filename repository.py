from typing import Annotated
from fastapi import Depends
from schemas import AnalysisRead

# ---------- In-memory storage ----------

analyses: dict[int, AnalysisRead] = {}
next_id = 1


# ---------- Dependency ----------

def get_storage() -> dict[int, AnalysisRead]:
    return analyses


Storage = Annotated[
    dict[int, AnalysisRead],
    Depends(get_storage),
]