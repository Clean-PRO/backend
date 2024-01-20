# __Cleanpro__ 🧹

Ваш самый дружелюбный и красивый web-сервис по оформлению и управлению заказами на уборку*

<sup>_\* по версии нашей бэкенд-команды_</sup>

___

### ССЫЛКИ

[Главная страница]

[API документация]

[Figma]

___

### ВВЕДЕНИЕ

CleanPRO - это веб-приложение, которое поможет вашей клининговой компании полностью автоматизировать оформление входящих заявок на уборку. Управляющему персоналу доступен удобный и информативный личный кабинет администратора, который в реальном времени позволяет отслеживать заказы и их статистику. Пользователям предлагается современный и практичный интерфейс создания заявки, спроектированный на основании результатов социального опроса десятков людей.

___

### ОПИСАНИЕ

Миссия CleanPRO - предоставить максимально удобный и доступный сервис как для заказчиков, так и для клининговой компании.

Для клиентов:
- ⚡️ быстрое оформление заказа без первичной регистрации
- 💷 прозрачность ценообразования
- 🕑 интерактивный выбор графика уборки
- 🔄 возможность повтора заказов в несколько кликов
- 🫶 интуитивно-понятный интерфейс

Для администраторов:
- 🚦 автоматическое оформление заказа и присвоение заказу уборщика без участие человека
- ⛪️ удобный личный кабинет с полным доступом ко всем заказам и персоналу
- 📊 емкая статистика заказов, охватывающая каждый их аспект от наиболее используемых услуг до самой частой причины отмен
- 📅 управление графиком работы уборщиков, в т.ч. отпуском
- 🌎 автоматическая загрузка отзывов с Я.Карт на сайт

___

### ТЕХНОЛОГИИ

CleanPRO разработан с использованием следующих технологий:

- [Python] (v.3.11) - целевой язык программирования backend
- [Django] (v.4.2) - высокоуровневый веб-фреймворк
- [Django REST framework] (v.3.14) - инструмент для создания Web API
- [PostgreSQL] (v.13.10) - объектно-реляционная база данных
- [Celery] (v.5.3) - распределенная очередь задач
- [Redis] (v.5.0) - резидентная система управления NoSQL базами данных, брокер сообщений Celery
- [PyJWT] (v.2.8) - плагин, предоставляющий JSON Web Token аутентификацию для Django REST Framework, разработанную в соответствии со стандартом RFC 7519
- [Gunicorn] (v.21.2) - Python WSGI HTTP-сервер для UNIX
- [Nginx] - HTTP-сервер и обратный прокси-сервер
- [Docker] (v.24.0) - инструмент для автоматизирования процессов разработки, доставки и запуска приложений в контейнерах

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Celery](https://a11ybadges.com/badge?logo=celery)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![PyJWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

- [JavaScript] (v.1.8) - целевой язык программирования frontend
- [React] (v.18.2) - библиотека JavaScript для разработки пользовательских интерфейсов (UI) веб-приложений
- [React Router] (v.6.15) - библиотека React для маршрутизации страниц
- [Vite] (v.4.4) - инструмент сборки JavaScript-приложений
- [Redux] (v.8.1) - библиотека  управления состоянием JavaScript приложений
- [SCSS] - метаязык написания CSS-кода

![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![React Router](https://img.shields.io/badge/React_Router-CA4245?style=for-the-badge&logo=react-router&logoColor=white)
![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
![Redux](https://img.shields.io/badge/redux-%23593d88.svg?style=for-the-badge&logo=redux&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

___

### РАЗВЕРТКА

✅ Создать корневую папку с проектом (предлагается "cleanpro") и перейти в неё

```
mkdir cleanpro
cd cleanpro
```

✅ Загрузить актуальные версии frontend и backend

```
git clone git@github.com:Clean-PRO/frontend.git
git clone git@github.com:Clean-PRO/backend.git
```

✅ Перейти в папку backend

```
cd backend/backend
```

✅ Создать файл переменных окружения из примера

```
cp .env.example .env
```

✅ Изменить переменные окружения (если необходимо)
```
(на примере редактора Nano)
nano .env
```

✅ Перейти в корневую папку backend
```
cd ..
```

✅ Запустить Docker (убедитесь, что `docker daemon` запущен в системе!)

```
docker-compose up --build
```

✅ Проверить доступность проекта на `localhost:80`

```
http://localhost:80/
```

___

### ЛИЦЕНЗИЯ

MIT

**Ура, халява!**

___

### КОМАНДА BACKEND

🦸🏻‍♂️ [Кирилл]

🧙🏻‍♀️ [Виктор]

🥷 [Владимир]

🧚‍♀️ [Регина]

[Кирилл]: <https://github.com/TheSuncatcher222/>
[Виктор]: <https://github.com/VictorTsyganov/>
[Владимир]: <https://github.com/Star-memory/>
[Регина]: <https://github.com/Reginababaika/>

[Python]: <https://www.python.org/>
[Django]: <https://www.djangoproject.com/>
[Django REST framework]: <https://www.django-rest-framework.org/>
[PostgreSQL]: <https://www.postgresql.org/>
[Celery]: <https://docs.celeryq.dev/en/stable/>
[Redis]: <https://redis.io/>
[PyJWT]: <https://pyjwt.readthedocs.io/en/latest/>
[Gunicorn]: <https://gunicorn.org/>
[Nginx]: <https://nginx.org/en/>
[Docker]: <https://www.docker.com/>

[JavaScript]: <https://www.javascript.com/>
[React]: <https://react.dev/>
[React Router]: <https://reactrouter.com/en/main/>
[Vite]: <https://vitejs.dev/>
[Redux]: <https://redux.js.org/>
[SCSS]: <https://sass-lang.com/>

[Главная страница]: <https://cleanpro.webtm.ru/>
[API документация]: <https://cleanpro.webtm.ru/docs/swagger/>
[Figma]: <https://www.figma.com/file/HJHGNY1PYZ7IC4a4SlqhdK/%D0%97%D0%B0%D0%BA%D0%B0%D0%B7-%D0%BA%D0%BB%D0%B8%D0%BD%D0%B8%D0%BD%D0%B3%D0%B0?type=design&node-id=49%3A87&mode=design&t=H31Q1xRNAieSXz5x-1/>

