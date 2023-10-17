# Cleanpro

___

## Запуск проекта локально в контейнерах

Создать корневую папку с проектом (предлагается "cleanpro") и перейти в неё

```
mkdir cleanpro
cd cleanpro
```

Загрузить актуальные версии frontend и backend

```
git clone git@github.com:Clean-PRO/frontend.git
git clone git@github.com:Clean-PRO/backend.git
```

Перейти в папку backend

```
cd backend/backend
```

Создать файл переменных окружения из примера

```
cp .env.example .env
```

Изменить переменные окружения (если необходимо)
```
(на примере редактора Nano)
nano .env
```

Перейти в корневую папку backend
```
cd ..
```

Запустить Docker (убедитесь, что docker daemon запущен в системе!)

```
docker-compose up --build
```

## Работа с сайтом

По умолчанию проект доступен на localhost:80

```
http://localhost:80/
```
