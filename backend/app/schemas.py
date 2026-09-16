"""Общие форматы данных, которые агенты передают друг другу.

    SearchQuery ─► Scout ─► Vacancy[] ─► Analyst ─► MatchResult[] ─► Copywriter ─► Application[]
                                            ▲                              ▲
                                        CVProfile ─────────────────────────┘

Меняете поле здесь — проверьте всех агентов, которые его используют.
"""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field, HttpUrl


# ---------- Вход ----------

class Seniority(str, Enum):
    intern = "intern"
    junior = "junior"
    middle = "middle"
    senior = "senior"
    lead = "lead"


class SearchQuery(BaseModel):
    """Что ищем. Вход для агента-скаута."""

    stack: list[str] = Field(..., min_length=1, examples=[["Python", "FastAPI", "PostgreSQL"]])
    keywords: list[str] = Field(default_factory=list, examples=[["backend"]])
    location: str | None = Field(None, examples=["Бишкек"])
    remote: bool = True
    seniority: Seniority | None = None
    limit: int = Field(50, ge=1, le=500)


# ---------- 1. Скаут ----------

class Salary(BaseModel):
    min: int | None = None
    max: int | None = None
    currency: str | None = None  # "USD", "KGS", "RUB"...


class Vacancy(BaseModel):
    """Вакансия в едином формате, из какого бы источника она ни пришла."""

    id: str = Field(..., description="Уникальный id: '<source>:<id в источнике>'", examples=["hh:123456"])
    source: str = Field(..., examples=["hh", "remotive"])
    url: HttpUrl
    title: str
    company: str
    description: str = Field(..., description="Полный текст вакансии (без HTML)")
    skills: list[str] = Field(default_factory=list)
    location: str | None = None
    remote: bool = False
    seniority: Seniority | None = None
    salary: Salary | None = None
    published_at: datetime | None = None


# ---------- CV ----------

class Experience(BaseModel):
    company: str
    position: str
    start: date | None = None
    end: date | None = None  # None = по настоящее время
    description: str = ""
    skills: list[str] = Field(default_factory=list)


class Education(BaseModel):
    institution: str
    degree: str | None = None
    field: str | None = None
    year: int | None = None


class CVProfile(BaseModel):
    """Резюме в структурированном виде. Единственный источник правды о кандидате:
    копирайтер НЕ может упоминать то, чего здесь нет."""

    full_name: str
    title: str | None = Field(None, examples=["Backend Developer"])
    summary: str = ""
    skills: list[str] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list, examples=[["Русский — родной", "English — B2"]])
    raw_text: str = Field("", description="Исходный текст CV")


# ---------- 2. Аналитик ----------

class Verdict(str, Enum):
    apply = "apply"
    maybe = "maybe"
    skip = "skip"


class MatchResult(BaseModel):
    """Насколько вакансия подходит под CV и что подправить."""

    vacancy_id: str
    score: int = Field(..., ge=0, le=100)
    verdict: Verdict
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    reasoning: str = Field("", description="Коротко: почему такой вердикт")
    tailoring_plan: list[str] = Field(
        default_factory=list,
        description="Что подчеркнуть в CV/письме под эту вакансию",
    )


# ---------- 3. Копирайтер ----------

class CVChange(BaseModel):
    section: str = Field(..., examples=["summary", "experience[0].description"])
    before: str
    after: str
    reason: str = ""


class ApplicationStatus(str, Enum):
    draft = "draft"        # сгенерировано, ждёт проверки человеком
    approved = "approved"  # человек одобрил
    rejected = "rejected"  # человек отклонил
    sent = "sent"          # человек отправил отклик


class Application(BaseModel):
    """Готовый черновик отклика. Отправляет всегда человек."""

    vacancy_id: str
    cover_letter: str
    cv_changes: list[CVChange] = Field(default_factory=list)
    status: ApplicationStatus = ApplicationStatus.draft
    created_at: datetime = Field(default_factory=datetime.now)
