FROM python:3.12.3-alpine3.20

WORKDIR /src

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./docker/.env .

COPY ./docker/init.sh .
RUN chmod +x init.sh