### Описание запуска приложения MoodyLamp


# Использование environment variables

1. Файл с настройками лежит django-stripe-lamps/djstripetut/.env
2. НЕ РЕКОМЕНДУЕТСЯ заливать файл с настройками (.env) на git, так там обычно хранятся пароли и подобная информация, но так как проект тестовый, для удобства тестирования оставляю его на гите

# Запуск без использования Docker:

1. git clone https://github.com/MiMoody/django-stripe-lamps.git - склонировать репозиторий с проектом
2. cd django-stripe-lamps - перейти в папку проекта
3. pip install -r requirements.txt - установить зависимости проекта (лучше устанавливать в виртуальное окружение)
4. python manage.py collectstatic
5. python manage.py runserver host:port

# Запуск с использованием Docker

1. git clone https://github.com/MiMoody/django-stripe-lamps.git - склонировать репозиторий с проектом
2. cd django-stripe-lamps - перейти в папку проекта
3. docker build -t moody_lamp .
4. docker run -d --name stripe-lamp -v /path/to/project/:/django-stripe-lamps/ -p 9456:8000  moody_lamp