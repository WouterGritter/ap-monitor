FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY *.py ./
COPY logger/*.py ./logger/
COPY tplink_api/*.py ./tplink_api/

ARG IMAGE_VERSION=Unknown
ENV IMAGE_VERSION=${IMAGE_VERSION}

CMD [ "python3", "-u", "main.py" ]
