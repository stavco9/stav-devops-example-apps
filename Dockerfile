FROM python:3.8-slim-buster

ARG LISTEN_PORT=3000
ENV LISTEN_PORT=${LISTEN_PORT}

# Install requirements for PG Library
RUN apt install -y libpq-dev

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE ${LISTEN_PORT}

CMD ["python3", "main.py"]