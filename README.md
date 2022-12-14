### Описание запуска приложения MoodyLamp

# Тест готового проекта на удаленном сервере
1. URL: https://moodylamp.mimoody.space/

# Использование environment variables

1. Файл с настройками лежит django-stripe-lamps/djstripetut/.env
2. НЕ РЕКОМЕНДУЕТСЯ заливать файл с настройками (.env) на git, так там обычно хранятся пароли и подобная информация, но так как проект тестовый, для удобства тестирования оставляю его на гите

# Запуск без использования Docker:

1. git clone https://github.com/MiMoody/django-stripe-lamps.git - склонировать репозиторий с проектом
2. cd django-stripe-lamps - перейти в папку проекта
3. pip install -r requirements.txt - установить зависимости проекта (лучше устанавливать в виртуальное окружение)
4. python manage.py collectstatic
5. python manage.py runserver
6. http://localhost:8000/ - перейти по адресу 

# Запуск с использованием Docker со сборкой

1. git clone https://github.com/MiMoody/django-stripe-lamps.git - склонировать репозиторий с проектом
2. cd django-stripe-lamps - перейти в папку проекта
3. В файле ./djstriptut/.env необходимо поменять переменную DOMAIN на http://localhost:9456/
4. docker build -t moody_lamp .
5. docker run -d --name stripe-lamp -v /path/to/project/media/:/django-stripe-lamps/media/ -v /path/to/project/localdb/:/django-stripe-lamps/localdb/ -p 9456:8000  moody_lamp

ИЛИ запуск без volumes (но данные из бд и добавленная media во время работы не сохранится):

docker run -d --name stripe-lamp -p 9456:8000  mikimoody/moody_lamp

6. http://localhost:9456/ - перейти по адресу 

# Запуск с использованием Docker без сборки (образ лежит на dockerhub: mikimoody/moody_lamp)

1. docker run -d --name stripe-lamp -v /path/to/project/media/:/django-stripe-lamps/media/ -v /path/to/project/localdb/:/django-stripe-lamps/localdb/ -p 9456:8000  moody_lamp

ИЛИ запуск без volumes (но данные из бд и добавленная media во время работы не сохранится):

docker run -d --name stripe-lamp -p 9456:8000  mikimoody/moody_lamp

# Тестовые карты для оплаты stripe

## Успешная оплата:

1. Номер карты: 4242424242424242
2. Дата: 12/34 
3. CVC: 111

## Неудачная оплата:

1. Номер карты: 4000000000000002
2. Дата: 12/34 
3. CVC: 111

# Доступ к панели Django Admin

1. Url: http://host:port/admin
1. Login:admin
2. Password:admin