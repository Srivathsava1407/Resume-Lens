import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from backend.models.schemas import AnalysisResult, SkillGap


MOCK_RESULT = AnalysisResult(
    match_score=78,
    summary="Strong candidate with relevant Python and API experience. Missing some cloud keywords.",
    matched_keywords=["Python", "FastAPI", "REST API", "Git"],
    missing_keywords=["AWS", "Docker", "Kubernetes"],
    skill_gaps=[
        SkillGap(skill="AWS", present_in_resume=False, importance="preferred",
                 suggestion="Add any AWS projects or certifications"),
        SkillGap(skill="Docker", present_in_resume=False, importance="required",
                 suggestion="Include Docker in your tech stack section"),
    ],
    strengths=["Strong Python background", "REST API experience matches well"],
    improvements=["Add cloud platform experience", "Mention containerization tools"],
    cover_letter=None,
)


@pytest.mark.asyncio
async def test_analyze_endpoint_with_text(client):
    with patch("backend.routers.analyze.analyze_resume", new_callable=AsyncMock) as mock_ai:
        mock_ai.return_value = MOCK_RESULT

        response = client.post(
            "/api/analyze",
            data={
                "resume_text": "Python developer with 2 years experience...",
                "job_description": "Looking for Python engineer with FastAPI...",
                "generate_cover_letter": "false",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["match_score"] == 78
        assert "Python" in data["matched_keywords"]
        assert len(data["skill_gaps"]) == 2


@pytest.mark.asyncio
async def test_analyze_endpoint_missing_inputs(client):
    response = client.post(
        "/api/analyze",
        data={"job_description": "Some job description"},
    )
    assert response.status_code == 400


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from backend.main import app
    return TestClient(app)
