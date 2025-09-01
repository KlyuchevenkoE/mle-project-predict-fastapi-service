# Инструкции по запуску микросервиса

## 0. Загрузка модели
```python

# создание виртуального пространства
sudo apt-get install python3.10-venv
python3.10 -m venv .virt 
# и установки необходимых библиотек в него
pip install -r requirements.txt
source .virt/bin/activate # используется для всех дальнейших команд
cd services # используется для всех дальнейших команд
```

### Запуск mlflow

```bash
sh load_model/mlflow_start_server.sh

```
### выгрузка модели

```bash
python3.10 load_model/load_model.py #модель выгружается в директорию models/

```

## 1. FastAPI микросервис в виртуальном окружение
```bash
# команда запуска сервиса с помощью uvicorn
uvicorn ml_service.estate_app:app --reload --port 8081 --host 0.0.0.0 
```

### Пример curl-запроса к микросервису

```bash
curl -X POST 'http://localhost:8081/howmuch/?flat_id=345345' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"x000": 307, "x001": 9, "x003": 9, "x005": 10, "x007": 82, "x009": 5.84, "x012": 9, "x017": 0, "x019": 0, "x023": 0}'

```


## 2. FastAPI микросервис в Docker-контейнере

```bash
# команда для запуска микросервиса 
docker build . --tag flats
docker container run --publish 4600:1702 --env-file .env --volume=./models:/services/models flats

```

### Пример curl-запроса к микросервису

```bash
curl -X POST 'http://localhost:4600/howmuch/?flat_id=345345' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"x000": 307, "x001": 9, "x003": 9, "x005": 10, "x007": 82, "x009": 5.84, "x012": 9, "x017": 0, "x019": 0, "x023": 0}'

```

## 3. Docker compose для микросервиса и системы моониторинга

```bash
# команда для запуска микросервиса в режиме docker compose
docker compose up --build
```

### Пример curl-запроса к микросервису 

```bash
 curl -X POST 'http://localhost:1702/howmuch/?flat_id=345345' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"x000": 307, "x001": 9, "x003": 9, "x005": 10, "x007": 82, "x009": 5.84, "x012": 9, "x017": 0, "x019": 0, "x023": 0}'
```

## 4. Скрипт симуляции нагрузки
Скрипт выполняет 60 POST-запросов на http://localhost:1702/howmuch/?flat_id=..., где flat_id увеличивается от 345001 и далее. Для каждого запроса он формирует JSON из полей x***, чьи значения детерминированно вычисляются по индексу i, и выводит в консоль код ответа, время и размер. Между запросами пауза 1 с, а после 30-го запроса — дополнительная пауза 10 с

# команды необходимые для запуска скрипта
```bash
sh synthetic_test.sh
```
Адреса сервисов:
- микросервис: http://localhost:1702/
- Prometheus: http://localhost:9090/
- Grafana: http://localhost:3000/