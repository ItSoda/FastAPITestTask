FROM python:3.10

SHELL [ "/bin/bash", "-c"]

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash itsoda && chmod 777 /opt /run

WORKDIR /itsoda

COPY --chown=itsoda:itsoda . .

COPY pyproject.toml poetry.lock /itsoda/

RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

CMD [ "gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000" ]