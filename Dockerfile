From python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR ./capsite

COPY ./capsite .

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

#RUN python3 manage.py makemigrations
#RUN python3 manage.py migrate
#RUN python3 manage.py createsuperuser