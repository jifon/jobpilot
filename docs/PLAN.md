# План разработки JobPilot

## Фаза 0. Основа ✅
- [x] `.gitignore`, убраны `__pycache__` из git
- [x] `requirements.txt`, `.env.example`, `app/config.py`
- [x] `app/schemas.py` — общие форматы данных
- [x] Тестовые данные в `backend/test/fixtures/` + тесты схем

## Фаза 1. Скаут и разбор CV
- [ ] Скаут: один источник с официальным API (hh.ru/hh.kg `api.hh.ru/vacancies` или Remotive)
- [ ] Привести ответ к `Vacancy`, убрать дубли, сохранить в SQLite
- [ ] `POST /scout` принимает `SearchQuery`, возвращает `Vacancy[]`
- [ ] Разбор CV: PDF → текст → `CVProfile` (Claude, структурированный вывод)
- [ ] `POST /cv` загружает PDF

## Фаза 2. Аналитик
- [ ] Быстрый фильтр без LLM: пересечение навыков, отсев ниже `PREFILTER_MIN_SCORE`
- [ ] LLM-оценка → `MatchResult` (score, verdict, недостающие навыки, план подгонки)
- [ ] Кэш по `(vacancy_id, cv_hash)`

## Фаза 3. Копирайтер
- [ ] Cover letter + `CVChange[]` для вакансий с verdict = apply
- [ ] Правило: нельзя выдумывать опыт или навыки, которых нет в `CVProfile`
- [ ] Автопроверка: все упомянутые навыки есть в CV

## Фаза 4. Пайплайн и интерфейс
- [ ] `pipeline.py`: scout → analyst → copywriter, статус шагов в БД
- [ ] `POST /run`, `GET /applications`, `PATCH /applications/{id}`
- [ ] Простой фронтенд: список, score, письмо, «Одобрить» / «Отклонить»

## Фаза 5. Качество
- [ ] 10–20 пар «вакансия + CV» для проверки качества
- [ ] Второй источник вакансий, экспорт в DOCX/PDF

## Правила
- Не парсить LinkedIn и Indeed (это нарушает их правила)
- Ключи только в `.env`
- Работать в ветках `feature/*`, в `master` через PR
