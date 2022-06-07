FROM python:3.8

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD . /src
WORKDIR /src
CMD python ./manage.py runserver 0.0.0.0:8000
