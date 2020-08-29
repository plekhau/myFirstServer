FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY birds birds
COPY myServer myServer
COPY templates templates
COPY manage.py .
COPY wait-for-db.sh .
RUN sed -i "s/'HOST': 'localhost'/'HOST': 'db'/g" myServer/settings.py

CMD ./wait-for-db.sh && python manage.py runserver 0.0.0.0:8080
