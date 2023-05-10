import os

LOG_LEVEL = os.getenv("LOG_LEVEL") or "INFO"
ENVIRONMENT = os.getenv("ENVIRONMENT") or "DEV"
MICROSERVICE = os.getenv("MICROSERVICE") or "stav-poc"
DB_SECRET_NAME = "rds-flask-dev-conn"
DB_SECRET_REGION = "us-east-1"