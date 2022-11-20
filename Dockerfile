FROM python:3.8
RUN mkdir /django-stripe-lamps
COPY . /django-stripe-lamps
WORKDIR /django-stripe-lamps
RUN pip install -r requirements.txt
CMD ["sh","-c","python3 manage.py collectstatic && python3 manage.py runserver 0.0.0.0:8000"]