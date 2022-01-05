FROM python:3.8.12-alpine3.15

WORKDIR /root/app

RUN apk update && apk add \
    curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH "/root/.poetry/bin:$PATH"

COPY pyproject.toml /root/app/pyproject.toml

ARG dev
RUN if [ ! -z $dev ]; then \
        poetry install; \
        poetry export --dev -f requirements.txt --output requirements.txt; \
    else \
        poetry install --no-dev; \
        poetry export -f requirements.txt --output requirements.txt; \
    fi
RUN pip install -r requirements.txt

COPY app.py /root/app/app.py
COPY run.sh /root/app/run.sh
COPY meteofrenchapi /root/app/meteofrenchapi

CMD [ "/bin/sh", "run.sh" ]
