from datetime import datetime, timezone

from schemas import AnalysisCreate, AnalysisRead, AnalysisUpdate
import repository

class AnalysisNotFoundError(Exception):
    """Exception raised when an analysis is not found."""


def create_analysis(payload: AnalysisCreate) -> AnalysisRead:
    return repository.create_analysis(
        payload,
        status="pending",
        result=None,
        created_at=datetime.now(timezone.utc),
    )



def get_analysis_by_id(analysis_id: int) -> AnalysisRead | None:
    analysis = repository.get_by_id(analysis_id)

    if analysis is None:
        raise AnalysisNotFoundError("Analysis not found")

    return analysis

def get_analysis_list():
    analysis_list = repository.get_storage()

    return list(analysis_list.values())

def delete_analyses(analyses_id: int):
    if repository.get_by_id(analyses_id) is None:
        raise AnalysisNotFoundError("Analysis not found")

    return repository.delete_analysis(analyses_id)



def update_analysis(
    analysis_id: int,
    payload: AnalysisUpdate,
) -> AnalysisRead:
    updated_analysis = repository.update_analysis(analysis_id, payload)

    if updated_analysis is None:
        raise AnalysisNotFoundError("Analysis not found")

    return updated_analysis