import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.schemas import Application, CVProfile, MatchResult, Vacancy, Verdict

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_fixture_vacancies_are_valid():
    vacancies = [Vacancy.model_validate(v) for v in load("vacancies.json")]
    assert len({v.id for v in vacancies}) == len(vacancies)


def test_fixture_cv_is_valid():
    cv = CVProfile.model_validate(load("cv.json"))
    assert cv.skills


def test_match_and_application_roundtrip():
    match = MatchResult(vacancy_id="example:1", score=80, verdict=Verdict.apply)
    app_draft = Application(vacancy_id=match.vacancy_id, cover_letter="...")
    assert Application.model_validate_json(app_draft.model_dump_json()) == app_draft


def test_health():
    assert TestClient(app).get("/health").json() == {"status": "ok"}
