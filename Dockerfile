FROM python:3.8.2

ARG PORT

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
EXPOSE ${PORT}

CMD uvicorn main:app --reload --port ${PORT} --host 0.0.0.0
#CMD gunicorn main:app --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker
