FROM python:3.9-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

# RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev && \
    pip install --no-cache-dir -r requirements.txt 

ENTRYPOINT [ "sh", "entrypoint.sh" ]