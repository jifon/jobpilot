# JobPilot

Система из трёх AI-агентов, которая ищет вакансии и готовит под них отклики.

```
SearchQuery ─► Scout ─► Vacancy[] ─► Analyst ─► MatchResult[] ─► Copywriter ─► Application[]
```

Отклики — это **черновики**. Отправляет их всегда человек.

## Запуск (backend)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env          # и вписать ANTHROPIC_API_KEY
uvicorn app.main:app --reload
```

Документация API: http://127.0.0.1:8000/docs

## Тесты

```bash
cd backend
pytest
```

## Структура

```
backend/app/
  main.py              # FastAPI
  config.py            # настройки из .env
  schemas.py           # общие форматы данных между агентами
  agents/scout/        # 1. поиск вакансий
  agents/analyst/      # 2. сравнение с CV
  agents/copywriter/   # 3. cover letter и правки CV
  cv/                  # загрузка и разбор CV
  jobs/                # хранение вакансий
  users/               # пользователи
backend/test/fixtures/ # тестовые вакансии и CV
```

План разработки: [docs/PLAN.md](docs/PLAN.md)
