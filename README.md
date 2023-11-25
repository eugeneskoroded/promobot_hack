# Добро пожаловать на кейс Promobot!
# Решение команды Своего рода учёные
## Пользовательский интерфейс
React
WEB-приложение: [http://81.94.159.11:8080](http://81.94.159.128:8080/)

## Установка и запуск
Проект приложения расположен в папке prod
Все модули собраны в Docker образы и docker-compose, деплой осуществляется через них.
Порядок сборки образов:
1) FastAPI
* Зайти в папку [fastapi](prod/fastapi)
* Запустить команду: `docker build -t fastapi .`

2) GPT-Server
* Зайти в папку [gpt-server](prod/gpt-server)
* Запустить команду: `docker build -t gpt-server .`

3) React App
* Зайти в папку [react_app](prod/react_app)
* Запустить команду: `docker build -t react_app .`

4) В папке проекта [prod](prod) запустить команду: `docker compose up`

