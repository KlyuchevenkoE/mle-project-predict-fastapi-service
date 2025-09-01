# Микросервис ML на FastAPI

## Описание проекта
Микросервис на FastAPI для предсказаний ML-модели. Принимает запросы, валидирует данные и возвращает предсказания в формате JSON ({"flat_id": flat_id, "prediction": ypred}). Контейнеризирован с помощью Docker, интегрирован с Prometheus и Grafana для мониторинга.

## Цели
1. Создать FastAPI-микросервис для предсказаний с валидацией данных.
2. Контейнеризировать сервис в Docker.
3. Настроить мониторинг с Prometheus и Grafana.
4. Дать инструкции для запуска и тестирования.
5. Построить дашборд Grafana для анализа метрик.

## Технологии
- FastAPI, Uvicorn: веб-фреймворк и сервер.
- Docker: контейнеризация.
- Prometheus, Grafana: мониторинг.
- prometheusfastapiinstrumentator: экспорт метрик.
- Python, Pydantic, NumPy: ядро и зависимости

## Структура
- mlservice/: код микросервиса.
- models/: ML-модель.
- services/.env: переменные окружения.
- prometheus.yml: конфиг Prometheus.
- docker-compose.yaml: сервисы FastAPI, Prometheus, Grafana.
- Dockerfile: сборка образа.
- requirements.txt: зависимости.
- Instructions.md: инструкции по запуску и примерам запросов.

## Запуск
См. Instructions.md для:
1. Запуска локально 
2. Запуска в Docker без Compose.
3. Запуска с Docker Compose.
4. Доступа к Prometheus (/metrics), Grafana.
*все этапы сопровождаются примерами запроса для конкретного исполнения. В общем случае:

## Пример запроса
curl -X POST 'http://localhost:<PORT>/howmuch/?flat_id=<flat_id>' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"x000": <x000>, "x001": <x001>, "x003": <x003>, "x005": <x005>, "x007": <x007>, "x009": <x009>, "x012": <x012>, "x017": <x017>, "x019": <x019>, "x023": <x023>}'


## Мониторинг
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Метрики: /metrics (prometheusfastapiinstrumentator).
