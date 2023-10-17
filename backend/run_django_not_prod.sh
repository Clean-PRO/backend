#!/bin/bash

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@ waiting for database @@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

while ! pg_isready -h db_cs -p 5432; do
    echo "База данных недоступна, ждем 5 секунд..."
    sleep 5
done

# Disconnect from Postgres client timeout
sleep 5

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@ preparing migrations @@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

python manage.py makemigrations
python manage.py migrate

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@   collecting static   @@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

python manage.py collectstatic --noinput

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@  creating superuser  @@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

if ! python manage.py shell -c "from users.models import User; print(User.objects.filter(username='admin').exists())" | grep -q "True"; then
    echo "from users.models import User; \
    admin = User.objects.create_superuser('admin@email.com', 'admin'); \
    admin.username = 'admin'; \
    admin.phone = '+799911122233'; \
    admin.save()" | python manage.py shell
    echo "Создан пользователь 'admin' с паролем 'admin' и адресом электронной почты 'admin@email.com'"
else
    echo "Пользователь 'admin' уже существует"
fi

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@  creating cleaner_1  @@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

if ! python manage.py shell -c "from users.models import User; print(User.objects.filter(username='cleaner_1').exists())" | grep -q "True"; then
    echo "from users.models import User; \
    cleaner_1 = User.objects.create_cleaner('cleaner_1@email.com', 'cleaner_1'); \
    cleaner_1.username = 'cleaner_1'; \
    cleaner_1.phone = '+899911122233'; \
    cleaner_1.save()" | python manage.py shell
    echo "Создан пользователь 'cleaner_1' с паролем 'cleaner_1' и адресом электронной почты 'cleaner_1@email.com'"
else
    echo "Пользователь 'cleaner_1' уже существует"
fi

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@  creating cleaner_2  @@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

if ! python manage.py shell -c "from users.models import User; print(User.objects.filter(username='cleaner_2').exists())" | grep -q "True"; then
    echo "from users.models import User; \
    cleaner_2 = User.objects.create_cleaner('cleaner_2@email.com', 'cleaner_2'); \
    cleaner_2.username = 'cleaner_2'; \
    cleaner_2.phone = '+999911122233'; \
    cleaner_2.save()" | python manage.py shell
    echo "Создан пользователь 'cleaner_2' с паролем 'cleaner_2' и адресом электронной почты 'cleaner_2@email.com'"
else
    echo "Пользователь 'cleaner_1' уже существует"
fi

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@  import services  @@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

python manage.py csv_services_import
python manage.py csv_cleaning_types_import

echo "Все сервисы и пакеты услуг импортированы!"

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@  cache reviews  @@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

python manage.py init_reviews_cache

echo "Все отзывы кеширваны!"

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@  run celery core @@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

celery --app=cleanpro worker -l INFO &

# Celery core startapp timeout
sleep 3

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@  run celery beat @@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

celery -A cleanpro beat -l INFO &
# Celery beat startapp timeout
sleep 3 

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@@  run gunicorn  @@@@@@@@@@@@@@@@@@@@@@@@@@@
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

gunicorn --bind 0.0.0.0:8000 cleanpro.wsgi
