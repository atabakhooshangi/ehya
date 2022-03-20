FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1

RUN apk add --update --no-cache g++ gcc libc-dev linux-headers postgresql-dev python3-dev musl-dev jpeg-dev zlib-dev supervisor openssl-dev libffi-dev

WORKDIR /ehyasalamat

COPY docker-req.txt requirements-docker.txt

RUN pip install --upgrade pip
RUN pip install -r requirements-docker.txt


COPY . /ehyasalamat

COPY ./entrypoint.sh /

ENTRYPOINT ["sh","/entrypoint.sh"]

