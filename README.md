# Добро пожаловать на кейс Promobot!
# Решение команды Своего рода учёные
## Пользовательский интерфейс
React
WEB-приложение: [http://81.94.159.11:8080](http://81.94.159.128:8080/)

# Установка и запуск
## Проект приложения расположен в папке prod
### Все модули собраны в Docker образы и docker-compose, деплой осуществляется через них.
Порядок сборки образов:
1) FastAPI
* Зайти в папку [fastapi](prod/fastapi)
* Запустить команду: `docker build -t fastapi .`

2) GPT-Server
* Зайти в папку [gpt-server](prod/gpt-server)
* Запустить команду: `docker build -t gpt_server .`

3) React App
* Зайти в папку [react_app](prod/react_app)
* Запустить команду: `docker build -t react_app .`

4) В папке проекта [prod](prod)
* Открыть файл `docker-compose.yml`
* Изменить адреса серверов в пунктах `ports:` на адреса вашего сервера
### Это должно выглядеть так:
  ```dockerfile
  
      version: '3'
      services:
        react_app:
          image: react_app
          ports:
            - "АДРЕС.ВАШЕГО.ДЕПЛОЙ.СЕРВЕРА:ПОРТ1:8080"
        fastapi:
          image: fastapi
          runtime: nvidia # uncomment on server with GPU
          command: uvicorn fastapp:app --reload --host "0.0.0.0" --port 8081
          environment:
            - NVIDIA_VISIBLE_DEVICES=0
            - NVIDIA_DRIVER_CAPABILITIES=compute,utility
            - PYTHONUNBUFFERED=1
          ports:
            - "81.94.159.128:8081:8081"
        gpt_server:
          image: gpt_server
          stdin_open: true
          tty: true
          runtime: nvidia # uncomment on server with GPU
          command: gunicorn -w 1 --bind 0.0.0.0:8082 --timeout 3600 gpt_server:app
          environment:
            - NVIDIA_VISIBLE_DEVICES=0
            - NVIDIA_DRIVER_CAPABILITIES=compute,utility
            - PYTHONUNBUFFERED=1
            - MODEL_NAME=IlyaGusev/saiga2_13b_lora
            - BASE_MODEL_PATH=TheBloke/Llama-2-13B-fp16
          volumes:
            - /home/ubuntu/projects/volume:/user/volume
          ports:
            - 0.0.0.0:8082:8082
  ```
* Запустить команду: `docker compose up` из папки [prod](prod)

