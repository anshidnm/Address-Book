FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt \
    && rm -rf /tmp
