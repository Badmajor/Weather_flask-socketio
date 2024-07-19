# Пример веб приложения на Flask. Позволяет узнать погоду в реальном времени в любом городе


### Фундамент приложения основан на Flask с использованием технологий:
- flask-socketio. Вывода информации о погоде в городе и подсказки при вводе города. 
Погоду получаем по обращению к API https://open-meteo.com/.  
Города https://geocoding-api.open-meteo.com/v1/search
- flask-sqlalchemy. Сохранение истории просмотра каждого пользователя. 
Так же для подсчета количества запросов для каждого города
- flask-session. Используется для идентификации пользователей. 
Таким образом сохраняется история запросов пользователя без необходимости авторизации и 
регистрации в проложении. При повторном посещении сайта, на странице отображается 10 последних запросов 
пользователя. Сессия сохраняется 7 дней.
- flask-restful. Для создания RESTAPI. Для просмотра количество запросов каждого города
- pytest. Тесты
- redis. Для хранения сессии пользователей.
- posgres. База данных
- docker compose. Для организации управления оркестром контейнеров. Приложение разделено 
на 4 контейнера (backend, db, redis, nginx), контейнеры объединены в сеть. Обращаются друг к другу 
по имени контейнера.
- nginx. Веб-сервер.

### Запус
Для запуска приложения на машине обязательно должен быть установлен Docker 
не ниже 27.0 версии. Подробнее про установку: https://docs.docker.com/engine/install/

#### Клонируем репозиторий
```commandline
git clone git@github.com:Badmajor/Weather_flask-socketio.git
```

#### Создаем необходимый для запуска .env файл
```commandline
echo "DEBUG=True
WEATHER_URL=https://api.open-meteo.com/v1/forecast
SEARCH_CITY_URL=https://geocoding-api.open-meteo.com/v1/search
SECRET_KEY=really-secret-key

# Для PostgeSQL
DATABASE_DIALECT=postgresql
DATABASE_DRIVER=psycopg2
POSTGRES_DB=weather
POSTGRES_USER=admin_test
POSTGRES_PASSWORD=postgre_admin
POSTGRES_HOST=db
POSTGRES_PORT=5432
" > Weather_flask-socketio/.env
```
Можно заполнить файл .env.example и переименовать его в .env

#### Запускаем оркестр контейнеров
```commandline
sudo docker compose -f Weather_flask-socketio/infra/docker-compose.prod.yml up --build -d
```

## Приложение будет доступно по адресу: 
http://127.0.0.1:80/

## API: http://127.0.0.1/api/v1/
endpoints:
- /cityes - Список городов 
- 
```
            "id": int
            "name": str,
            "country": str,
            "count": int,
```