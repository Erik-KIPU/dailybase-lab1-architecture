# Платформа индивидуальной траектории обучения

Результаты лабораторных работ №1–4 по проекту платформы для преподавателей и репетиторов.

Платформа помогает вести учащихся, планировать занятия, хранить учебные материалы, выдавать домашние задания, проводить тестирование и анализировать прогресс. На основании накопленных результатов система формирует рекомендации и помогает корректировать индивидуальную траекторию обучения.

## Лабораторная работа №1

В репозитории представлены:

- [ARCHITECTURE.md](ARCHITECTURE.md) — архитектурный отчёт;
- [C4 Container diagram](docs/c4-container.mmd) — исходник диаграммы контейнеров;
- [ER diagram](docs/erd.mmd) — исходник ER-диаграммы базы данных;
- [план разработки](PLAN.md) — расширенный план реализации проекта.

## Основные роли

- **Преподаватель** — работает с учащимися, занятиями, учебными планами, материалами, заданиями, тестами и аналитикой.
- **Администратор** — управляет пользователями, ролями, предметами, заданиями и общими учебными планами.

Личный кабинет учащегося в первую версию проекта не входит и может быть добавлен отдельным этапом.

## Технологический контур

- Frontend: React + TypeScript;
- Backend: FastAPI + Python;
- Database: PostgreSQL;
- фоновые задачи: Redis и worker;
- файлы: MinIO или S3-совместимое хранилище;
- уведомления: Telegram Bot API и SMTP;
- развёртывание: Docker Compose;
- API: REST и OpenAPI.

## Архитектурный подход

Первая версия строится как модульный монолит: React-клиент обращается к FastAPI REST API, а backend работает с PostgreSQL и объектным хранилищем. Redis используется для очереди фоновых задач, включая отправку уведомлений. Такое решение сохраняет простоту разработки и позволяет выделить worker без преждевременного перехода к микросервисам.

Подробные сценарии, сущности, ограничения и диаграммы находятся в [ARCHITECTURE.md](ARCHITECTURE.md).

## Лабораторная работа №2 — REST API и OpenAPI

- [openapi.yaml](openapi.yaml) — OpenAPI 3.0.3, аутентификация и CRUD учащихся, занятий и предметов.
- [REST API Specs](ARCHITECTURE.md#11-rest-api-specs--лабораторная-работа-2) — таблица методов, ролей и кодов ответа.
- [Инструкция и контрольные вопросы](docs/LAB2.md).
- [Swagger UI](docs/swagger.html) — локальная интерактивная документация.

Просмотр: `python -m http.server 8080 --bind 127.0.0.1`, затем открыть
`http://127.0.0.1:8080/docs/swagger.html`. Это сервер документации, а не backend API.

## Лабораторная работа №3 — каркас FastAPI

Реализованы слои API, сервиса и доменной модели, адаптер часов, конфигурация окружения и публичный GET /api/v1/health. PostgreSQL и бизнес-операции из проектного контракта пока не реализованы.

Быстрый запуск из корня репозитория в PowerShell (Python 3.10+):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m backend.app
```

Копировать .env.example нужно только при первом запуске. В локальном .env настраиваются APP_NAME, APP_VERSION, APP_ENV, HTTP_HOST, HTTP_PORT.

- [Health check](http://127.0.0.1:8000/api/v1/health).
- [Swagger реализованного backend](http://127.0.0.1:8000/docs).
- [Подробный отчёт, проверки и ответы для защиты](docs/LAB3.md).

Тестирование:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts/validate_openapi.py
```

GitHub Actions запускает эти проверки на push и pull request.

## Лабораторная работа №4 — Docker

Каркас backend из ЛР3 упакован в образ на основе `python:3.11-slim`.
В корне находятся [Dockerfile](Dockerfile) и [.dockerignore](.dockerignore).

При запущенном Docker Desktop в режиме Linux containers выполните из корня репозитория:

```powershell
docker build -t dailybase-backend:lab4 .
docker images dailybase-backend
docker run --name dailybase-lab4 -d -p 127.0.0.1:8084:8000 -e HTTP_HOST=0.0.0.0 -e HTTP_PORT=8000 -e APP_ENV=production dailybase-backend:lab4
curl.exe http://127.0.0.1:8084/api/v1/health
docker logs dailybase-lab4
```

- [Health контейнера](http://127.0.0.1:8084/api/v1/health).
- [Swagger контейнера](http://127.0.0.1:8084/docs).
- [Отчёт, порядок демонстрации и пять контрольных вопросов](docs/LAB4.md).

Порт `8084` на компьютере перенаправляется на `8000` внутри контейнера;
`8080` остаётся доступным для документации ЛР2. Настройки передаются при запуске,
локальный `.env` в образ не включается.

Остановка и удаление контейнера (образ сохраняется):

```powershell
docker stop dailybase-lab4
docker rm dailybase-lab4
```
